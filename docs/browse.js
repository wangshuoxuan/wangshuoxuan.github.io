(() => {
  const controls = document.querySelector('.filters');
  if (!controls) return;
  const entries = [...document.querySelectorAll('[data-entry]')];
  const selects = [...controls.querySelectorAll('select')];
  const en = document.documentElement.lang === 'en';
  function update() {
    let count = 0;
    entries.forEach(entry => {
      const matches = selects.every(select => !select.value ||
        (select.dataset.filter === 'subject'
          ? entry.dataset.subject.split(' ').includes(select.value)
          : entry.dataset[select.dataset.filter] === select.value));
      entry.hidden = !matches;
      if (matches) count++;
    });
    document.querySelector('[data-count]').textContent = `${count} ${en ? 'entries' : '条内容'}`;
    document.querySelector('[data-empty]').hidden = count > 0;
  }
  controls.hidden = false;
  selects.forEach(select => select.addEventListener('change', update));
  controls.querySelector('[data-reset]').addEventListener('click', () => {
    selects.forEach(select => { select.value = ''; });
    update();
  });
  update();
})();
