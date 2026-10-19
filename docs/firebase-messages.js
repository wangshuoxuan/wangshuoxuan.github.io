/* Reader identities persist in this browser. Firestore rules enforce isolation. */
(async () => {
 'use strict';
 const config=window.FIREBASE_MESSAGES;
 const ownerPage=location.pathname==='/admin/messages.html';
 const postPath=location.pathname.replace(/-en(?=\.html$)/,'');
 if(!config?.app?.apiKey||(!config.enabled&&!ownerPage))return;
 if(!ownerPage&&!/^\/post-[a-z0-9-]+\.html$/.test(location.pathname))return;
 const zh=!ownerPage&&document.documentElement.lang==='zh-CN';
 const translations={
  'Private messages':'给我留言',
  'Only you and Wang Shuoxuan can read this conversation. No registration is needed.':'这段对话仅你和王烁瑄可见，无需注册。',
  'Return in the same browser on this device to see replies. Private browsing or clearing site data can lose access. Anyone using this browser profile may also see this conversation.':'请用这台设备的同一浏览器回来查看回复。无痕浏览或清除网站数据可能导致无法找回；共用同一浏览器配置的人也可能看到这段对话。',
  'Connecting…':'正在连接…','Refresh':'刷新回复','Sign out':'退出登录',
  'Your private message':'你的留言','Send privately':'发送留言',
  'Load older messages':'查看更早的留言','Wang Shuoxuan':'王烁瑄',
  'No messages yet.':'尚无留言，欢迎写下你的想法。',
  'Your private messages are loaded.':'已显示你的留言及回复。',
  'Messages could not be loaded. Please try again.':'未能加载对话，请重试。',
  'Message sent privately.':'留言已发送。你可以在这里查看回复。',
  'Message not sent. Please wait at least a minute between messages and check your connection.':'暂未发送。内容仍保留，请检查网络，并在两次留言之间至少间隔一分钟。',
  'Private messaging could not connect. Your text has not been sent. Please retry later.':'暂时无法连接，内容尚未发送，请稍后重试。',
  'Retry connection':'重新连接','Sending…':'正在发送…',
  'This browser cannot securely remember this conversation. Please enable website storage and retry.':'此浏览器暂时无法保存对话身份，请允许网站存储后重试。'
 };
 const tr=text=>zh?(translations[text]||text):text;
 const el=(tag,text,raw=false)=>{const n=document.createElement(tag);if(text!==undefined)n.textContent=raw?text:tr(text);return n;};
 let box=document.getElementById(ownerPage?'message-app':'private-messages');
 if(!box){box=el('section');box.className='private-messages';box.id='private-messages';const main=document.querySelector('main');main.insertBefore(box,main.querySelector('footer'));}
 box.replaceChildren(el('h2',ownerPage?'Private inbox':'Private messages'),el('p',ownerPage?'Sign in with your owner account to view and reply to all private messages.':'Only you and Wang Shuoxuan can read this conversation. No registration is needed.'));
 const status=el('p','Connecting…');status.setAttribute('role','status');box.append(status);
 const setStatus=text=>{status.textContent=tr(text);};
 const controls=el('div'),thread=el('div');thread.setAttribute('aria-live','polite');box.append(controls);
 const retry=el('button','Retry connection');retry.type='button';retry.hidden=true;controls.append(retry);
 const compose=el('form'),label=el('label','Your private message'),text=el('textarea'),send=el('button','Send privately');
 text.rows=5;text.required=true;text.maxLength=5000;text.name='message';text.autocomplete='off';label.append(text);send.type='submit';send.disabled=true;compose.append(label,send);compose.hidden=ownerPage;
 if(!ownerPage){box.append(compose);const note=el('p','Return in the same browser on this device to see replies. Private browsing or clearing site data can lose access. Anyone using this browser profile may also see this conversation.');note.className='message-storage-note';box.append(note);}
 box.append(thread);
 const more=el('button','Load older messages');more.type='button';more.hidden=true;box.append(more);
 let initializing=false,ready=false,authSDK,dbSDK,auth,db,unsubscribe=null,cursor=null,readerRows=[],readerCount=50;
 function unavailable(error){send.disabled=true;retry.hidden=false;setStatus(error?.code==='auth/web-storage-unsupported'?'This browser cannot securely remember this conversation. Please enable website storage and retry.':'Private messaging could not connect. Your text has not been sent. Please retry later.');}
 function render(entries,append=false){
  if(!append)thread.replaceChildren();
  for(const entry of entries){
   const row=entry.data(),item=el('article');item.className='message';
   item.append(el('small',(ownerPage?row.post_path+' · ':'')+(row.created_at?.toDate().toLocaleString()||'')),el('p',row.body,true));
   if(ownerPage){const replyLabel=el('label','Private reply'),reply=el('textarea'),save=el('button','Save private reply');reply.rows=3;reply.maxLength=5000;reply.value=row.reply||'';replyLabel.append(reply);save.type='button';save.onclick=async()=>{save.disabled=true;try{await dbSDK.updateDoc(entry.ref,{reply:reply.value.trim(),replied_at:dbSDK.serverTimestamp()});setStatus('Reply saved privately.');}catch{setStatus('Reply could not be saved. Check the owner account and connection.');}finally{save.disabled=false;}};item.append(replyLabel,save);}
   else if(row.reply)item.append(el('strong','Wang Shuoxuan'),el('p',row.reply,true));
   thread.append(item);
  }
 }
 function renderReader(){render(readerRows.slice(-readerCount));more.hidden=readerRows.length<=readerCount;}
 async function loadOwner(reset=true){
  if(!auth.currentUser||auth.currentUser.isAnonymous)return;
  if(reset){thread.replaceChildren();cursor=null;}
  const filters=[dbSDK.orderBy('created_at','desc')];if(cursor)filters.push(dbSDK.startAfter(cursor));filters.push(dbSDK.limit(50));
  const data=await dbSDK.getDocs(dbSDK.query(dbSDK.collection(db,'reader_messages'),...filters));render(data.docs,!reset);cursor=data.docs.at(-1)||cursor;more.hidden=data.size<50;setStatus(data.empty&&reset?'No messages yet.':'Private inbox loaded.');
 }
 function watchReader(user){
  unsubscribe?.();readerCount=50;readerRows=[];
  const q=dbSDK.query(dbSDK.collection(db,'reader_messages'),dbSDK.where('uid','==',user.uid),dbSDK.where('post_path','==',postPath));
  unsubscribe=dbSDK.onSnapshot(q,data=>{readerRows=data.docs.slice().sort((a,b)=>(a.data().created_at?.toMillis()||0)-(b.data().created_at?.toMillis()||0));renderReader();setStatus(data.empty?'No messages yet.':'Your private messages are loaded.');},()=>{setStatus('Messages could not be loaded. Please try again.');unsubscribe?.();unsubscribe=null;retry.hidden=false;});
 }
 async function ensureReader(){
  if(!auth.currentUser)await authSDK.signInAnonymously(auth);
  send.disabled=!auth.currentUser;
 }
 async function initialize(){
  if(initializing)return;initializing=true;retry.hidden=true;setStatus('Connecting…');
  try{
   if(!ready){
    const modules=await Promise.all(['app','auth','firestore'].map(n=>import('https://www.gstatic.com/firebasejs/13.0.0/firebase-'+n+'.js')));
    const appSDK=modules[0];authSDK=modules[1];dbSDK=modules[2];
    const app=appSDK.getApps().find(a=>a.name==='[DEFAULT]')||appSDK.initializeApp(config.app);auth=authSDK.getAuth(app);db=dbSDK.getFirestore(app);
    await authSDK.setPersistence(auth,ownerPage?authSDK.browserSessionPersistence:authSDK.browserLocalPersistence);
    await auth.authStateReady();
    if(ownerPage){
     const login=el('button','Continue with Google'),refresh=el('button','Refresh'),logout=el('button','Sign out');login.type=refresh.type=logout.type='button';
     login.onclick=async()=>{login.disabled=true;try{await authSDK.signInWithPopup(auth,new authSDK.GoogleAuthProvider());}catch{setStatus('Sign-in could not be completed. Please try again or allow the sign-in popup.');}finally{login.disabled=false;}};
     refresh.onclick=()=>loadOwner().catch(()=>setStatus('Access denied or unavailable. Use the owner account.'));logout.onclick=()=>authSDK.signOut(auth);controls.append(login,refresh,logout);
     authSDK.onAuthStateChanged(auth,user=>{thread.replaceChildren();const signed=!!user&&!user.isAnonymous;login.hidden=signed;refresh.hidden=logout.hidden=!signed;more.hidden=true;if(signed)loadOwner().catch(()=>setStatus('Access denied or unavailable. Use the owner account.'));else setStatus('Sign in with the owner account.');});
    }else{
     authSDK.onAuthStateChanged(auth,user=>{unsubscribe?.();unsubscribe=null;send.disabled=!user;thread.replaceChildren();if(user)watchReader(user);});
    }
    ready=true;
   }
   if(!ownerPage){await ensureReader();if(auth.currentUser&&!unsubscribe)watchReader(auth.currentUser);}
  }catch(error){unavailable(error);}finally{initializing=false;}
 }
 retry.onclick=initialize;
 more.onclick=()=>{if(ownerPage)loadOwner(false).catch(()=>setStatus('Messages could not be loaded. Please try again.'));else{readerCount+=50;renderReader();}};
 compose.onsubmit=async e=>{
  e.preventDefault();if(!auth?.currentUser||!text.value.trim())return;
  send.disabled=true;send.textContent=tr('Sending…');
  try{const batch=dbSDK.writeBatch(db);batch.set(dbSDK.doc(dbSDK.collection(db,'reader_messages')),{uid:auth.currentUser.uid,post_path:postPath,body:text.value.trim(),created_at:dbSDK.serverTimestamp()});batch.set(dbSDK.doc(db,'message_limits',auth.currentUser.uid),{last_message:dbSDK.serverTimestamp()});await batch.commit();text.value='';setStatus('Message sent privately.');}
  catch{setStatus('Message not sent. Please wait at least a minute between messages and check your connection.');}
  finally{send.disabled=!auth?.currentUser;send.textContent=tr('Send privately');}
 };
 await initialize();
})();
