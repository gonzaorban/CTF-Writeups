/* index.js
   Small UX helper to:
   - Validate the login form client-side (nice UX only)
   - Show a playful "training mode" toggle (reveals a hint)
   - Add a tiny shake animation when login fails (based on server hint element)
   - Small "typing" effect for hero subtitle
*/

document.addEventListener('DOMContentLoaded', () => {
  // Basic form validation & friendly UX
  const form = document.querySelector('form');
  if (form) {
    const user = form.querySelector('input[name="username"]');
    const pass = form.querySelector('input[name="password"]');
    const btn  = form.querySelector('button[type="submit"]');

    // Prevent empty submissions (client-side only; server still validates)
    form.addEventListener('submit', (e) => {
      if (!user.value.trim() || !pass.value.trim()) {
        e.preventDefault();
        flashAlert('Please fill both fields before attempting to log in.');
        animateShake(form);
      } else {
        // optional: disable button for a short moment to show "working"
        btn.disabled = true;
        btn.style.opacity = '0.9';
        btn.textContent = 'Checking...';
      }
    });

    // simple enter key UX on username to jump to password
    user.addEventListener('keydown', (ev) => {
      if (ev.key === 'Enter') {
        ev.preventDefault();
        pass.focus();
      }
    });
  }

  // Reveal training hint toggle (non-destructive)
  const hintToggle = document.getElementById('hint-toggle');
  if (hintToggle) {
    hintToggle.addEventListener('click', () => {
      const hintBox = document.getElementById('hint-box');
      if (!hintBox) return;
      hintBox.classList.toggle('visible');
      hintToggle.textContent = hintBox.classList.contains('visible') ? 'Hide hint' : 'Show hint';
    });
  }

  // If server printed an element with id="login-failed", show shake
  const failedEl = document.getElementById('login-failed');
  if (failedEl) {
    const formElem = document.querySelector('form') || failedEl;
    animateShake(formElem);
  }

  // Hero typing effect (for the left panel subtitle if it exists)
  const heroSub = document.querySelector('.h-sub');
  if (heroSub) {
    const fullText = heroSub.getAttribute('data-full') || heroSub.textContent;
    heroSub.textContent = '';
    typeText(heroSub, fullText, 25);
  }

  // Utility functions
  function flashAlert(text) {
    // show a small temporary message under the form
    let a = document.createElement('div');
    a.className = 'alert';
    a.textContent = text;
    const container = document.querySelector('.login-box') || document.body;
    container.prepend(a);
    setTimeout(() => {
      a.style.transition = 'opacity 350ms';
      a.style.opacity = '0';
      setTimeout(() => a.remove(), 400);
    }, 2500);
  }

  function animateShake(elem) {
    if (!elem) return;
    elem.animate([
      { transform: 'translateX(0px)' },
      { transform: 'translateX(-6px)' },
      { transform: 'translateX(6px)' },
      { transform: 'translateX(-4px)' },
      { transform: 'translateX(4px)' },
      { transform: 'translateX(0px)' }
    ], {
      duration: 420,
      easing: 'cubic-bezier(.36,.07,.19,.97)'
    });
  }

  function typeText(target, text, speed=40) {
    let i = 0;
    const t = setInterval(() => {
      target.textContent += text.charAt(i);
      i++;
      if (i >= text.length) clearInterval(t);
    }, speed);
  }
});