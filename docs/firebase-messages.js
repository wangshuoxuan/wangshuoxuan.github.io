/* Authenticated private messages. Database rules, not this UI, enforce access. */
(async () => {
 'use strict';
 const config=window.FIREBASE_MESSAGES;
 const ownerPage=location.pathname==='/admin/messages.html';
 if(!config?.app?.apiKey||(!config.enabled&&!ownerPage))return;
 if(!ownerPage&&!/^\/post-[a-z0-9-]+\.html$/.test(location.pathname))return;
 const el=(tag,text)=>{const n=document.createElement(tag);if(text!==undefined)n.textContent=text;return n;};
 let box=ownerPage?document.getElementById('message-app'):document.getElementById('private-messages');
 if(!box){box=el('section');box.className='private-messages';document.querySelector('main').append(box);}
 box.replaceChildren(el('h2',ownerPage?'Private inbox':'Private messages'),el('p','Only you and Wang Shuoxuan can read your messages and his replies. Google sign-in is required.'));
 const status=el('p','Connecting…');status.setAttribute('role','status');box.append(status);
 try{
  const [appSDK,authSDK,dbSDK]=await Promise.all(['app','auth','firestore'].map(n=>import('https://www.gstatic.com/firebasejs/13.0.0/firebase-'+n+'.js')));
  const app=appSDK.initializeApp(config.app),auth=authSDK.getAuth(app),db=dbSDK.getFirestore(app);
  await authSDK.setPersistence(auth,authSDK.browserSessionPersistence);
  const controls=el('div'),thread=el('div');box.append(controls,thread);
  const login=el('button','Continue with Google');login.type='button';login.onclick=async()=>{login.disabled=true;try{await authSDK.signInWithPopup(auth,new authSDK.GoogleAuthProvider());}catch{status.textContent='Sign-in could not be completed. Please try again or allow the sign-in popup.';}finally{login.disabled=false;}};
  const refresh=el('button','Refresh'),logout=el('button','Sign out');logout.onclick=()=>authSDK.signOut(auth);controls.append(login,refresh,logout);
  const compose=el('form'),label=el('label','Your private message'),text=el('textarea'),send=el('button','Send privately');text.rows=5;text.required=true;text.maxLength=5000;label.append(text);compose.append(label,send);box.append(compose);
  let cursor=null;
  const more=el('button','Load older messages');more.hidden=true;box.append(more);
  async function load(reset=true){
   if(!auth.currentUser)return;
   if(reset){thread.replaceChildren();cursor=null;}
   const filters=ownerPage?[dbSDK.orderBy('created_at','desc')]:[dbSDK.where('uid','==',auth.currentUser.uid),dbSDK.where('post_path','==',location.pathname)];
   if(cursor)filters.push(dbSDK.startAfter(cursor));filters.push(dbSDK.limit(50));
   const data=await dbSDK.getDocs(dbSDK.query(dbSDK.collection(db,'reader_messages'),...filters));
   for(const entry of data.docs){const row=entry.data(),item=el('article');item.className='message';item.append(el('small',(ownerPage?row.post_path+' · ':'')+(row.created_at?.toDate().toLocaleString()||'')),el('p',row.body));
    if(ownerPage){const replyLabel=el('label','Private reply'),reply=el('textarea'),save=el('button','Save private reply');reply.rows=3;reply.maxLength=5000;reply.value=row.reply||'';replyLabel.append(reply);save.onclick=async()=>{save.disabled=true;try{await dbSDK.updateDoc(entry.ref,{reply:reply.value.trim(),replied_at:dbSDK.serverTimestamp()});status.textContent='Reply saved privately.';}catch{status.textContent='Reply could not be saved. Check the owner account and connection.';}finally{save.disabled=false;}};item.append(replyLabel,save);}
    else if(row.reply)item.append(el('strong','Wang Shuoxuan'),el('p',row.reply));thread.append(item);
   }
   cursor=data.docs.at(-1)||cursor;more.hidden=data.size<50;
   status.textContent=data.empty&&reset?'No messages yet.':ownerPage?'Private inbox loaded.':'Your private messages are loaded.';
  }
  const safeLoad=reset=>load(reset).catch(()=>{status.textContent=ownerPage?'Access denied or unavailable. Use the owner account.':'Messages could not be loaded. Please try again.';});
  refresh.onclick=()=>safeLoad(true);more.onclick=()=>safeLoad(false);
  compose.onsubmit=async e=>{e.preventDefault();if(!auth.currentUser||!text.value.trim())return;send.disabled=true;try{const batch=dbSDK.writeBatch(db);batch.set(dbSDK.doc(dbSDK.collection(db,'reader_messages')),{uid:auth.currentUser.uid,post_path:location.pathname,body:text.value.trim(),created_at:dbSDK.serverTimestamp()});batch.set(dbSDK.doc(db,'message_limits',auth.currentUser.uid),{last_message:dbSDK.serverTimestamp()});await batch.commit();text.value='';await load();status.textContent='Message sent privately.';}catch{status.textContent='Message not sent. Please wait at least a minute between messages and check your connection.';}finally{send.disabled=false;}};
  authSDK.onAuthStateChanged(auth,user=>{thread.replaceChildren();login.hidden=!!user;logout.hidden=!user;refresh.hidden=!user;compose.hidden=!user||ownerPage;more.hidden=true;if(user){status.textContent=ownerPage?'Signed in. Checking inbox access…':'Signed in.';if(ownerPage){const uid=el('small','Account ID: '+user.uid);controls.querySelector('small')?.remove();controls.append(uid);}safeLoad(true);}else status.textContent='Sign in to view and send private messages.';});
 }catch{status.textContent='Private messaging could not connect. Please try again later.';}
})();
