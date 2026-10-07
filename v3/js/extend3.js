/* The Wonder Agency: combined version (nav, smooth scroll, pinned services, video case studies) */
(function () {
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine = window.matchMedia && window.matchMedia('(pointer: fine)').matches;
  var clamp = function (v, a, b) { return v < a ? a : v > b ? b : v; };
  function load(v) { if (v && !v.getAttribute('src') && v.dataset.src) v.src = v.dataset.src; }
  function play(v) { load(v); var p = v && v.play(); if (p && p.catch) p.catch(function () {}); }

  // smooth scroll on desktop
  var lenis = null;
  if (window.Lenis && !reduce && fine) {
    try { lenis = new Lenis({ lerp: 0.1, smoothWheel: true }); window.__lenis = lenis;
      (function raf(t) { lenis.raf(t); requestAnimationFrame(raf); })(performance.now());
    } catch (e) { lenis = null; }
  }
  function goTo(y) { if (lenis) lenis.scrollTo(y, { duration: 1.3 }); else window.scrollTo({ top: y, behavior: reduce ? 'auto' : 'smooth' }); }

  // nav: shows after the opening, turns into a floating pill once you scroll
  var nav = document.getElementById('x-nav'), hero = document.getElementById('hero');
  function navTick() {
    if (!nav) return;
    if (!hero || hero.classList.contains('is-done') || window.scrollY > 80) nav.classList.add('is-ready');
    nav.classList.toggle('is-solid', window.scrollY > 60);
  }
  setInterval(navTick, 400);
  if (nav) nav.querySelectorAll('.x-nav-links a, .x-nav-brand').forEach(function (a) {
    a.addEventListener('click', function (e) {
      var id = a.getAttribute('href'), t = id === '#top' ? document.body : document.querySelector(id);
      if (!t) return; e.preventDefault(); e.stopPropagation();
      goTo(id === '#top' ? 0 : t.getBoundingClientRect().top + window.scrollY - 20);
    });
  });

  // services: pinned chapters
  var sv = document.querySelector('.x-sv'), svCur = -1;
  var chs = sv ? sv.querySelectorAll('.x-sv-ch') : [], meds = sv ? sv.querySelectorAll('.x-sv-med') : [], btns = sv ? sv.querySelectorAll('.x-sv-index button') : [];
  var rail = sv && sv.querySelector('.x-sv-rail i'), count = sv && sv.querySelector('.x-sv-count');
  function svSet(i) {
    if (i === svCur) return;
    var prev = svCur; svCur = i;
    chs.forEach(function (c, k) { c.classList.toggle('is-on', k === i); });
    btns.forEach(function (b, k) { b.classList.toggle('is-on', k === i); });
    meds.forEach(function (m, k) {
      m.classList.toggle('is-on', k === i); m.classList.toggle('was', k === prev);
      var v = m.querySelector('video'); if (k === i) play(v); else if (k !== prev) v.pause();
    });
    if (prev >= 0) setTimeout(function () { var m = meds[prev]; if (m && prev !== svCur) { m.classList.remove('was'); m.querySelector('video').pause(); } }, 900);
    if (count) count.textContent = '0' + (i + 1) + ' / 0' + chs.length;
    if (meds[i + 1]) load(meds[i + 1].querySelector('video'));
  }
  btns.forEach(function (b) {
    b.addEventListener('click', function () {
      var r = sv.getBoundingClientRect(), total = r.height - window.innerHeight, i = +b.dataset.i;
      goTo(r.top + window.scrollY + total * ((i + 0.5) / chs.length));
    });
  });

  // case studies: pinned, video behind
  var cs = document.querySelector('.x-cases'), csCur = -1;
  var csVids = cs ? cs.querySelectorAll('.x-cases-bg video') : [], csPanels = cs ? cs.querySelectorAll('.x-case2') : [], csDots = cs ? cs.querySelectorAll('.x-cases-dots span') : [];
  function csSet(i) {
    if (i === csCur) return; csCur = i;
    csVids.forEach(function (v, k) { v.classList.toggle('is-on', k === i); if (k === i) play(v); else v.pause(); });
    csPanels.forEach(function (p, k) { p.classList.toggle('is-on', k === i); });
    csDots.forEach(function (d, k) { d.classList.toggle('is-on', k === i); });
  }

  function progress(el) { var r = el.getBoundingClientRect(), total = r.height - window.innerHeight; return { p: clamp(-r.top / total, 0, 1), near: r.top < window.innerHeight * 1.5 && r.bottom > -window.innerHeight * 0.5 }; }
  var ticking = false;
  function onScroll() {
    ticking = false; navTick();
    if (sv) { var a = progress(sv); svSet(Math.min(chs.length - 1, Math.floor(a.p * chs.length))); if (rail) rail.style.height = (a.p * 100).toFixed(1) + '%';
      if (!a.near) meds.forEach(function (m) { m.querySelector('video').pause(); }); else if (meds[svCur]) play(meds[svCur].querySelector('video')); }
    if (cs) { var c = progress(cs); csSet(c.p < 0.5 ? 0 : 1); if (!c.near) csVids.forEach(function (v) { v.pause(); }); else if (csVids[csCur]) play(csVids[csCur]); }
  }
  window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  window.addEventListener('resize', onScroll); onScroll();
})();
