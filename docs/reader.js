/* Each visit starts in English; a reader's earlier choice never overrides it. */
(() => {
  'use strict';
  const root = document.body;
  document.querySelectorAll('[data-reading]').forEach(button => {
    if (button.tagName !== 'BUTTON') return;
    button.addEventListener('click', () => {
      const view = button.dataset.reading;
      if (!['en', 'zh', 'both'].includes(view)) return;
      root.dataset.reading = view;
      document.documentElement.lang = view === 'zh' ? 'zh-CN' : 'en';
      document.querySelectorAll('.post-en').forEach(e => { e.hidden = view === 'zh'; });
      document.querySelectorAll('.post-zh').forEach(e => { e.hidden = view === 'en'; });
      document.querySelectorAll('button[data-reading]').forEach(e => e.setAttribute('aria-pressed', String(e === button)));
      root.dispatchEvent(new CustomEvent('reading-language', { detail: view }));
    });
  });
})();
