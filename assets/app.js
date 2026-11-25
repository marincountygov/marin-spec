// Marin Spec behavior: Copy prompt. The shell owns the steps (`nav[data-steps]`: one step at a time, the state
// words, the progress line, "On this page", Previous and Next), routing, menus, and the shared copy helper.
// Prompt text lives in prompts/*.md and is copied into index.html by scripts/sync-prompts.py; this file never
// holds prompt text or project content.

document.addEventListener('DOMContentLoaded', () => {
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
