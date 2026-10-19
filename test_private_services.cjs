const assert = require('node:assert/strict');
const vm = require('node:vm');
const fs = require('node:fs');
const source = fs.readFileSync('docs/site-services.js', 'utf8');
function run(path,config={enabled:false,url:'',publishableKey:''}) {
 let network=0,callbacks=0;const appended=[];
 const node=()=>({append(){},setAttribute(){},className:'',id:''});
 const context={window:{SITE_SERVICES:config},sessionStorage:{getItem(){return null},setItem(){},removeItem(){}},location:{pathname:path,hash:'',search:'',origin:'https://example.com'},document:{createElement:node,dispatchEvent(){},querySelector(selector){return selector==='main'?{insertBefore(box){appended.push(box)}}:null;}},URLSearchParams,Date,JSON,Event:class{},fetch(){network++;throw Error('unexpected network')},setInterval(){callbacks++;},history:{replaceState(){}}};
 vm.runInNewContext(source,context);
 return {context,network,callbacks,appended};
}
for(const path of ['/','/post-test.html','/admin/insights.html']){
 const r=run(path);assert.equal(r.context.window.PrivateSite.available,false);assert.equal(r.network,0);assert.equal(r.callbacks,0);
}
assert.equal(run('/post-test.html').appended.length,1);
assert.equal(run('/').appended.length,0);
assert.equal(run('/',{enabled:true,url:'http://untrusted.invalid',publishableKey:'test'}).context.window.PrivateSite.available,false);
console.log('Disabled/misconfigured services fail closed: no network calls or collection timers.');
