/* The Wonder Agency: behaviour for the added sections */
(function () {
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Accordions (services + questions): one open at a time per group
  document.querySelectorAll('.x-acc').forEach(function (acc) {
    acc.addEventListener('click', function (e) {
      var btn = e.target.closest('.x-acc-btn');
      if (!btn) return;
      var item = btn.parentNode, open = item.classList.contains('is-open');
      acc.querySelectorAll('.x-acc-item.is-open').forEach(function (i) {
        i.classList.remove('is-open');
        i.querySelector('.x-acc-btn').setAttribute('aria-expanded', 'false');
      });
      if (!open) { item.classList.add('is-open'); btn.setAttribute('aria-expanded', 'true'); }
    });
  });

  // Count-up for the stats
  function countUp(el) {
    var target = parseFloat(el.getAttribute('data-count')), suffix = el.getAttribute('data-suffix') || '';
    var fmt = function (n) { return Math.round(n).toLocaleString('en-GB') + suffix; };
    if (reduce) { el.textContent = fmt(target); return; }
    var start = null, dur = 1600;
    (function step(t) {
      if (!start) start = t;
      var p = Math.min((t - start) / dur, 1);
      el.textContent = fmt(target * (1 - Math.pow(1 - p, 3)));
      if (p < 1) requestAnimationFrame(step);
    })(performance.now());
  }

  // Reveal on scroll
  var targets = document.querySelectorAll('.x-r, .x-chat, [data-count]');
  if (!('IntersectionObserver' in window)) {
    targets.forEach(function (el) { el.classList.add('x-in'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        en.target.classList.add('x-in');
        if (en.target.hasAttribute('data-count')) countUp(en.target);
        io.unobserve(en.target);
      });
    }, { threshold: 0.12 });
    targets.forEach(function (el) { io.observe(el); });
  }

  // Videos marked data-x-auto: load when first seen, play only while on screen
  var autos = document.querySelectorAll('video[data-x-auto]');
  function playV(v) { if (!v.getAttribute('src') && v.dataset.src) v.src = v.dataset.src; var p = v.play(); if (p && p.catch) p.catch(function () {}); }
  if ('IntersectionObserver' in window) {
    var vio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) playV(en.target); else en.target.pause(); });
    }, { threshold: 0.2 });
    autos.forEach(function (v) { vio.observe(v); });
  } else { autos.forEach(playV); }

  // Hero: cards stack in the middle, scatter, then the name comes in
  var hero = document.getElementById('hero'), cards = hero && hero.querySelector('.x-cards');
  if (cards) {
    var n = cards.children.length;
    var finish = function () { cards.classList.add('is-live'); hero.classList.add('is-done'); };
    if (reduce || window.scrollY > 80) {
      cards.classList.add('is-scatter'); hero.classList.add('is-name'); finish();
    } else {
      var stackTime = n * 130 + 800;
      requestAnimationFrame(function () { requestAnimationFrame(function () { cards.classList.add('is-stack'); }); });
      setTimeout(function () { cards.classList.remove('is-stack'); cards.classList.add('is-scatter'); }, stackTime);
      setTimeout(function () { hero.classList.add('is-name'); }, stackTime + 550);
      setTimeout(finish, stackTime + 550 + 1300);
    }
    // gentle drift with the mouse, and spread as you scroll away
    if (!reduce) {
      window.addEventListener('mousemove', function (e) {
        if (window.scrollY > window.innerHeight) return;
        cards.style.setProperty('--mx', ((e.clientX / window.innerWidth - 0.5) * -34).toFixed(1) + 'px');
        cards.style.setProperty('--my', ((e.clientY / window.innerHeight - 0.5) * -34).toFixed(1) + 'px');
      }, { passive: true });
    }
  }

  // Scroll-linked bits: hero spread + reel wall drift
  var wall = document.querySelector('.x-wall'), track = wall && wall.querySelector('.x-wall-track'), ticking = false;
  function onScroll() {
    ticking = false;
    var vh = window.innerHeight, y = window.scrollY;
    if (cards && !reduce && y < vh * 2) cards.style.setProperty('--k', (1 + Math.min(y / vh, 1.5) * 0.4).toFixed(3));
    if (track && !reduce) {
      var r = wall.getBoundingClientRect(), total = r.height - vh;
      var p = Math.max(0, Math.min(1, -r.top / total));
      var max = Math.max(0, track.scrollWidth - window.innerWidth);
      track.style.transform = 'translate3d(' + (-max * p).toFixed(1) + 'px,0,0)';
    }
  }
  window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  window.addEventListener('resize', onScroll); onScroll();

  // Hover preview on closed service rows (desktop pointers only)
  var peek = document.querySelector('.x-peek');
  if (peek && window.matchMedia('(hover:hover) and (min-width:992px)').matches) {
    var pv = peek.querySelector('video');
    document.querySelectorAll('.x-acc-item[data-peek]').forEach(function (item) {
      var btn = item.querySelector('.x-acc-btn');
      btn.addEventListener('mouseenter', function () {
        if (item.classList.contains('is-open')) return;
        pv.poster = item.dataset.peekPoster; pv.src = item.dataset.peek;
        var p = pv.play(); if (p && p.catch) p.catch(function () {});
        peek.classList.add('is-on');
      });
      btn.addEventListener('mousemove', function (e) {
        peek.style.setProperty('--px', (e.clientX + 36) + 'px'); peek.style.setProperty('--py', (e.clientY - 140) + 'px');
      });
      var off = function () { peek.classList.remove('is-on'); pv.pause(); };
      btn.addEventListener('mouseleave', off); btn.addEventListener('click', off);
    });
  }

  // Reel playlist in the sticky video panel: plays each reel in turn
  var v = document.getElementById('x-reel');
  if (v) {
    var list = (v.getAttribute('data-reels') || '').split(','), i = 0;
    v.addEventListener('ended', function () {
      i = (i + 1) % list.length;
      v.src = list[i];
      var p = v.play(); if (p && p.catch) p.catch(function () {});
    });
  }
})();
