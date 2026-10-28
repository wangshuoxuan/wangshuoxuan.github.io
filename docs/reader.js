/* Article language is independent of the surrounding website language. */
(() => {
  'use strict';
  const root=document.body;
  const controls=document.querySelector('.reading-controls');
  if(!controls)return;
  function setView(view,announce=false) {
    if(!['en','zh','both'].includes(view))view='en';
    root.dataset.reading=view;
    document.querySelectorAll('.post-en').forEach(node=>{node.hidden=view==='zh';});
    document.querySelectorAll('.post-zh').forEach(node=>{node.hidden=view==='en';});
    document.querySelectorAll('[data-bilingual-only]').forEach(node=>{node.hidden=view!=='both';});
    controls.querySelectorAll('button[data-reading]').forEach(button=>{
      button.setAttribute('aria-pressed',String(button.dataset.reading===view));
    });
    if(announce)root.dispatchEvent(new CustomEvent('reading-language',{detail:view}));
  }
  controls.querySelectorAll('button[data-reading]').forEach(button=>{
    button.addEventListener('click',()=>setView(button.dataset.reading,true));
  });
  setView('en');
  // Browser back/forward caches can retain a previous mode and hidden attributes.
  addEventListener('pageshow',event=>{if(event.persisted)setView('en');});
})();
