// Marin Spec behavior: one step at a time, the current-step marker, and Copy
// prompt. The shell owns routing, menus, and the shared copy helper. Prompt text
// lives in prompts/*.md and is copied into index.html by scripts/sync-prompts.py;
// this file never holds prompt text or project content.

document.addEventListener('DOMContentLoaded', () => {
  // The shell's toggle for the steps column and the current-step line do nothing without JavaScript.
  document.querySelectorAll('.filter-toggle, .spec-progress').forEach((element) => { element.hidden = false; });

  const STEPS = ['prepare', 'analyze', 'resolve', 'spec', 'review', 'build'];

  // One step at a time. Without JavaScript every step stays on the page and the
  // step links jump down to them.
  const stepLinks = new Map();
  document.querySelectorAll('.spec-steps a').forEach((link) => {
    stepLinks.set(link.getAttribute('href').slice(1), link);
  });

  // Give each box an id (its step plus its heading) so the "On this page" list can link to it.
  const slug = (text) => text.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
  STEPS.forEach((step) => {
    document.querySelectorAll('#' + step + ' .spec-box').forEach((box) => {
      const heading = box.querySelector('h3');
      if (heading && !box.id) box.id = step + '-' + slug(heading.textContent);
    });
  });

  // "On this page": the boxes of the current step, rebuilt when the step changes. The shell marks the one being read.
  const tocHolder = document.querySelector('.spec-toc-holder');
  let tocStep = null;
  function buildToc(step) {
    if (!tocHolder || tocStep === step) return;
    tocStep = step;
    tocHolder.textContent = '';
    const boxes = Array.from(document.querySelectorAll('#' + step + ' .spec-box[id]'));
    if (boxes.length < 2) return;
    const nav = document.createElement('nav');
    nav.className = 'toc spec-toc';
    nav.setAttribute('aria-label', 'On this page');
    const title = document.createElement('h2');
    title.textContent = 'On this page';
    const list = document.createElement('ul');
    boxes.forEach((box) => {
      const item = document.createElement('li');
      const link = document.createElement('a');
      link.href = '#' + box.id;
      link.textContent = box.querySelector('h3').textContent;
      item.append(link);
      list.append(item);
    });
    nav.append(title, list);
    tocHolder.append(nav);
    if (window.marinOnThisPage) window.marinOnThisPage(nav);
  }

  // A hash can name a step or a box inside one.
  function stepOfHash(hash) {
    if (stepLinks.has(hash)) return hash;
    const target = hash ? document.getElementById(hash) : null;
    const section = target && target.closest('.spec-step');
    return section ? section.id : STEPS[0];
  }

  function showStep(id, moveFocus) {
    if (!stepLinks.has(id)) id = STEPS[0];
    STEPS.forEach((step) => {
      const section = document.getElementById(step);
      if (section) section.hidden = step !== id;
      const link = stepLinks.get(step);
      if (step === id) link.setAttribute('aria-current', 'step');
      else link.removeAttribute('aria-current');
    });
    const parts = stepLinks.get(id).textContent.match(/^(\d+)\. (.+)$/);
    buildToc(id);
    document.querySelector('.spec-progress').textContent = 'Step ' + parts[1] + ' of ' + STEPS.length + ': ' + parts[2];
    if (!moveFocus) return;
    const heading = document.querySelector('#' + id + ' > h2');
    heading.tabIndex = -1;
    heading.focus();
    heading.scrollIntoView({ block: 'start' });
  }

  function goToStep(id) {
    const url = new URL(window.location.href);
    url.hash = id;
    window.history.pushState(null, '', url);
    showStep(id, true);
  }

  document.querySelectorAll('.spec-steps a').forEach((link) => {
    link.addEventListener('click', (event) => {
      event.preventDefault();
      goToStep(link.getAttribute('href').slice(1));
    });
  });

  // Previous and Next buttons stay hidden without JavaScript, where the step links do the work.
  document.querySelectorAll('[data-next-step], [data-prev-step]').forEach((button) => {
    button.hidden = false;
    button.addEventListener('click', () => goToStep(button.dataset.nextStep || button.dataset.prevStep));
  });

  window.addEventListener('popstate', () => showStep(stepOfHash(window.location.hash.slice(1)), false));
  showStep(stepOfHash(window.location.hash.slice(1)), false);
  const firstTarget = window.location.hash.length > 1 ? document.getElementById(window.location.hash.slice(1)) : null;
  if (firstTarget && firstTarget.classList.contains('spec-box')) firstTarget.scrollIntoView();

  // Copy prompt: the button stays hidden without JavaScript; the prompt text is
  // always on the page to select by hand.
  document.querySelectorAll('[data-copy-prompt]').forEach((button) => {
    button.hidden = false;
    const status = button.closest('.spec-prompt').querySelector('.spec-prompt__status');
    let timer;
    button.addEventListener('click', async () => {
      const source = document.getElementById(button.dataset.copyPrompt);
      const ok = await window.marinCopyText(source.textContent);
      status.textContent = ok ? 'Copied. Paste it into your AI tool.' : 'Copy did not work. Select the prompt text and copy it by hand.';
      clearTimeout(timer);
      timer = setTimeout(() => { status.textContent = ''; }, 6000);
    });
  });
});
