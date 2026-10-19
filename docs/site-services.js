/* No network requests or collection occur until the backend is configured. */
(() => {
 'use strict';
 const config=window.SITE_SERVICES||{};
 const available=config.enabled&&/^https:\/\/[a-z0-9-]+\.supabase\.co$/.test(config.url||'')&&!!config.publishableKey;
 const authKey='site-reader-auth';let session;
 try{session=JSON.parse(sessionStorage.getItem(authKey)||'null');}catch{session=null;}
 const fragment=new URLSearchParams(location.hash.slice(1));
 if(fragment.has('access_token')){
  session={access_token:fragment.get('access_token'),expires_at:Date.now()+Number(fragment.get('expires_in')||3600)*1000};
  try{sessionStorage.setItem(authKey,JSON.stringify(session));}catch{}
  history.replaceState(null,'',location.pathname+location.search);
 }
 async function request(path,body,method='POST',authenticated=false){
  if(!available)throw Error('The private service has not been connected yet.');
  if(authenticated&&(!session||session.expires_at<Date.now()))throw Error('Please sign in again.');
  const response=await fetch(config.url+path,{method,headers:{apikey:config.publishableKey,Authorization:'Bearer '+(authenticated?session.access_token:config.publishableKey),'Content-Type':'application/json',Prefer:'return=representation'},body:body===undefined?undefined:JSON.stringify(body)});
  if(!response.ok)throw Error(response.status===401||response.status===403?'Access denied. Please sign in with the correct account.':'The request could not be completed. Please try again.');
  const raw=await response.text();return raw?JSON.parse(raw):null;
 }
 async function login(email){
  if(!email||!email.includes('@'))throw Error('Enter your email address.');
  await request('/auth/v1/otp?redirect_to='+encodeURIComponent(location.origin+location.pathname),{email,create_user:true});
 }
 function logout(){session=null;try{sessionStorage.removeItem(authKey);}catch{}location.reload();}
 function el(tag,text){const n=document.createElement(tag);if(text!==undefined)n.textContent=String(text);return n;}
 window.PrivateSite={available,request,login,logout,el,signedIn:()=>!!session&&session.expires_at>Date.now()};
 document.dispatchEvent(new Event('private-site-ready'));
 if(/^\/post-[a-z0-9-]+\.html$/.test(location.pathname)){
  const box=el('section');box.className='private-messages';box.id='private-messages';
  box.append(el('h2','Private messages'),el('p','Only you and Wang Shuoxuan can read your messages and his replies.'));
  if(!available){box.append(el('p','Private messaging is not available yet.'));}
  else{
   const status=el('p');status.setAttribute('role','status');const form=el('form');
   const label=el('label','Email address'),email=el('input');email.type='email';email.required=true;email.autocomplete='email';label.append(email);
   const sign=el('button','Email me a sign-in link');sign.type='submit';form.append(label,sign);
   form.addEventListener('submit',async e=>{e.preventDefault();sign.disabled=true;try{await login(email.value.trim());status.textContent='Check your email. Open the sign-in link in this browser.';}catch(error){status.textContent=error.message;}finally{sign.disabled=false;}});
   box.append(form,status);const thread=el('div');box.append(thread);
   async function load(){
    const rows=await request('/rest/v1/reader_messages?select=id,body,created_at,reply,replied_at&post_path=eq.'+encodeURIComponent(location.pathname)+'&order=created_at.desc&limit=100',undefined,'GET',true);
    thread.replaceChildren();for(const row of rows){const item=el('article');item.append(el('small',new Date(row.created_at).toLocaleString()),el('p',row.body));if(row.reply)item.append(el('strong','Wang Shuoxuan'),el('p',row.reply));thread.append(item);}
   }
   if(window.PrivateSite.signedIn()){
    form.hidden=true;const compose=el('form'),messageLabel=el('label','Your private message'),message=el('textarea');message.required=true;message.maxLength=5000;message.rows=5;messageLabel.append(message);
    const send=el('button','Send privately');send.type='submit';const out=el('button','Sign out');out.type='button';out.onclick=logout;compose.append(messageLabel,send,out);box.append(compose);
    compose.onsubmit=async e=>{e.preventDefault();send.disabled=true;try{await request('/rest/v1/reader_messages',{post_path:location.pathname,body:message.value.trim()},'POST',true);message.value='';status.textContent='Message sent privately.';await load();}catch(error){status.textContent=error.message;}finally{send.disabled=false;}};
    load().catch(error=>status.textContent=error.message);
   }
  }
  document.querySelector('main')?.insertBefore(box,document.querySelector('main>footer'));
 }
 // Anonymous tab-scoped session estimates. No URL query/hash or private content is sent.
 if(!available||location.pathname.includes('/admin/')||navigator.doNotTrack==='1'||navigator.globalPrivacyControl||!/^\/(?:[a-zA-Z0-9_-]+\.html)?$/.test(location.pathname))return;
 let sid=crypto.randomUUID(),id=crypto.randomUUID(),active=0,scroll=0,last=Date.now(),interaction=Date.now();
 try{const old=JSON.parse(sessionStorage.getItem('site-visit-session')||'null');if(old&&Date.now()-old.time<1800000)sid=old.id;sessionStorage.setItem('site-visit-session',JSON.stringify({id:sid,time:Date.now()}));}catch{}
 const device=innerWidth<640?'mobile':innerWidth<1024?'tablet':'desktop';let ref='';try{ref=document.referrer?new URL(document.referrer).hostname:'';}catch{}
 function tick(){const now=Date.now();if(document.visibilityState==='visible'&&document.hasFocus()&&now-interaction<90000)active+=Math.min(now-last,15000);last=now;const size=document.documentElement.scrollHeight-innerHeight;scroll=Math.max(scroll,size>0?Math.min(100,Math.round(scrollY/size*100)):100);}
 function report(){tick();request('/rest/v1/rpc/record_site_visit',{p_id:id,p_session:sid,p_path:location.pathname,p_referrer:ref,p_device:device,p_active:Math.round(active),p_scroll:scroll}).catch(()=>{});try{sessionStorage.setItem('site-visit-session',JSON.stringify({id:sid,time:Date.now()}));}catch{}}
 for(const type of ['pointerdown','keydown','scroll','touchstart'])addEventListener(type,()=>interaction=Date.now(),{passive:true});
 setInterval(tick,5000);setInterval(report,30000);document.addEventListener('visibilitychange',report);addEventListener('pagehide',report);report();
})();
