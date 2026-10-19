-- Run once in a NEW Supabase project. Register the verified owner UUID afterward.
begin;
create schema if not exists private;
revoke all on schema private from public,anon,authenticated;
create table private.site_admins(user_id uuid primary key references auth.users(id));
alter table private.site_admins enable row level security;
create function public.is_site_admin() returns boolean language sql stable security definer set search_path='' as $$
 select exists(select 1 from private.site_admins where user_id=(select auth.uid()));
$$;
revoke all on function public.is_site_admin() from public;
grant execute on function public.is_site_admin() to authenticated;

create table public.reader_messages(
 id uuid primary key default gen_random_uuid(),
 user_id uuid not null default auth.uid() references auth.users(id) on delete cascade,
 post_path text not null check(post_path ~ '^/post-[a-z0-9-]+\.html$'),
 body text not null check(char_length(trim(body)) between 1 and 5000),
 created_at timestamptz not null default now(),
 reply text check(char_length(reply)<=5000),replied_at timestamptz
);
create index on public.reader_messages(user_id,created_at desc);
alter table public.reader_messages enable row level security;
revoke all on public.reader_messages from public,anon,authenticated;
grant select on public.reader_messages to authenticated;
grant insert(post_path,body) on public.reader_messages to authenticated;
grant update(reply,replied_at) on public.reader_messages to authenticated;
create policy own_or_owner_read on public.reader_messages for select to authenticated
 using(user_id=(select auth.uid()) or (select public.is_site_admin()));
create policy reader_insert on public.reader_messages for insert to authenticated
 with check(user_id=(select auth.uid()) and reply is null and replied_at is null);
create policy owner_reply on public.reader_messages for update to authenticated
 using((select public.is_site_admin())) with check((select public.is_site_admin()));
create function public.limit_message_rate() returns trigger language plpgsql security definer set search_path='' as $$
begin
 perform pg_advisory_xact_lock(hashtext(new.user_id::text));
 if(select count(*) from public.reader_messages where user_id=new.user_id and created_at>now()-interval '1 hour')>=10 then
 raise exception 'Please wait before sending more messages';end if;return new;
end;$$;
revoke all on function public.limit_message_rate() from public;
create trigger limit_messages before insert on public.reader_messages for each row execute function public.limit_message_rate();

create table public.site_visits(
 id uuid primary key,session_id uuid not null,path text not null,referrer_host text not null default '',
 device text not null check(device in('mobile','tablet','desktop')),
 started_at timestamptz not null default now(),updated_at timestamptz not null default now(),
 active_ms integer not null default 0 check(active_ms between 0 and 86400000),
 scroll_percent integer not null default 0 check(scroll_percent between 0 and 100)
);
create index on public.site_visits(started_at);
create index on public.site_visits(path,started_at);
alter table public.site_visits enable row level security;
revoke all on public.site_visits from public,anon,authenticated;
grant select on public.site_visits to authenticated;
create policy owner_only_statistics on public.site_visits for select to authenticated using((select public.is_site_admin()));
create function public.record_site_visit(p_id uuid,p_session uuid,p_path text,p_referrer text,p_device text,p_active integer,p_scroll integer)
returns void language plpgsql security definer set search_path='' as $$
begin
 if p_path !~ '^/([a-zA-Z0-9_-]+\.html)?$' or char_length(p_referrer)>180 or p_referrer !~ '^[a-zA-Z0-9.:-]*$'
 or p_device not in('mobile','tablet','desktop') or p_active<0 or p_active>86400000 or p_scroll<0 or p_scroll>100 then
 raise exception 'Invalid analytics event';end if;
 insert into public.site_visits(id,session_id,path,referrer_host,device,active_ms,scroll_percent)
 values(p_id,p_session,p_path,p_referrer,p_device,least(p_active,5000),p_scroll)
 on conflict(id) do update set
 active_ms=greatest(public.site_visits.active_ms,least(p_active,(extract(epoch from now()-public.site_visits.started_at)*1000+5000)::integer)),
 scroll_percent=greatest(public.site_visits.scroll_percent,p_scroll),updated_at=now()
 where public.site_visits.path=p_path and public.site_visits.session_id=p_session and public.site_visits.started_at>now()-interval '24 hours';
end;$$;
revoke all on function public.record_site_visit(uuid,uuid,text,text,text,integer,integer) from public;
grant execute on function public.record_site_visit(uuid,uuid,text,text,text,integer,integer) to anon,authenticated;

create function public.site_dashboard(p_days integer default 30) returns jsonb language plpgsql stable security definer set search_path='' as $$
declare answer jsonb;
begin
 if not public.is_site_admin() then raise exception 'Owner access required' using errcode='42501';end if;
 if p_days not between 1 and 366 then raise exception 'Invalid date range';end if;
 with v as(select * from public.site_visits where started_at>=now()-make_interval(days=>p_days)),
 pages as(select path,count(*) views,count(distinct session_id) sessions,round(avg(active_ms)/1000,1) active_seconds,round(avg(scroll_percent),1) scroll,
 round(100.0*count(*) filter(where scroll_percent>=90)/nullif(count(*),0),1) completion from v group by path order by views desc),
 days as(select to_char(started_at at time zone 'Asia/Shanghai','YYYY-MM-DD') day,count(*) views,count(distinct session_id) sessions from v group by 1 order by 1),
 refs as(select referrer_host source,count(*) views from v group by 1 order by 2 desc),
 devices as(select device,count(*) views from v group by 1 order by 2 desc)
 select jsonb_build_object('views',(select count(*) from v),'sessions',(select count(distinct session_id) from v),
 'active_seconds',(select coalesce(round(avg(active_ms)/1000,1),0) from v),
 'pages',coalesce((select jsonb_agg(to_jsonb(pages)) from pages),'[]'::jsonb),
 'days',coalesce((select jsonb_agg(to_jsonb(days)) from days),'[]'::jsonb),
 'referrers',coalesce((select jsonb_agg(to_jsonb(refs)) from refs),'[]'::jsonb),
 'devices',coalesce((select jsonb_agg(to_jsonb(devices)) from devices),'[]'::jsonb)) into answer;return answer;
end;$$;
revoke all on function public.site_dashboard(integer) from public;
grant execute on function public.site_dashboard(integer) to authenticated;
commit;
-- After the owner signs in, obtain the UUID from Auth > Users, then run:
-- insert into private.site_admins(user_id) values('OWNER_AUTH_UUID');
