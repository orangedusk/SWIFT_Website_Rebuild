/* Demo tool: desktop / tablet / mobile preview (demo branch only, loaded by demo/demo.js).
   Shows the current page in an iframe at tablet or phone width. */
(function () {
  var style = document.createElement('style');
  style.textContent =
    '.viewport-btn { color: rgba(24,37,36,0.5); }' +
    '.viewport-btn:hover { color: rgba(24,37,36,0.8); background: #EAF1EF; }' +
    '.viewport-btn[aria-pressed="true"] { background: #2C685E; color: #fff; }' +
    '.viewport-btn[aria-pressed="true"]:hover { background: #2C685E; color: #fff; }';
  document.head.appendChild(style);

  var wrap = document.createElement('div');
  wrap.innerHTML =
    '<div id="viewportSwitcher" class="fixed z-[80] bottom-5 right-4 hidden lg:flex items-center gap-0.5 rounded-full bg-white border border-dashed border-ink/25 shadow-[0_4px_14px_-4px_rgba(0,0,0,0.2)] p-1">' +
    '  <button type="button" data-viewport="desktop" class="viewport-btn focus-ring flex items-center gap-1.5 rounded-full text-xs font-medium px-3 py-1.5 transition-colors" aria-pressed="true">' +
    '    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" aria-hidden="true"><rect x="3" y="4" width="18" height="12" rx="1.2" stroke="currentColor" stroke-width="1.6"/><path d="M9 20h6M12 16v4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>' +
    '    Desktop' +
    '  </button>' +
    '  <button type="button" data-viewport="tablet" class="viewport-btn focus-ring flex items-center gap-1.5 rounded-full text-xs font-medium px-3 py-1.5 transition-colors" aria-pressed="false">' +
    '    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" aria-hidden="true"><rect x="5" y="2.5" width="14" height="19" rx="1.6" stroke="currentColor" stroke-width="1.6"/><path d="M11 19h2" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>' +
    '    Tablet' +
    '  </button>' +
    '  <button type="button" data-viewport="mobile" class="viewport-btn focus-ring flex items-center gap-1.5 rounded-full text-xs font-medium px-3 py-1.5 transition-colors" aria-pressed="false">' +
    '    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" aria-hidden="true"><rect x="7" y="2" width="10" height="20" rx="1.8" stroke="currentColor" stroke-width="1.6"/><path d="M11 19h2" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>' +
    '    Mobile' +
    '  </button>' +
    '</div>' +
    '' +
    '<div id="viewportOverlay" class="fixed inset-0 z-[70] hidden bg-ink/70 backdrop-blur-sm">' +
    '  <div class="relative h-full flex flex-col items-center justify-center gap-3 p-6">' +
    '    <div class="flex items-center gap-3 text-white/90 text-sm font-medium">' +
    '      <span id="viewportLabel">Tablet — 768px</span>' +
    '      <button type="button" id="viewportClose" class="focus-ring inline-flex items-center gap-1.5 rounded-full bg-white/15 hover:bg-white/25 text-white px-3 py-1.5 text-xs transition-colors">' +
    '        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>' +
    '        Close' +
    '      </button>' +
    '    </div>' +
    '    <div class="rounded-[1.5rem] border-4 border-ink/80 bg-white shadow-[0_30px_80px_-20px_rgba(0,0,0,0.6)] overflow-hidden" style="height: min(85vh, 900px);">' +
    '      <iframe id="viewportFrame" title="Site preview" class="h-full" style="width: 768px;"></iframe>' +
    '    </div>' +
    '  </div>';
  while (wrap.firstChild) document.body.appendChild(wrap.firstChild);

  var switcher = document.getElementById('viewportSwitcher');
  var overlay = document.getElementById('viewportOverlay');
  var frame = document.getElementById('viewportFrame');
  var label = document.getElementById('viewportLabel');

  // Campaigns can be switched while a device preview is open (homepage only)
  if (window.SwiftDemoCampaigns) {
    var campaignBtn = document.createElement('button');
    campaignBtn.type = 'button';
    campaignBtn.className = 'focus-ring inline-flex items-center gap-1.5 rounded-full bg-white/15 hover:bg-white/25 active:bg-white/30 text-white px-3 py-1.5 text-xs transition-colors';
    campaignBtn.innerHTML = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M4 5h16M4 12h10M4 19h13" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>Preview campaigns';
    campaignBtn.addEventListener('click', window.SwiftDemoCampaigns.open);
    label.parentNode.insertBefore(campaignBtn, label.nextSibling);
  }
  var closeBtn = document.getElementById('viewportClose');

  var sizes = {
    tablet: { width: 768, label: 'Tablet — 768px' },
    mobile: { width: 390, label: 'Mobile — 390px' }
  };

  var buttons = Array.prototype.slice.call(switcher.querySelectorAll('.viewport-btn'));

  function setActive(name) {
    buttons.forEach(function (b) {
      b.setAttribute('aria-pressed', b.dataset.viewport === name ? 'true' : 'false');
    });
  }

  function showViewport(name) {
    var size = sizes[name];
    frame.style.width = size.width + 'px';
    label.textContent = size.label;
    if (!frame.src) frame.src = window.location.href;
    overlay.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
    setActive(name);
  }

  function showDesktop() {
    overlay.classList.add('hidden');
    document.body.style.overflow = '';
    setActive('desktop');
  }

  buttons.forEach(function (btn) {
    btn.addEventListener('click', function () {
      var name = btn.dataset.viewport;
      if (name === 'desktop') showDesktop();
      else showViewport(name);
    });
  });

  closeBtn.addEventListener('click', showDesktop);
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && !overlay.classList.contains('hidden')) showDesktop();
  });
})();
