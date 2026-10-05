/* Demo tool: switch between the current homepage and saved prototypes (demo branch only, loaded by demo/demo.js).
   Only shows on the pages being compared. Add a prototype by adding a line to VERSIONS. */
(function () {
  var VERSIONS = [
    { file: 'index.html', label: 'Teal' },
    { file: 'prototype-logo-colours.html', label: 'Logo colours' },
    { file: 'prototype-split-hero.html', label: 'Split hero' }
  ];
  var page = location.pathname.split('/').pop() || 'index.html';
  var here = VERSIONS.filter(function (v) { return v.file === page; })[0];
  if (!here) return;

  var bar = document.createElement('div');
  bar.id = 'compareSwitcher';
  bar.setAttribute('role', 'group');
  bar.setAttribute('aria-label', 'Compare homepage versions');
  bar.className = 'fixed z-[80] bottom-[108px] left-4 hidden lg:flex items-center gap-0.5 rounded-full bg-white border border-dashed border-ink/25 shadow-[0_4px_14px_-4px_rgba(0,0,0,0.2)] p-1';
  bar.innerHTML = '<span class="text-xs text-ink/70 pl-3 pr-2">Compare</span>' + VERSIONS.map(function (v) {
    var on = v === here;
    return '<a href="' + v.file + '"' + (on ? ' aria-current="page"' : '') +
      ' class="focus-ring rounded-full text-xs font-medium px-3 py-1.5 transition-colors ' +
      (on ? 'bg-teal700 text-white' : 'text-ink/70 hover:text-ink hover:bg-mint active:bg-line') + '">' + v.label + '</a>';
  }).join('');
  document.body.appendChild(bar);

  if (window.SwiftDemo) {
    VERSIONS.forEach(function (v) {
      if (v !== here) window.SwiftDemo.addMenuItem('Compare: view ' + v.label.toLowerCase() + ' version', function () { location.href = v.file; });
    });
  }
})();
