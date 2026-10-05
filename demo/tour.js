/* Demo tool: guided tour of the site (demo branch only, loaded by demo/demo.js).
   Adds a "Take the tour" button to every page. Steps can span pages: moving to a step on
   another page navigates there with ?tour=<step> and the tour resumes on load. */
(function () {

  var PAGE = (location.pathname.split('/').pop() || 'index.html');
  var q = function (sel) { return function () { return document.querySelector(sel); }; };
  var byText = function (sel, text) {
    return function () {
      return Array.prototype.find.call(document.querySelectorAll(sel), function (el) { return el.textContent.indexOf(text) !== -1; });
    };
  };

  var STEPS = [
    // Homepage
    { page: 'index.html', title: 'Welcome to the new SWIFT website', body: 'This tour walks through each feature and page. Use Next or your arrow keys, and press Esc to leave at any time.' },
    { page: 'index.html', target: q('div.sticky.bg-urgent'), title: 'Emergency banner', body: 'Stays at the top of every page. One tap calls 000.' },
    { page: 'index.html', target: q('header'), title: 'Header', body: 'Stays in view as you scroll, with the clinic’s number and a Request appointment button on every page.' },
    { page: 'index.html', target: function () { var h = document.getElementById('heroHeadline'); return h && h.closest('section'); }, title: 'Hero', body: 'A full-width photo with SWIFT\'s promise, plus call and directions. Seasonal campaigns take over this space.' },
    { page: 'index.html', target: function () { var s = document.getElementById('openStatus'); return s && s.parentElement; }, title: 'Live opening status', body: 'Checks the time in Sydney and shows whether the clinic is open right now.' },
    { page: 'index.html', target: q('#careFinder'), title: 'Is urgent care right for me?', body: 'Visitors search a symptom or tap a common one. The answer says call 000, call SWIFT first, come to SWIFT or see your GP, and every answer ends with: if you are unsure, call SWIFT first.' },
    { page: 'index.html', target: q('#right-care'), title: 'Three ways to get care', body: 'Each column starts with a simple rule, then the most common reasons, with the rest one tap away. A search highlights its match here.' },
    { page: 'index.html', target: q('#visitStepper'), title: 'What happens when you visit', body: 'Seven steps from arrival to going home, so first-time patients know what to expect.' },
    { page: 'index.html', target: q('#other-care'), title: 'Here for something else?', body: 'Scans, dental and booked care, for visitors who aren’t here for urgent care.' },
    { page: 'index.html', target: q('#services'), title: 'Services', body: 'Each tile opens that service on the Services page.' },
    { page: 'index.html', target: q('#fees'), title: 'Fees at a glance', body: 'The main fee up front, with a link to the full fee schedule.' },
    { page: 'index.html', target: q('#doctors'), title: 'Our doctors', body: 'The clinic’s leaders, with a link to the full team.' },
    { page: 'index.html', target: q('#facilities'), title: 'Our clinic facilities', body: 'Real photos of the Rouse Hill clinic. More can be added as they come in.' },
    { page: 'index.html', target: q('#location'), title: 'Location', body: 'Address, hours and a map, with one-tap directions.' },
    { page: 'index.html', target: q('#faq'), title: 'Common questions', body: 'Short answers to what patients ask most.' },
    { page: 'index.html', target: q('#campaignDemoBtn'), title: 'Campaign preview (demo tool)', body: 'Shows a seasonal campaign, like flu season or school holidays, in the hero\'s photo slot. The question and search stay put. Not shown to patients.' },
    { page: 'index.html', target: q('#viewportSwitcher'), title: 'Device preview (demo tool)', body: 'Shows the site at tablet and mobile sizes without leaving your desk.' },
    { page: 'index.html', target: q('nav[aria-label="Quick actions"]'), title: 'Mobile quick actions', body: 'On phones, call, find care, directions and the menu are always one tap away.' },

    // Services
    { page: 'services.html', target: q('nav[aria-label="Services on this page"]'), title: 'Services page', body: 'Every service on one page. This menu jumps straight to each one.' },
    { page: 'services.html', target: q('article#emergency'), title: 'Service cards', body: 'A short summary, the key points, and a tag saying whether it’s walk-in or by appointment.' },
    { page: 'services.html', target: q('article#cardiology'), title: 'Safety built in', body: 'Where a service overlaps with an emergency, like chest pain, the card says when to call 000 instead.' },
    { page: 'services.html', target: q('article#imaging'), title: 'Independent providers', body: 'Imaging and dental are separate practices in the same building, and are labelled that way.' },

    // Fees
    { page: 'fees.html', target: byText('main .hero-in', '$396'), title: 'Fees page', body: 'The main walk-in fee is the first thing visitors see.' },
    { page: 'fees.html', target: q('#medicare'), title: 'Medicare explained', body: 'What’s covered with and without a Medicare card, in plain words.' },
    { page: 'fees.html', target: q('section#emergency'), title: 'Detailed fee tables', body: 'Every fee from the current site: urgent care, infusions, wound care and scans. The menu on the left jumps between them.' },

    // Team
    { page: 'team.html', target: function () { var g = document.getElementById('grp0'); return g && g.closest('section'); }, title: 'Meet the team', body: 'All 17 staff with photos, grouped into leadership, doctors and nurses.' },
    { page: 'team.html', target: q('#vijay-manivel'), title: 'Staff profiles', body: 'Each card opens a profile with a larger photo and bio, and has its own link to share.' },

    // Request appointment
    { page: 'request-appointment.html', target: byText('main .hero-in', 'need an appointment'), title: 'Request an appointment', body: 'Reminds urgent patients they can just walk in, before they start a form.' },
    { page: 'request-appointment.html', target: q('#serviceGroup'), title: 'Choose a service', body: 'One tap to pick what to book. Links from other pages can preselect a service.' },
    { page: 'request-appointment.html', target: q('#apptForm'), title: 'A simple, checked form', body: 'Clear error messages and a confirmation once sent. It’s ready to connect to Best Practice online booking.' },
    { page: 'request-appointment.html', title: 'That’s the tour', body: 'Every page and feature, start to finish. Press Finish to go back to the homepage.', finish: true },
  ];

  var PAGE_NAMES = { 'index.html': 'Homepage', 'services.html': 'Services', 'fees.html': 'Fees', 'team.html': 'Team', 'request-appointment.html': 'Appointments' };
  var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var css = [
    '.tour-launch{position:fixed;left:16px;bottom:128px;z-index:31;display:inline-flex;align-items:center;gap:6px;border-radius:999px;background:#fff;border:1px dashed rgba(44,104,94,.5);color:#2C685E;font:500 12px/1 "IBM Plex Sans",sans-serif;padding:9px 14px 9px 12px;box-shadow:0 4px 14px -4px rgba(30,69,63,.3);cursor:pointer;transition:transform .3s cubic-bezier(.34,1.56,.64,1),opacity .2s ease}',
    '@media (max-width:1023px){.tour-launch--desktop{display:none}}',
    '.tour-launch:hover{transform:translateY(-2px)}.tour-launch:active{transform:scale(.96)}',
    '.tour-launch:focus-visible,.tour-card button:focus-visible{outline:2px solid #4B9587;outline-offset:2px}',
    '@media (min-width:1024px){.tour-launch{bottom:64px}}',
    '.tour-active .tour-launch{opacity:0;pointer-events:none}',
    '.tour-shield{position:fixed;inset:0;z-index:95}',
    '.tour-spot{position:fixed;z-index:96;border-radius:16px;box-shadow:0 0 0 2px #6FB3A3,0 0 0 200vmax rgba(24,37,36,.55);pointer-events:none;opacity:0;transition:opacity .25s ease}',
    '.tour-spot.is-blank{box-shadow:0 0 0 200vmax rgba(24,37,36,.55)}',
    '.tour-card{position:fixed;z-index:97;width:min(360px,calc(100vw - 24px));background:#fff;color:#182524;border-radius:16px;padding:18px 18px 16px;box-shadow:0 24px 60px -18px rgba(24,37,36,.55),0 6px 16px -8px rgba(24,37,36,.3);font-family:"IBM Plex Sans",sans-serif;opacity:0;transform:translateY(8px);transition:opacity .25s ease,transform .35s cubic-bezier(.22,1,.36,1)}',
    '.tour-card.is-in{opacity:1;transform:none}',
    '.tour-meta{display:flex;align-items:center;justify-content:space-between;gap:8px;font-size:12px;color:rgba(24,37,36,.55)}',
    '.tour-chip{background:#EAF1EF;color:#1E453F;border-radius:999px;padding:3px 9px;font-weight:500}',
    '.tour-x{width:30px;height:30px;margin:-6px -6px -6px 0;border:0;background:none;border-radius:999px;color:rgba(24,37,36,.5);cursor:pointer;display:flex;align-items:center;justify-content:center;transition:background-color .2s ease,color .2s ease,transform .2s ease}',
    '.tour-x:hover{background:#EAF1EF;color:#182524}.tour-x:active{transform:scale(.92)}',
    '.tour-title{font:700 19px/1.25 "Bricolage Grotesque",sans-serif;letter-spacing:-.02em;margin:10px 0 6px}',
    '.tour-body{font-size:15px;line-height:1.6;color:rgba(24,37,36,.75);margin:0}',
    '.tour-bar{height:3px;background:#D9E3E0;border-radius:3px;margin:16px 0 14px;overflow:hidden}',
    '.tour-bar span{display:block;height:100%;background:#2C685E;border-radius:3px;transform-origin:left;transition:transform .4s cubic-bezier(.22,1,.36,1)}',
    '.tour-actions{display:flex;justify-content:space-between;align-items:center;gap:8px}',
    '.tour-btn{border-radius:999px;font:500 14px/1 "IBM Plex Sans",sans-serif;padding:10px 16px;cursor:pointer;transition:transform .3s cubic-bezier(.34,1.56,.64,1),background-color .2s ease,color .2s ease}',
    '.tour-btn:active{transform:scale(.96)}',
    '.tour-back{background:none;border:1px solid #D9E3E0;color:#1E453F}.tour-back:hover{background:#EAF1EF}.tour-back[disabled]{opacity:.35;pointer-events:none}',
    '.tour-next{background:#2C685E;border:1px solid #2C685E;color:#fff}.tour-next:hover{background:#377E71;transform:translateY(-1px)}',
    '@media (prefers-reduced-motion:reduce){.tour-card,.tour-spot,.tour-bar span{transition:none}}'
  ].join('\n');

  var style = document.createElement('style');
  style.textContent = css;
  document.head.appendChild(style);

  var launch = document.createElement('button');
  launch.type = 'button';
  launch.className = 'tour-launch';
  launch.innerHTML = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M8 5.5v13l10.5-6.5L8 5.5Z" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></svg>Take the tour';
  launch.addEventListener('click', function () { go(0); });
  document.body.appendChild(launch);

  // On small screens the floating button would cover page content, so the tour lives in the mobile menu instead
  if (window.SwiftDemo && document.querySelector('#mobileMenu nav')) {
    launch.classList.add('tour-launch--desktop');
    window.SwiftDemo.addMenuItem('Take the tour', function () { go(0); }, true);
  }

  var shield, spot, card, current = -1, settleTimer, lastFocus;

  function el(tag, cls) { var e = document.createElement(tag); if (cls) e.className = cls; return e; }

  function build() {
    shield = el('div', 'tour-shield');
    spot = el('div', 'tour-spot');
    card = el('div', 'tour-card');
    card.setAttribute('role', 'dialog');
    card.setAttribute('aria-modal', 'true');
    card.setAttribute('aria-labelledby', 'tourTitle');
    card.innerHTML =
      '<div class="tour-meta"><span><span class="tour-chip" id="tourPage"></span> <span id="tourCount" style="margin-left:6px"></span></span>' +
      '<button type="button" class="tour-x" id="tourExit" aria-label="Exit tour"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></button></div>' +
      '<p class="tour-title" id="tourTitle"></p><p class="tour-body" id="tourBody" aria-live="polite"></p>' +
      '<div class="tour-bar" aria-hidden="true"><span id="tourBar"></span></div>' +
      '<div class="tour-actions"><button type="button" class="tour-btn tour-back" id="tourBack">Back</button>' +
      '<button type="button" class="tour-btn tour-next" id="tourNext">Next</button></div>';
    document.body.appendChild(shield);
    document.body.appendChild(spot);
    document.body.appendChild(card);
    card.querySelector('#tourExit').addEventListener('click', end);
    card.querySelector('#tourBack').addEventListener('click', function () { go(current - 1, -1); });
    card.querySelector('#tourNext').addEventListener('click', function () {
      if (STEPS[current].finish) { end(); if (PAGE !== 'index.html') location.href = 'index.html'; return; }
      go(current + 1, 1);
    });
    document.addEventListener('keydown', onKey);
    window.addEventListener('scroll', place, { passive: true });
    window.addEventListener('resize', place);
    document.documentElement.classList.add('tour-active');
  }

  function onKey(e) {
    if (current < 0) return;
    if (e.key === 'Escape') { e.preventDefault(); end(); }
    else if (e.key === 'ArrowRight') { e.preventDefault(); card.querySelector('#tourNext').click(); }
    else if (e.key === 'ArrowLeft' && current > 0) { e.preventDefault(); go(current - 1, -1); }
  }

  function targetOf(step) {
    if (!step || !step.target) return null;
    var t = step.target();
    if (!t) return null;
    var r = t.getBoundingClientRect();
    return (r.width && r.height) ? t : null; // hidden at this screen size, e.g. mobile-only bar on desktop
  }

  // Move to step i, skipping steps whose target isn't shown at this screen size
  function go(i, dir) {
    dir = dir || 1;
    while (i >= 0 && i < STEPS.length && STEPS[i].page === PAGE && STEPS[i].target && !targetOf(STEPS[i])) i += dir;
    if (i < 0 || i >= STEPS.length) return;
    if (STEPS[i].page !== PAGE) { location.href = STEPS[i].page + '?tour=' + i + (dir < 0 ? '&dir=back' : ''); return; }
    if (!card) { lastFocus = document.activeElement; build(); }
    current = i;
    render();
  }

  function render() {
    var step = STEPS[current];
    card.classList.remove('is-in');
    spot.style.opacity = '0';
    card.querySelector('#tourPage').textContent = PAGE_NAMES[step.page];
    card.querySelector('#tourCount').textContent = (current + 1) + ' of ' + STEPS.length;
    card.querySelector('#tourTitle').textContent = step.title;
    card.querySelector('#tourBody').textContent = step.body;
    card.querySelector('#tourBar').style.transform = 'scaleX(' + ((current + 1) / STEPS.length) + ')';
    card.querySelector('#tourBack').disabled = current === 0;
    var next = STEPS[current + 1];
    card.querySelector('#tourNext').textContent = step.finish ? 'Finish'
      : (next && next.page !== PAGE ? 'Next: ' + PAGE_NAMES[next.page] : 'Next');

    var t = targetOf(step);
    if (t) {
      var r = t.getBoundingClientRect();
      var headerH = headerOffset();
      var room = window.innerHeight - headerH - 24;
      var top = r.height <= room ? r.top + window.scrollY - headerH - Math.max(16, (room - r.height) / 3) : r.top + window.scrollY - headerH - 16;
      if (getComputedStyle(t).position === 'fixed' || t.closest('header') || t.classList.contains('sticky')) top = window.scrollY;
      if (t.tagName === 'HEADER' || t.classList.contains('sticky')) top = 0;
      window.scrollTo({ top: Math.max(0, top), behavior: reduceMotion ? 'auto' : 'smooth' });
    }
    clearTimeout(settleTimer);
    settleTimer = setTimeout(function () { place(true); card.classList.add('is-in'); card.querySelector('#tourNext').focus({ preventScroll: true }); }, t && !reduceMotion ? 520 : 60);
  }

  function headerOffset() {
    var h = document.querySelector('header');
    return h ? Math.max(0, h.getBoundingClientRect().bottom) : 0;
  }

  // Position the spotlight on the target and, once scrolling settles, the card beside it
  function place(settled) {
    if (current < 0 || !card) return;
    var step = STEPS[current];
    var t = targetOf(step);
    var vw = window.innerWidth, vh = window.innerHeight, pad = 8, gap = 14;
    var cw = card.offsetWidth, ch = card.offsetHeight;

    if (!t) {
      spot.classList.add('is-blank');
      spot.style.cssText += ';left:50%;top:50%;width:0;height:0;opacity:1';
      card.style.left = Math.round((vw - cw) / 2) + 'px';
      card.style.top = Math.round((vh - ch) / 2) + 'px';
      return;
    }
    spot.classList.remove('is-blank');
    var r = t.getBoundingClientRect();
    var sTop = Math.max(r.top - pad, 0), sBot = Math.min(r.bottom + pad, vh);
    spot.style.left = (r.left - pad) + 'px';
    spot.style.top = sTop + 'px';
    spot.style.width = (r.width + pad * 2) + 'px';
    spot.style.height = Math.max(0, sBot - sTop) + 'px';
    spot.style.opacity = '1';

    if (settled !== true) return;
    var left = Math.min(Math.max(12, r.left), vw - cw - 12);
    var top;
    if (vh - sBot >= ch + gap + 12) top = sBot + gap;              // below
    else if (sTop - headerOffset() >= ch + gap + 12) top = sTop - ch - gap; // above
    else if (vw - (r.right + pad) >= cw + gap + 12) { left = r.right + pad + gap; top = Math.max(headerOffset() + 12, Math.min(sTop, vh - ch - 12)); } // right
    else if (r.left - pad >= cw + gap + 12) { left = r.left - pad - gap - cw; top = Math.max(headerOffset() + 12, Math.min(sTop, vh - ch - 12)); } // left
    else { top = vh - ch - 12; left = Math.round((vw - cw) / 2); }  // over the lower part of a tall target
    card.style.left = Math.round(left) + 'px';
    card.style.top = Math.round(top) + 'px';
  }

  function end() {
    current = -1;
    clearTimeout(settleTimer);
    [shield, spot, card].forEach(function (n) { if (n && n.parentNode) n.parentNode.removeChild(n); });
    shield = spot = card = null;
    document.removeEventListener('keydown', onKey);
    window.removeEventListener('scroll', place);
    window.removeEventListener('resize', place);
    document.documentElement.classList.remove('tour-active');
    if (lastFocus && lastFocus.focus) lastFocus.focus({ preventScroll: true });
    else launch.focus({ preventScroll: true });
  }

  // Resume a tour that navigated here from another page
  var m = /[?&]tour=(\d+)/.exec(location.search);
  if (m) {
    var start = parseInt(m[1], 10);
    var dir = /[?&]dir=back/.test(location.search) ? -1 : 1;
    if (history.replaceState) history.replaceState(null, '', location.pathname + location.hash);
    var begin = function () { setTimeout(function () { go(start, dir); }, 250); };
    if (document.readyState === 'complete') begin(); else window.addEventListener('load', begin);
  }
})();
