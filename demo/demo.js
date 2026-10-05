/* Demo tools loader (demo branch only, never on main).
   Each page includes just this one script. It sets up the shared "Demo tools" group in the
   mobile menu, then loads each tool, which builds its own buttons and dialogs.
   Inside the viewport-preview iframe no controls are added, so the preview shows the real site;
   only the campaign follower loads, so a campaign picked outside also shows in the preview. */
(function () {
  var base = (document.currentScript && document.currentScript.src || '').replace(/[^/]*$/, '');

  // Inside the tablet/mobile preview: show the real site, but let it follow the campaign picked outside
  if (window.top !== window.self) {
    window.SwiftDemoEmbedded = true;
    var follower = document.createElement('script');
    follower.src = base + 'campaigns.js';
    document.body.appendChild(follower);
    return;
  }
  var group = null;

  // On small screens floating buttons would cover page content, so tools add an entry to the mobile menu instead
  function menuGroup() {
    if (group) return group;
    var nav = document.querySelector('#mobileMenu nav');
    if (!nav) return null;
    group = document.createElement('div');
    group.setAttribute('data-demo-menu', '');
    group.className = 'border-t border-dashed border-line mt-2 pt-3 flex flex-col gap-1';
    group.innerHTML = '<p class="text-xs text-ink/65">Demo tools, not shown to patients</p>';
    nav.appendChild(group);
    return group;
  }

  function closeMenu() {
    var menuBtn = document.getElementById('menuBtn');
    if (menuBtn && menuBtn.getAttribute('aria-expanded') === 'true') menuBtn.click();
  }

  window.SwiftDemo = {
    addMenuItem: function (label, onClick, first) {
      var g = menuGroup();
      if (!g) return;
      var item = document.createElement('button');
      item.type = 'button';
      item.className = 'text-left py-2.5 hover:text-teal700 active:text-teal900 focus-ring rounded';
      item.textContent = label;
      item.addEventListener('click', function () { closeMenu(); onClick(); });
      if (first) g.insertBefore(item, g.children[1] || null); else g.appendChild(item);
    }
  };

  // The tour loads last so the elements it points at (campaign and viewport buttons) already exist
  var tools = ['campaigns.js', 'viewport.js', 'compare.js', 'samples.js', 'tour.js'];
  (function next(i) {
    if (i >= tools.length) return;
    var s = document.createElement('script');
    s.src = base + tools[i];
    s.onload = s.onerror = function () { next(i + 1); };
    document.body.appendChild(s);
  })(0);
})();
