(() => {
 'use strict';
 const api=window.PrivateSite,status=document.getElementById('status'),form=document.getElementById('login'),owner=document.getElementById('owner');
 if(!api?.available){status.textContent='Use Umami for private traffic analytics and the Private inbox for reader messages and replies. Both require your own sign-in.';form.hidden=true;return;}
 const {el,request}=api;let offset=0;
 function table(target,head,rows){const node=document.getElementById(target);node.replaceChildren();const table=el('table'),tr=el('tr');head.forEach(x=>tr.append(el('th',x)));table.append(tr);rows.forEach(row=>{const tr=el('tr');row.forEach(cell=>tr.append(el('td',cell)));table.append(tr);});node.append(table);}
 form.onsubmit=async e=>{e.preventDefault();try{await api.login(form.elements.email.value.trim());status.textContent='Check your email. Open the link in this browser.';}catch(error){status.textContent=error.message;}};
 async function messages(reset=true){
  if(reset){offset=0;document.getElementById('messages').replaceChildren();}
  const rows=await request('/rest/v1/reader_messages?select=*&order=created_at.desc&limit=50&offset='+offset,undefined,'GET',true);
  for(const row of rows){const item=el('article');item.className='message';item.append(el('small',row.post_path+' · '+new Date(row.created_at).toLocaleString()),el('p',row.body));const label=el('label','Private reply'),reply=el('textarea');reply.rows=3;reply.maxLength=5000;reply.value=row.reply||'';label.append(reply);const button=el('button','Save private reply');button.onclick=async()=>{button.disabled=true;try{await request('/rest/v1/reader_messages?id=eq.'+encodeURIComponent(row.id),{reply:reply.value.trim(),replied_at:new Date().toISOString()},'PATCH',true);status.textContent='Reply saved privately.';}catch(error){status.textContent=error.message;}finally{button.disabled=false;}};item.append(label,button);document.getElementById('messages').append(item);}
  offset+=rows.length;document.getElementById('more').hidden=rows.length<50;
 }
 async function refresh(){try{
  const d=await request('/rest/v1/rpc/site_dashboard',{p_days:Number(document.getElementById('days').value)},'POST',true);
  owner.hidden=false;form.hidden=true;status.textContent='Owner access verified by the database.';
  document.getElementById('metrics').replaceChildren(el('p',`${d.views} page views · ${d.sessions} estimated sessions · ${d.active_seconds}s average active time per view`));
  table('pages',['Page','Views','Sessions','Active seconds / view','Scroll %','90% scroll completion %'],d.pages.map(p=>[p.path,p.views,p.sessions,p.active_seconds,p.scroll,p.completion]));
  table('daily',['Date (Beijing)','Views','Sessions'],d.days.map(p=>[p.day,p.views,p.sessions]));
  table('sources',['Type','Source','Views'],[...d.referrers.map(p=>['Referrer',p.source||'Direct / unknown',p.views]),...d.devices.map(p=>['Device',p.device,p.views])]);await messages();
 }catch(error){owner.hidden=true;status.textContent=error.message;}}
 document.getElementById('refresh').onclick=refresh;document.getElementById('days').onchange=refresh;document.getElementById('signout').onclick=api.logout;document.getElementById('more').onclick=()=>messages(false).catch(error=>status.textContent=error.message);
 if(api.signedIn())refresh();else status.textContent='Sign in with the owner account. Other accounts cannot read these statistics.';
})();
