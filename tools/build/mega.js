/* The Wonder Agency: mega menu (desktop) and expanding mobile menu */
(function () {
  var nav = document.getElementById('x-nav'); if (!nav) return;
  var root = document.documentElement;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var hover = window.matchMedia && window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  var mega = nav.querySelector('.x-mega'), wrap = nav.querySelector('.x-mega-wrap');
  var veil = document.querySelector('.x-mega-veil');
  var triggers = nav.querySelectorAll('[data-mega]');
  var panels = mega ? mega.querySelectorAll('.x-mm') : [];
  var cur = null, closeT = null, openT = null, loaded = false;

  function playV(v) { if (!v) return; if (!v.getAttribute('src') && v.dataset.src) v.src = v.dataset.src; var p = v.play(); if (p && p.catch) p.catch(function () {}); }
  function loadMedia(scope) {
    scope.querySelectorAll('[data-mm-poster]').forEach(function (v) { v.setAttribute('poster', v.dataset.mmPoster); v.removeAttribute('data-mm-poster'); });
    scope.querySelectorAll('img[data-mm-src]').forEach(function (i) { i.src = i.dataset.mmSrc; i.removeAttribute('data-mm-src'); });
  }
  function warm() { if (loaded || !mega) return; loaded = true; loadMedia(mega); }

  function size(instant) {
    var p = cur && mega.querySelector('.x-mm[data-panel="' + cur + '"]'); if (!p) return;
    if (instant) { mega.classList.add('no-anim'); }
    mega.style.height = p.offsetHeight + 'px';
    if (instant) { void mega.offsetHeight; mega.classList.remove('no-anim'); }
  }
  function open(name) {
    if (!mega) return;
    clearTimeout(closeT); warm();
    var first = !cur;
    if (cur === name) return;
    cur = name;
    triggers.forEach(function (t) { var on = t.dataset.mega === name; t.classList.toggle('is-on', on); t.setAttribute('aria-expanded', on ? 'true' : 'false'); });
    panels.forEach(function (p) {
      var on = p.dataset.panel === name; p.classList.toggle('is-on', on); p.setAttribute('aria-hidden', on ? 'false' : 'true');
      p.querySelectorAll('video').forEach(function (v) { if (!on) v.pause(); });
    });
    root.classList.add('is-mega');
    size(first);
    var p = mega.querySelector('.x-mm[data-panel="' + name + '"]');
    if (name === 'services') svcSet(svcCur < 0 ? 0 : svcCur, true);
    if (name === 'ai') aiRun(p.querySelector('.x-ai'));
    p.querySelectorAll('.x-mm-cta video').forEach(playV);
  }
  function close() {
    if (!cur) return;
    root.classList.remove('is-mega');
    triggers.forEach(function (t) { t.classList.remove('is-on'); t.setAttribute('aria-expanded', 'false'); });
    var was = cur; cur = null;
    setTimeout(function () { if (cur) return; panels.forEach(function (p) { p.classList.remove('is-on'); p.setAttribute('aria-hidden', 'true'); p.querySelectorAll('video').forEach(function (v) { v.pause(); }); }); mega.style.height = '0px'; }, 320);
  }
  function soonClose() { clearTimeout(openT); clearTimeout(closeT); closeT = setTimeout(close, 220); }

  triggers.forEach(function (t) {
    t.setAttribute('aria-haspopup', 'true'); t.setAttribute('aria-expanded', 'false');
    if (hover) {
      t.addEventListener('mouseenter', function () { clearTimeout(closeT); clearTimeout(openT); warm(); openT = setTimeout(function () { open(t.dataset.mega); }, cur ? 40 : 90); });
      t.addEventListener('mouseleave', function () { clearTimeout(openT); });
    }
    // touch / pen on a wide screen: first tap opens the panel, second tap follows the link
    t.addEventListener('click', function (e) { if (!hover && cur !== t.dataset.mega) { e.preventDefault(); open(t.dataset.mega); } });
    t.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowDown' || e.key === ' ') { e.preventDefault(); open(t.dataset.mega); var f = mega.querySelector('.x-mm.is-on a'); if (f) f.focus(); }
    });
  });
  // other top-level links close any open panel when hovered
  nav.querySelectorAll('.x-nav-links > a:not([data-mega]), .x-nav-brand, .x-nav-right').forEach(function (a) { a.addEventListener('mouseenter', function () { clearTimeout(openT); if (cur) soonClose(); }); });
  if (wrap) { wrap.addEventListener('mouseenter', function () { clearTimeout(closeT); }); }
  nav.addEventListener('mouseleave', soonClose);
  nav.addEventListener('mouseenter', function () { clearTimeout(closeT); });
  if (veil) veil.addEventListener('click', close);
  if (mega) mega.addEventListener('click', function (e) { if (e.target.closest('a')) setTimeout(close, 0); });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && cur) { var t = nav.querySelector('[data-mega="' + cur + '"]'); close(); if (t) t.focus(); }
  });
  nav.addEventListener('focusout', function () { setTimeout(function () { if (cur && !nav.contains(document.activeElement)) close(); }, 0); });
  window.addEventListener('resize', function () { if (cur) size(true); });
  window.addEventListener('scroll', function () { if (cur && !nav.matches(':hover')) close(); }, { passive: true });

  // services: hovering a service swaps the preview video
  var svcItems = mega ? mega.querySelectorAll('.x-mm-item') : [], svcVids = mega ? mega.querySelectorAll('.x-mm-prev video') : [];
  var svcName = mega && mega.querySelector('.x-mm-cap b'), svcLink = mega && mega.querySelector('.x-mm-prev');
  var svcCur = -1;
  function svcSet(i, force) {
    if (i === svcCur && !force) return; svcCur = i;
    svcItems.forEach(function (it, k) { it.classList.toggle('is-on', k === i); });
    svcVids.forEach(function (v, k) { var on = k === i; v.classList.toggle('is-on', on); if (on) playV(v); else setTimeout(function () { if (svcCur !== k) v.pause(); }, 700); });
    if (svcName && svcItems[i]) { svcName.textContent = svcItems[i].querySelector('b').textContent; svcLink.href = svcItems[i].href; }
    if (svcVids[i + 1] && !svcVids[i + 1].getAttribute('src')) svcVids[i + 1].src = svcVids[i + 1].dataset.src;
  }
  svcItems.forEach(function (it, k) { it.addEventListener('mouseenter', function () { svcSet(k); }); it.addEventListener('focus', function () { svcSet(k); }); });

  // sector tiles play on hover
  if (mega) mega.querySelectorAll('.x-mm-tile').forEach(function (t) {
    var v = t.querySelector('video'); if (!v) return;
    t.addEventListener('mouseenter', function () { playV(v); });
    t.addEventListener('mouseleave', function () { v.pause(); });
  });

  // AI search visual: question types out, the assistant answers, the score counts up
  var aiTimers = [], aiLast = 0;
  function aiRun(box) {
    if (!box) return;
    var q = box.querySelector('.x-ai-type'), n = box.querySelector('.x-ai-num'), text = q.dataset.text, target = +n.dataset.n;
    if (reduce) { box.classList.add('is-static', 'is-ans', 'is-score'); q.textContent = text; n.textContent = target; return; }
    if (Date.now() - aiLast < 4000 && box.classList.contains('is-score')) return;
    aiLast = Date.now();
    aiTimers.forEach(clearTimeout); aiTimers = [];
    box.classList.remove('is-ans', 'is-score'); q.innerHTML = '<span class="x-ai-cur"></span>'; n.textContent = '0';
    var i = 0;
    (function type() {
      if (i <= text.length) { q.innerHTML = text.slice(0, i) + '<span class="x-ai-cur"></span>'; i++; aiTimers.push(setTimeout(type, 22 + Math.random() * 28)); return; }
      aiTimers.push(setTimeout(function () { q.textContent = text; box.classList.add('is-ans'); }, 350));
      aiTimers.push(setTimeout(function () {
        box.classList.add('is-score');
        var t0 = performance.now();
        (function count(t) { var p = Math.min(1, (t - t0) / 1500), e = 1 - Math.pow(1 - p, 3); n.textContent = Math.round(target * e); if (p < 1) requestAnimationFrame(count); })(t0);
      }, 1300));
    })();
  }

  // mobile: expanding sections
  var menu = document.getElementById('x-menu');
  document.querySelectorAll('.x-mi [data-mi]').forEach(function (b) {
    b.addEventListener('click', function () {
      var item = b.closest('.x-mi'), on = !item.classList.contains('is-open');
      document.querySelectorAll('.x-mi.is-open').forEach(function (o) { if (o !== item) { o.classList.remove('is-open'); o.querySelector('[data-mi]').setAttribute('aria-expanded', 'false'); } });
      item.classList.toggle('is-open', on); b.setAttribute('aria-expanded', on ? 'true' : 'false');
      if (on) loadMedia(item);
      var ai = item.querySelector('.x-ai'); if (on && ai) setTimeout(function () { aiRun(ai); }, 250);
    });
  });
  var burger = nav.querySelector('.x-nav-burger');
  if (burger && menu) burger.addEventListener('click', function () { setTimeout(function () { if (root.classList.contains('is-menu')) loadMedia(menu.querySelector('.x-mi')); }, 0); });
  if (menu) menu.querySelectorAll('a[href]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      var h = a.getAttribute('href'); if (h.charAt(0) !== '#' || a.hasAttribute('data-x-audit')) return;
      var t = h === '#top' ? document.body : document.querySelector(h); if (!t) return;
      e.preventDefault(); if (burger) burger.click();
      window.scrollTo(0, h === '#top' ? 0 : t.getBoundingClientRect().top + window.scrollY - 20);
    });
  });
})();
