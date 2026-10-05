"""Wrap a page's <main> content in the site chrome taken from request-appointment.html."""
import os, re, sys
ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '')
src = open(ROOT + 'request-appointment.html').read()

def between(a, b, incl_b=False):
    i = src.index(a); j = src.index(b, i)
    return src[i:j + (len(b) if incl_b else 0)]

head = src[:src.index('  /* Service picker tiles */')]
chrome = between('<body', '<main>')
footer = between('<!-- Footer -->', '</footer>', incl_b=True)
menu_js = between('  (function () {\n    var btn = document.getElementById(\'menuBtn\');', '  })();', incl_b=True)

# Design tokens shared by every sub page (match the homepage)
SURFACE = 'shadow-[0_1px_2px_rgba(30,69,63,0.05),0_12px_28px_-20px_rgba(30,69,63,0.35)]'
CARD = 'bg-white rounded-[20px] border border-line ' + SURFACE
H2 = 'font-display font-bold text-2xl sm:text-3xl leading-[1.12] tracking-[-0.02em] text-ink'
BTN = 'focus-ring spring inline-flex items-center justify-center rounded-full font-medium text-[15px] px-5 py-2.5 hover:scale-[1.03] active:scale-[0.97] duration-300 '
BTN_PRIMARY = BTN + 'bg-teal900 hover:bg-teal700 text-white transition-[transform,background-color]'
BTN_SECONDARY = BTN + 'border border-ink/15 bg-white text-ink hover:border-teal700 hover:text-teal900 transition-[transform,border-color,color]'

def intro(crumb, title, text, aside=''):
    """Page intro in the homepage's section style: big heading left, text (or an aside) right."""
    bc = ('      <nav aria-label="Breadcrumb" class="hero-in text-sm text-ink/70 mb-5" style="animation-delay:.02s">\n'
          '        <a href="index.html" class="inline-block py-1 hover:text-teal700 active:text-teal900 focus-ring rounded">Home</a>\n'
          '        <span aria-hidden="true" class="mx-1.5">/</span>\n'
          '        <span class="text-ink/80" aria-current="page">%s</span>\n      </nav>\n') % crumb
    h1 = ('<h1 class="hero-in text-balance font-display font-extrabold text-[2.6rem] leading-[1.02] sm:text-[3.5rem] tracking-[-0.03em] text-ink" style="animation-delay:.08s">%s</h1>' % title)
    p = '<p class="hero-in %s text-lg text-ink/70 leading-[1.7] max-w-xl" style="animation-delay:.2s">%s</p>'
    if aside:
        body = ('      <div class="grid lg:grid-cols-12 gap-8 lg:gap-12 items-end">\n'
                '        <div class="lg:col-span-7">\n          %s\n          %s\n        </div>\n'
                '        <div class="lg:col-span-5 hero-in" style="animation-delay:.3s">\n%s\n        </div>\n      </div>') % (h1, p % ('mt-5', text), aside)
    else:
        body = ('      <div class="grid lg:grid-cols-12 gap-5 lg:gap-12 items-end">\n'
                '        <div class="lg:col-span-6">%s</div>\n'
                '        <div class="lg:col-span-6">%s</div>\n      </div>') % (h1, p % ('lg:mb-2', text))
    return ('\n  <!-- Page intro -->\n  <section class="max-w-6xl mx-auto px-5 sm:px-8 pt-8 sm:pt-12 pb-10 sm:pb-16">\n'
            + bc + body + '\n  </section>\n')

REQ_BTN = '''      <a href="request-appointment.html" class="hidden sm:inline-flex focus-ring items-center rounded-full bg-teal700 hover:bg-teal600 text-white text-sm font-medium px-4 py-2 sm:px-5 sm:py-2.5 transition-colors active:scale-[0.97]">
        Request appointment
      </a>
      <button id="menuBtn"'''
REQ_BTN_MOBILE = '''<a href="tel:0288599099" class="mobile-link font-medium text-teal900">(02) 8859 9099</a>
          <a href="request-appointment.html" class="mobile-link focus-ring inline-flex items-center justify-center rounded-full bg-teal700 hover:bg-teal600 text-white text-sm font-medium px-5 py-2.5 transition-colors active:scale-[0.97]">Request appointment</a>'''

def site_links(html):
    return (html.replace('index.html#services"', 'services.html"')
                .replace('index.html#fees"', 'fees.html"'))

def build(filename, title, desc, main, active=None, css='', js=''):
    h = head
    h = re.sub(r'<title>.*?</title>', '<title>' + title + '</title>', h)
    h = re.sub(r'<meta name="description" content=".*?">', '<meta name="description" content="' + desc + '">', h)
    h = re.sub(r'<meta property="og:title" content=".*?">', '<meta property="og:title" content="' + title.replace('&amp;', '&') + '">', h)
    h = re.sub(r'<meta property="og:description" content=".*?">', '<meta property="og:description" content="' + desc + '">', h)
    c = chrome.replace('      <button id="menuBtn"', REQ_BTN, 1)
    c = c.replace('<a href="tel:0288599099" class="mobile-link font-medium text-teal900">(02) 8859 9099</a>', REQ_BTN_MOBILE, 1)
    c, f = site_links(c), site_links(footer)
    if 'team.html' not in f:
        f = f.replace('<li><a href="fees.html" class="hover:text-white focus-ring rounded">Fees</a></li>',
                  '<li><a href="fees.html" class="hover:text-white focus-ring rounded">Fees</a></li>\n        <li><a href="team.html" class="hover:text-white focus-ring rounded">Our team</a></li>')
    if active:
        # Mark the current page in the header and mobile menu
        c = c.replace('<a href="%s" class="hover:text-teal700' % active, '<a href="%s" aria-current="page" class="text-teal700 font-medium hover:text-teal900' % active)
        c = c.replace('<a href="%s" class="mobile-link py-2.5 hover:text-teal700' % active, '<a href="%s" aria-current="page" class="mobile-link py-2.5 text-teal700 font-medium hover:text-teal900' % active)
    out = (h + css + '</style>\n</head>\n\n' + c + '<main>\n' + main + '\n</main>\n\n' + f +
           '\n\n<script>\n' + menu_js + '\n' + js + '\n</script>\n<script src="demo/demo.js" defer></script>\n</body>\n</html>\n')
    open(ROOT + filename, 'w').write(out)
    print('wrote', filename, len(out), 'bytes')
