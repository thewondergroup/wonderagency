/* The Wonder Agency: content library on the Work page (filters + full-screen viewer) */
(function () {
  var lib = document.getElementById('p-lib'), lb = document.getElementById('p-lb');
  if (!lib || !lb) return;
  var items = [].slice.call(lib.querySelectorAll('.p-lib-item')), filters = [].slice.call(document.querySelectorAll('.p-lib-f'));
  var stage = lb.querySelector('.p-lb-media'), cap = lb.querySelector('.p-lb-cap'), count = lb.querySelector('.p-lb-count');
  var list = [], cur = 0, opener = null;

  // layout: fill columns row by row (each tile goes in the shortest column), so the first tiles sit along the top
  var colsN = 0;
  function layout(force) {
    var w = window.innerWidth, n = w >= 1100 ? 4 : w >= 768 ? 3 : 2;
    if (n === colsN && !force) return; colsN = n;
    var cols = [], h = [];
    for (var i = 0; i < n; i++) { var c = document.createElement('div'); c.className = 'p-lib-col'; cols.push(c); h.push(0); }
    items.forEach(function (it) {
      if (it.classList.contains('is-hidden')) { cols[0].appendChild(it); return; }
      var k = h.indexOf(Math.min.apply(null, h)); cols[k].appendChild(it); h[k] += parseFloat(it.dataset.r || 1) + 0.06;
    });
    lib.innerHTML = ''; cols.forEach(function (c) { lib.appendChild(c); });
  }
  layout(true);
  window.addEventListener('resize', function () { layout(false); });

  // filters
  filters.forEach(function (b) {
    b.addEventListener('click', function () {
      var f = b.dataset.f;
      filters.forEach(function (x) { var on = x === b; x.classList.toggle('is-on', on); x.setAttribute('aria-pressed', on ? 'true' : 'false'); });
      items.forEach(function (it) {
        var show = f === 'all' || (' ' + it.dataset.cat + ' ').indexOf(' ' + f + ' ') > -1;
        it.classList.toggle('is-hidden', !show);
        if (!show) { var v = it.querySelector('video'); if (v) v.pause(); }
      });
      layout(true);
      var y = lib.getBoundingClientRect().top + window.scrollY - 170;
      if (window.scrollY > y) { if (window.__lenis) window.__lenis.scrollTo(y, { duration: 0.8 }); else window.scrollTo({ top: y, behavior: 'smooth' }); }
    });
  });

  // viewer
  function show(i) {
    cur = (i + list.length) % list.length;
    var it = list[cur], el;
    stage.innerHTML = '';
    if (it.dataset.kind === 'v') {
      el = document.createElement('video');
      el.muted = true; el.loop = true; el.autoplay = true; el.playsInline = true;
      el.setAttribute('playsinline', ''); el.setAttribute('muted', ''); el.poster = it.dataset.poster; el.src = it.dataset.full;
    } else {
      el = document.createElement('img'); el.src = it.dataset.full; el.alt = it.dataset.cap;
    }
    stage.appendChild(el);
    if (el.play) { var p = el.play(); if (p && p.catch) p.catch(function () {}); }
    stage.classList.toggle('is-land', it.classList.contains('p-lib-land'));
    cap.textContent = it.dataset.cap;
    count.textContent = (cur + 1) + ' / ' + list.length;
    // preload the next one
    var nx = list[(cur + 1) % list.length];
    if (nx && nx.dataset.kind === 'p') { var im = new Image(); im.src = nx.dataset.full; }
  }
  function open(it) {
    list = items.filter(function (x) { return !x.classList.contains('is-hidden'); });
    opener = it; show(list.indexOf(it));
    lb.classList.add('is-open'); lb.setAttribute('aria-hidden', 'false');
    document.documentElement.classList.add('is-lb');
    if (window.__lenis) window.__lenis.stop();
    lib.querySelectorAll('video').forEach(function (v) { v.pause(); });
    lb.querySelector('.p-lb-x').focus();
  }
  function close() {
    lb.classList.remove('is-open'); lb.setAttribute('aria-hidden', 'true'); stage.innerHTML = '';
    document.documentElement.classList.remove('is-lb');
    if (window.__lenis) window.__lenis.start();
    if (opener) opener.focus({ preventScroll: true });
  }
  items.forEach(function (it) { it.addEventListener('click', function () { open(it); }); });
  lb.querySelector('.p-lb-x').addEventListener('click', close);
  lb.querySelector('.p-lb-prev').addEventListener('click', function () { show(cur - 1); });
  lb.querySelector('.p-lb-next').addEventListener('click', function () { show(cur + 1); });
  lb.addEventListener('click', function (e) { if (e.target === lb) close(); });
  document.addEventListener('keydown', function (e) {
    if (!lb.classList.contains('is-open')) return;
    if (e.key === 'Escape') close();
    else if (e.key === 'ArrowRight') show(cur + 1);
    else if (e.key === 'ArrowLeft') show(cur - 1);
  });
  var tx = null;
  lb.addEventListener('touchstart', function (e) { tx = e.touches[0].clientX; }, { passive: true });
  lb.addEventListener('touchend', function (e) {
    if (tx === null) return; var dx = e.changedTouches[0].clientX - tx; tx = null;
    if (Math.abs(dx) > 50) show(cur + (dx < 0 ? 1 : -1));
  }, { passive: true });
})();
