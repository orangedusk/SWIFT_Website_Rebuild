import sys, html, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from build_page import build, ROOT, intro, H2

# Clinic facilities gallery. Real images of the Rouse Hill clinic only.
# Add a photo: one line in PHOTOS (file, caption, detail, alt). The grid and the viewer pick it up.
# Two of the current images are the architect's renders of the fit-out, from the current site;
# swap them for photos from Berinder's photo session when they arrive.
PHOTOS = [
  ('brand_assets/clinic-reception-photo.jpg', 'Reception', 'Where you register when you walk in',
   "SWIFT's reception and waiting area, with the SWIFT logo on the wall, a curved timber counter and blue and green seating"),
  ('brand_assets/clinic-waiting-area.jpg', 'Kids and family waiting area', 'A calmer space for children while they wait',
   'The kids and family waiting area, with a tree mural, giraffe and small play table'),
  ('brand_assets/clinic-reception.jpg', 'Reception and corridor', 'Looking past reception towards the waiting area',
   'The reception counter with the SWIFT logo, and the corridor leading to the waiting area'),
]

# Videos Berinder is supplying (6 Oct meeting). Until a file arrives, its space says so.
# When one arrives: set 'src' (an .mp4 in brand_assets/) and 'poster' (a still .jpg).
VIDEOS = [
  {'title': 'Drone video', 'detail': 'The clinic and Civic Way from above', 'src': '', 'poster': ''},
  {'title': 'Walkthrough video', 'detail': 'From the front door to the treatment rooms', 'src': '', 'poster': ''},
]

FIG = 'shadow-[0_1px_2px_rgba(30,69,63,0.05),0_18px_40px_-26px_rgba(30,69,63,0.45)]'

tiles = []
for i, (src, cap, detail, alt) in enumerate(PHOTOS):
    span = 'md:col-span-2 md:row-span-2' if i == 0 else ''
    tiles.append('''      <button type="button" class="photo group relative rounded-[20px] overflow-hidden focus-ring %s %s h-64 sm:h-80 md:h-auto md:min-h-[240px] text-left active:scale-[0.99]" data-index="%d" aria-label="View larger: %s">
        <img src="%s" alt="%s" loading="lazy" class="absolute inset-0 w-full h-full object-cover transition-transform duration-500 group-hover:scale-105">
        <span class="absolute inset-0 bg-teal900 mix-blend-multiply opacity-[0.12]" aria-hidden="true"></span>
        <span class="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent" aria-hidden="true"></span>
        <span class="absolute left-5 right-5 bottom-5 text-white">
          <span class="block font-display font-semibold text-lg">%s</span>
          <span class="block text-sm text-white/80 mt-0.5">%s</span>
        </span>
      </button>''' % (span, FIG, i, html.escape(cap), src, html.escape(alt), html.escape(cap), html.escape(detail)))

videos = []
for v in VIDEOS:
    if v['src']:
        media = ('<video class="absolute inset-0 w-full h-full object-cover" controls preload="none" playsinline poster="%s">'
                 '<source src="%s" type="video/mp4"></video>') % (v['poster'], v['src'])
        label = ''
    else:
        media = ('<span class="absolute inset-0 flex flex-col items-center justify-center gap-3 text-teal700" aria-hidden="true">'
                 '<svg width="40" height="40" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="1.4"/><path d="M10 8.5v7l5.5-3.5L10 8.5Z" fill="currentColor"/></svg></span>')
        label = '<span class="inline-flex mt-2 items-center rounded-full bg-white/80 text-teal900 text-xs font-medium px-2.5 py-1">Coming soon</span>'
    videos.append('''      <figure class="rounded-[20px] overflow-hidden bg-white border border-line %s">
        <div class="relative aspect-video bg-gradient-to-br from-foam to-mint">%s</div>
        <figcaption class="p-5">
          <span class="block font-display font-semibold text-lg text-ink">%s</span>
          <span class="block text-sm text-ink/70 mt-0.5">%s</span>
          %s
        </figcaption>
      </figure>''' % (FIG, media, v['title'], v['detail'], label))

main = intro('Clinic facilities', 'Our clinic facilities',
             'Take a look around SWIFT&rsquo;s Rouse Hill clinic before you visit. Imaging, pathology and dental are in the same building.') + '''
  <!-- Photos: the first is large; the rest fill the grid. Click or tap one to see it full size. -->
  <section class="max-w-6xl mx-auto px-5 sm:px-8 pb-14 sm:pb-20" aria-labelledby="photosHeading">
    <h2 id="photosHeading" class="sr-only">Photos</h2>
    <div class="grid md:grid-cols-3 md:grid-rows-2 gap-4 md:h-[520px]">
''' + '\n'.join(tiles) + '''
    </div>
  </section>

  <!-- Videos -->
  <section class="max-w-6xl mx-auto px-5 sm:px-8 pb-16 sm:pb-24" aria-labelledby="videosHeading">
    <h2 id="videosHeading" class="''' + H2 + ''' mb-6">Videos</h2>
    <div class="grid md:grid-cols-2 gap-4">
''' + '\n'.join(videos) + '''
    </div>
  </section>

  <!-- Photo viewer -->
  <dialog id="viewer" class="viewer p-0 m-auto bg-transparent max-w-none max-h-none w-full h-full" aria-label="Photo viewer">
    <div class="absolute inset-0 flex flex-col items-center justify-center p-4 sm:p-10" data-close>
      <figure class="relative max-w-6xl w-full flex flex-col items-center">
        <img id="viewerImg" src="" alt="" class="max-h-[78vh] w-auto max-w-full rounded-[16px] object-contain shadow-[0_30px_80px_-20px_rgba(0,0,0,0.6)]">
        <figcaption class="mt-4 text-center text-white">
          <span id="viewerCap" class="block font-display font-semibold text-lg"></span>
          <span id="viewerCount" class="block text-sm text-white/70 mt-0.5"></span>
        </figcaption>
      </figure>
    </div>
    <button type="button" id="viewerClose" class="viewer-btn absolute top-4 right-4" aria-label="Close">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>
    </button>
    <button type="button" id="viewerPrev" class="viewer-btn absolute left-3 sm:left-6 top-[calc(50%-22px)]" aria-label="Previous photo">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M15 6l-6 6 6 6" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>
    </button>
    <button type="button" id="viewerNext" class="viewer-btn absolute right-3 sm:right-6 top-[calc(50%-22px)]" aria-label="Next photo">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M9 6l6 6-6 6" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>
    </button>
  </dialog>
'''

css = '''
  /* Gallery */
  .photo img { will-change: transform; }
  .viewer::backdrop { background: rgba(14,24,23,0.92); }
  .viewer[open] { animation: viewerIn .3s cubic-bezier(.22,1,.36,1); }
  @keyframes viewerIn { from { opacity: 0; } to { opacity: 1; } }
  .viewer-btn { width: 44px; height: 44px; display: flex; align-items: center; justify-content: center; border-radius: 9999px;
    background: rgba(255,255,255,0.12); color: #fff; transition: background-color .2s ease, transform .2s cubic-bezier(.34,1.56,.64,1); }
  .viewer-btn:hover { background: rgba(255,255,255,0.22); }
  .viewer-btn:active { transform: scale(0.94); }
  .viewer-btn:focus-visible { outline: 2px solid #6FB3A3; outline-offset: 3px; }
'''

js = '''
  // Photo viewer: click a photo to open it; arrows, arrow keys or swipe to move; Esc, x or the backdrop to close
  (function () {
    var dialog = document.getElementById('viewer');
    if (!dialog || typeof dialog.showModal !== 'function') return;
    var tiles = Array.prototype.slice.call(document.querySelectorAll('.photo'));
    var img = document.getElementById('viewerImg'), cap = document.getElementById('viewerCap'), count = document.getElementById('viewerCount');
    var current = 0, opener = null;
    function show(i) {
      current = (i + tiles.length) % tiles.length;
      var t = tiles[current], im = t.querySelector('img');
      img.src = im.src; img.alt = im.alt;
      cap.textContent = t.querySelector('.font-display').textContent;
      count.textContent = (current + 1) + ' of ' + tiles.length;
    }
    tiles.forEach(function (t, i) {
      t.addEventListener('click', function () { opener = t; show(i); dialog.showModal(); });
    });
    var single = tiles.length < 2;
    document.getElementById('viewerPrev').hidden = single;
    document.getElementById('viewerNext').hidden = single;
    document.getElementById('viewerPrev').addEventListener('click', function () { show(current - 1); });
    document.getElementById('viewerNext').addEventListener('click', function () { show(current + 1); });
    document.getElementById('viewerClose').addEventListener('click', function () { dialog.close(); });
    dialog.addEventListener('click', function (e) { if (e.target.hasAttribute && e.target.hasAttribute('data-close')) dialog.close(); });
    dialog.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowLeft') show(current - 1);
      if (e.key === 'ArrowRight') show(current + 1);
    });
    var x0 = null;
    dialog.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; }, { passive: true });
    dialog.addEventListener('touchend', function (e) {
      if (x0 === null) return;
      var dx = e.changedTouches[0].clientX - x0; x0 = null;
      if (Math.abs(dx) > 50) show(current + (dx < 0 ? 1 : -1));
    });
    dialog.addEventListener('close', function () { if (opener) opener.focus(); });
  })();
'''

build('gallery.html',
      'Clinic facilities — SWIFT Emergency &amp; Urgent Care, Rouse Hill',
      'Photos and videos of SWIFT Emergency &amp; Urgent Care in Rouse Hill, NSW: reception, the kids and family waiting area and more.',
      main, active=None, css=css, js=js)
