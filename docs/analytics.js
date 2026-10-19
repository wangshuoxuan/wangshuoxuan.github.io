/* Public website ID, not an account credential. No form or message contents are tracked. */
(() => {
 'use strict';
 if(location.hostname!=='wangshuoxuan.github.io'||location.pathname.startsWith('/admin/')||navigator.doNotTrack==='1'||navigator.globalPrivacyControl)return;
 try{if(localStorage.getItem('umami.disabled'))return;}catch{}
 window.cleanAnalyticsPayload=(type,payload)=>{
  if(payload.url){try{const u=new URL(payload.url,location.origin);payload.url=u.origin+u.pathname;}catch{return false;}}
  if(payload.referrer){try{payload.referrer=new URL(payload.referrer).origin;}catch{payload.referrer='';}}
  return payload;
 };
 const script=document.createElement('script');script.src='https://cloud.umami.is/script.js';script.defer=true;
 script.dataset.websiteId='96e0ff79-f76f-4bcf-bf0c-1532d3550f36';script.dataset.domains='wangshuoxuan.github.io';script.dataset.excludeSearch='true';script.dataset.excludeHash='true';script.dataset.doNotTrack='true';script.dataset.beforeSend='cleanAnalyticsPayload';document.head.append(script);
 if(!location.pathname.startsWith('/post-'))return;
 const sent=new Set();let active=0,lastInput=Date.now();
 function event(name,data){if(window.umami?.track)window.umami.track(name,data);}
 ['pointerdown','keydown','scroll'].forEach(name=>addEventListener(name,()=>{lastInput=Date.now();},{passive:true}));
 setInterval(()=>{if(document.visibilityState!=='visible'||!document.hasFocus()||Date.now()-lastInput>90000)return;active+=5;for(const seconds of [30,60,180,300])if(active>=seconds&&!sent.has(seconds)&&window.umami?.track){sent.add(seconds);event('active-reading',{seconds});}},5000);
 addEventListener('scroll',()=>{const height=document.documentElement.scrollHeight-innerHeight;if(height<=0)return;const depth=Math.round(scrollY/height*100);for(const mark of [50,90])if(depth>=mark&&!sent.has('scroll'+mark)&&window.umami?.track){sent.add('scroll'+mark);event('reading-depth',{percent:mark});}},{passive:true});
 document.body.addEventListener('reading-language',e=>{if(['en','zh','both'].includes(e.detail))event('reading-language',{language:e.detail});});
})();
