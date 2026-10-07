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
