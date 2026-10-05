/* Demo tool: password screen for the preview site (demo branch only, never on main).
   Loaded at the top of <head> so the page stays hidden until the password is entered.
   This keeps casual visitors out; it is not real security (the HTML is still in the files).

   Only a SHA-256 hash of the password is stored here. To change the password, run:
     node -e "console.log(require('crypto').createHash('sha256').update('swift-demo:' + process.argv[1]).digest('hex'))" 'NEW PASSWORD'
   and paste the result into HASH below. */
(function () {
  var HASH = '9568dc38576cc3c31cf96a96e0498324a77007aa3c9196fab71baa8c91b96b83';
  var KEY = 'swiftDemoUnlocked';

  try { if (localStorage.getItem(KEY) === HASH) return; } catch (e) {}

  var root = document.documentElement;
  root.classList.add('demo-locked');
  var style = document.createElement('style');
  style.textContent =
    'html.demo-locked body > *:not(#demoGate) { display: none !important; }' +
    'html.demo-locked, html.demo-locked body { background: #F6F8F7; }' +
    '#demoGate { position: fixed; inset: 0; z-index: 2147483647; display: flex; align-items: center; justify-content: center; padding: 20px; background: #F6F8F7; font-family: "IBM Plex Sans", system-ui, sans-serif; color: #182524; }' +
    '#demoGate form { width: 100%; max-width: 400px; background: #fff; border: 1px solid #D9E3E0; border-radius: 20px; padding: 32px 28px; box-shadow: 0 1px 2px rgba(30,69,63,.06), 0 24px 48px -28px rgba(30,69,63,.45); }' +
    '#demoGate .gate-logo { display: flex; align-items: center; gap: 10px; font-family: "Bricolage Grotesque", system-ui, sans-serif; font-weight: 700; font-size: 18px; }' +
    '#demoGate h1 { margin: 28px 0 0; font-family: "Bricolage Grotesque", system-ui, sans-serif; font-weight: 700; font-size: 28px; line-height: 1.1; letter-spacing: -0.02em; }' +
    '#demoGate p { margin: 10px 0 0; font-size: 15px; line-height: 1.6; color: rgba(24,37,36,.7); }' +
    '#demoGate label { display: block; margin-top: 24px; font-size: 14px; font-weight: 500; }' +
    '#demoGate input { display: block; width: 100%; box-sizing: border-box; margin-top: 8px; font: inherit; font-size: 16px; padding: 12px 16px; border: 1px solid #D9E3E0; border-radius: 12px; background: #fff; color: #182524; }' +
    '#demoGate input:hover { border-color: #4B9587; }' +
    '#demoGate input:focus-visible, #demoGate button:focus-visible { outline: 2px solid #4B9587; outline-offset: 2px; }' +
    '#demoGate input[aria-invalid="true"] { border-color: #B23A3A; }' +
    '#demoGate .gate-error { margin-top: 8px; font-size: 14px; color: #8C2C2C; }' +
    '#demoGate button { margin-top: 20px; width: 100%; font: inherit; font-weight: 500; color: #fff; background: #1E453F; border: 0; border-radius: 999px; padding: 13px 20px; cursor: pointer; transition: background-color .2s ease, transform .2s cubic-bezier(.34,1.56,.64,1); }' +
    '#demoGate button:hover { background: #2C685E; }' +
    '#demoGate button:active { transform: scale(.97); }' +
    '#demoGate button[disabled] { opacity: .6; cursor: progress; }';
  (document.head || root).appendChild(style);

  function sha256(text) {
    return crypto.subtle.digest('SHA-256', new TextEncoder().encode(text)).then(function (buf) {
      return Array.prototype.map.call(new Uint8Array(buf), function (b) { return ('0' + b.toString(16)).slice(-2); }).join('');
    });
  }

  function show() {
    var gate = document.createElement('div');
    gate.id = 'demoGate';
    gate.innerHTML =
      '<form novalidate>' +
        '<div class="gate-logo"><img src="brand_assets/logo/swift-logo.png" alt="SWIFT Emergency &amp; Urgent Care" width="168" height="60"></div>' +
        '<h1>Website preview</h1>' +
        '<p>This is a private preview of the new SWIFT website. Enter the password you were given to view it.</p>' +
        '<label for="demoGatePassword">Password</label>' +
        '<input id="demoGatePassword" type="password" autocomplete="current-password" required aria-describedby="demoGateError">' +
        '<div id="demoGateError" class="gate-error" role="alert"></div>' +
        '<button type="submit">View preview</button>' +
      '</form>';
    document.body.appendChild(gate);

    var form = gate.querySelector('form');
    var input = gate.querySelector('input');
    var error = gate.querySelector('.gate-error');
    var button = gate.querySelector('button');
    input.focus();

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!input.value) {
        input.setAttribute('aria-invalid', 'true');
        error.textContent = 'Enter the password to continue.';
        return;
      }
      button.disabled = true;
      sha256('swift-demo:' + input.value).then(function (h) {
        button.disabled = false;
        if (h !== HASH) {
          input.setAttribute('aria-invalid', 'true');
          error.textContent = "That password doesn't match. Check it and try again.";
          input.select();
          return;
        }
        try { localStorage.setItem(KEY, HASH); } catch (err) {}
        root.classList.remove('demo-locked');
        gate.remove();
      });
    });
  }

  if (document.body) show(); else document.addEventListener('DOMContentLoaded', show);
})();
