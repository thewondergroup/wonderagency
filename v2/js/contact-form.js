/* Contact form -> Google Sheet + email (via Google Apps Script web app).
   Paste the web app URL from Apps Script (Deploy > Manage deployments) below. */
(function () {
  var ENDPOINT = 'https://script.google.com/macros/s/AKfycbzzPgtb-gHU8EsYfempzwVKaS_g3TtE_8aqz2OQfLsmGA_qhBLciC1_FPOA-lUy9cikzw/exec';

  var form = document.getElementById('email-form');
  if (!form) return;
  var wrap = form.parentNode;
  var done = wrap.querySelector('.w-form-done');
  var fail = wrap.querySelector('.w-form-fail');
  var button = form.querySelector('input[type="submit"]');

  // Hidden field real people never fill in; bots do. Filled = ignored by the script.
  var trap = document.createElement('input');
  trap.type = 'text'; trap.name = 'website'; trap.tabIndex = -1; trap.autocomplete = 'off';
  trap.setAttribute('aria-hidden', 'true');
  trap.style.cssText = 'position:absolute;left:-9999px;width:1px;height:1px;opacity:0';
  form.appendChild(trap);

  function show(ok) {
    if (ok) { form.style.display = 'none'; done.style.display = 'block'; fail.style.display = 'none'; }
    else { fail.style.display = 'block'; }
  }

  // Runs before Webflow's own handler and stops it, so nothing is sent to Webflow.
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    e.stopPropagation();
    if (form.dataset.sending) return;
    if (ENDPOINT.indexOf('https://') !== 0) { show(false); return; }

    var data = new URLSearchParams(new FormData(form));
    data.set('checkbox', form.querySelector('#checkbox').checked ? 'Yes' : 'No');
    data.set('page', location.href);

    var label = button.value;
    form.dataset.sending = '1';
    button.value = button.getAttribute('data-wait') || label;
    fail.style.display = 'none';

    fetch(ENDPOINT, { method: 'POST', body: data })
      .then(function (r) { return r.json(); })
      .then(function (j) { show(j && j.ok === true); })
      .catch(function () { show(false); })
      .then(function () { delete form.dataset.sending; button.value = label; });
  });
})();
