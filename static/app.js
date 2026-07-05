function toast(msg) {
  let el = document.querySelector('.toast');
  if (!el) {
    el = document.createElement('div');
    el.className = 'toast';
    document.body.appendChild(el);
  }
  el.textContent = msg;
  el.classList.add('show');
  clearTimeout(el._t);
  el._t = setTimeout(() => el.classList.remove('show'), 3000);
}

async function api(url, options = {}) {
  const opts = Object.assign({ headers: { 'Content-Type': 'application/json' } }, options);
  if (opts.body && typeof opts.body !== 'string') opts.body = JSON.stringify(opts.body);
  const res = await fetch(url, opts);
  let data = null;
  try { data = await res.json(); } catch (e) { /* no body */ }
  if (!res.ok) {
    throw new Error((data && data.error) || 'Something went wrong');
  }
  return data;
}

/* ─── CUSTOM CURSOR ──────────────────────────────── */
(function() {
  const cursor = document.getElementById('cursor');
  if (!cursor) return;
  let cx = -100, cy = -100;
  let rafId = null;

  window.addEventListener('mousemove', (e) => {
    cx = e.clientX;
    cy = e.clientY;
    if (!rafId) {
      rafId = requestAnimationFrame(() => {
        cursor.style.left = cx + 'px';
        cursor.style.top  = cy + 'px';
        rafId = null;
      });
    }
  }, { passive: true });

  document.addEventListener('mouseover', (e) => {
    const target = e.target.closest('a, button, [role="button"], input, select, textarea, .chat-fab, .nav-item');
    if (target) {
      cursor.classList.add('hover');
    }
  });

  document.addEventListener('mouseout', (e) => {
    const target = e.target.closest('a, button, [role="button"], input, select, textarea, .chat-fab, .nav-item');
    if (target) {
      cursor.classList.remove('hover');
    }
  });
})();
