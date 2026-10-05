import sys, html, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from build_page import build, ROOT, intro, H2, BTN_PRIMARY, BTN_SECONDARY

# Names and roles from the current live site. Bios there are placeholder text, so
# 'bio' is left empty until SWIFT supplies real ones; the profile shows a neutral note meanwhile.
# Each person: (slug, name, qualifications, title and position, bio).
# Qualifications show under the name only when filled in (Dr Manivel is supplying them, item 5.3).
DOCTORS = [
  ('vijay-manivel', 'Dr Vijay Manivel', '', 'Co-Founder and Director', ''),
  ('berinder-shahpuri', 'Dr Berinder Shahpuri', '', 'Deputy Clinical Director, Emergency Physician', ''),
  ('gopinath-betarayappa', 'Dr Gopinath Betarayappa', '', 'Co-Founder and Director', ''),
  ('nina-dhaliwal', 'Dr Nina Dhaliwal', '', 'Emergency Physician and Toxicologist', ''),
  ('pramod-chandru', 'Dr Pramod Chandru', '', 'Emergency Physician and Toxicologist', ''),
  ('earl-butler', 'Dr Earl Butler', '', 'Emergency Physician and Toxicologist', ''),
  ('stephen-madden', 'Dr Stephen Madden', '', 'Senior Emergency Doctor', ''),
  ('athar-khan', 'Dr Athar Khan', '', 'Senior Emergency Doctor', ''),
  ('mahesh-jagada-gangadharaiah', 'Dr Mahesh Jagada Gangadharaiah', '', 'Emergency Physician', ''),
  ('behzad-mirmiran', 'Dr Behzad Mirmiran', '', 'Emergency Physician', ''),
  ('nasim-erfani', 'Dr Nasim Erfani', '', 'Emergency Physician', ''),
]
# Item 5.2: Dr Manivel first, Dr Shahpuri second, everyone else A to Z by surname (ignoring 'Dr')
FIXED_FIRST = ['vijay-manivel', 'berinder-shahpuri']
def surname(person): return person[1].split()[-1].lower()
DOCTORS = ([d for f in FIXED_FIRST for d in DOCTORS if d[0] == f] +
           sorted([d for d in DOCTORS if d[0] not in FIXED_FIRST], key=surname))

NURSES = [
  ('gisha-george', 'Gisha George', '', 'Nurse Unit Manager', ''),
  ('farai-mupedzi', 'Farai Mupedzi', '', 'Transitional Nurse Practitioner', ''),
  ('natalie-weitenberg', 'Natalie Weitenberg', '', 'Transitional Nurse Practitioner', ''),
  ('geetha-ganesan', 'Geetha Ganesan', '', 'Emergency Registered Nurse', ''),
  ('stuart-dawkins', 'Stuart Dawkins', '', 'Emergency Registered Nurse', ''),
  ('edsel-de-mesa', 'Edsel de Mesa', '', 'Registered Nurse', ''),
]

# From the current live site's Our Advisors page (photos too, in brand_assets/team/)
ADVISORS = [
  ('lea-mitchell', 'Lea Mitchell', '', 'Director of Nursing', ''),
  ('peter-roberts', 'Dr Peter Roberts', 'FACEM OAM', 'Senior Emergency Physician', ''),
  ('john-adie', 'John Adie', 'FRNZCUC FRACGP FACRRM', 'RNZCUC Australian Convenor', ''),
]

# Item 5.1 section order: Practice Manager, Our Doctors, Our Nurses, Our Admin Staff, Our Advisors,
# Contracting Doctors. Practice Manager, Admin Staff and Contracting Doctors are added once SWIFT
# supplies the names; empty sections are not shown.
ADVISOR_SLUGS = {a[0] for a in ADVISORS}
TEAM = [
  ('Our Doctors', 'Emergency physicians who see every walk-in patient', DOCTORS),
  ('Our Nurses', 'Emergency nurses and nurse practitioners', NURSES),
  ('Our Advisors', 'Experts in their fields, committed to the health of our community', ADVISORS),
]
NO_PHOTO = {'earl-butler'}

def initials(name):
    parts = [p for p in name.replace('Dr ', '').split() if p[0].isupper()]
    return (parts[0][0] + parts[-1][0]).upper()

def photo(slug, name, cls):
    if slug in NO_PHOTO:
        return ('<div class="%s rounded-[14px] bg-gradient-to-b from-foam to-mint flex items-center justify-center"><span class="font-display font-bold text-4xl text-teal700">%s</span></div>' % (cls, initials(name)))
    return ('<div class="%s relative overflow-hidden rounded-[14px] bg-gradient-to-b from-foam to-mint">'
            '<img src="brand_assets/team/%s.jpg" alt="Portrait of %s" loading="lazy" width="480" height="480" class="team-img w-full h-full object-cover object-top mix-blend-multiply"></div>') % (cls, slug, html.escape(name))

def card(slug, name, quals, role, bio):
    return ('''        <li class="flex">
          <button type="button" id="%s" class="team-card card-link group w-full h-full flex flex-col text-left focus-ring rounded-[20px] bg-white border border-line p-2.5 sm:p-3 scroll-mt-[140px]"
            data-slug="%s" data-advisor="%s" data-name="%s" data-quals="%s" data-role="%s" data-bio="%s" data-photo="%s" data-initials="%s" aria-haspopup="dialog">
            %s
            <span class="flex-1 flex flex-col px-2 pt-4 pb-2 sm:px-3">
              <span class="block font-display font-semibold text-[17px] leading-snug text-ink">%s</span>
              %s<span class="block text-sm text-ink/70 mt-1">%s</span>
              <span class="mt-auto pt-3 inline-flex items-center gap-1 text-sm font-medium text-teal700 group-hover:text-teal900">View profile
                <svg class="transition-transform duration-300 group-hover:translate-x-0.5" width="13" height="13" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M9 6l6 6-6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
              </span>
            </span>
          </button>
        </li>''' % (slug, slug, 'true' if slug in ADVISOR_SLUGS else '', html.escape(name), html.escape(quals), html.escape(role), html.escape(bio),
                     '' if slug in NO_PHOTO else 'brand_assets/team/%s.jpg' % slug, initials(name),
                     photo(slug, name, 'aspect-square'), html.escape(name),
                     ('<span class="block text-sm font-medium text-teal700 mt-1">%s</span>' % html.escape(quals)) if quals else '', html.escape(role)))

groups = []
for i, (title, sub, people) in enumerate(TEAM):
    cols = 'grid-cols-2 lg:grid-cols-4'
    groups.append('''
    <section class="%s" aria-labelledby="grp%d">
      <div class="flex items-baseline justify-between flex-wrap gap-x-4 gap-y-1 mb-6">
        <h2 id="grp%d" class="font-display font-bold text-2xl sm:text-3xl leading-[1.12] tracking-[-0.02em] text-ink">%s</h2>
        <p class="text-ink/70">%s</p>
      </div>
      <ul class="grid %s gap-3 sm:gap-5">
%s
      </ul>
    </section>''' % ('' if i == 0 else 'mt-16 sm:mt-20', i, i, title, sub, cols, '\n'.join(card(*p) for p in people)))

main = '''
%s
  <div class="max-w-6xl mx-auto px-5 sm:px-8 pb-16 sm:pb-24">
%s
  </div>

  <!-- Profile dialog -->
  <dialog id="profile" class="team-dialog p-0 m-auto w-[calc(100%%-2rem)] max-w-3xl rounded-[28px] overflow-hidden bg-white text-ink shadow-[0_30px_80px_-20px_rgba(27,39,51,0.55)] backdrop:bg-ink/55 backdrop:backdrop-blur-sm" aria-labelledby="profileName">
    <div class="grid sm:grid-cols-[260px_1fr]">
      <div id="profilePhoto" class="aspect-square sm:aspect-auto sm:h-full bg-mint"></div>
      <div class="relative p-6 sm:p-8">
        <button type="button" id="profileClose" class="focus-ring absolute top-3 right-3 w-10 h-10 flex items-center justify-center rounded-full text-ink/65 hover:text-ink hover:bg-mint active:scale-95 transition-[transform,background-color,color] duration-200" aria-label="Close profile">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>
        </button>
        <h2 id="profileName" class="font-display font-bold text-2xl sm:text-3xl tracking-tight text-ink pr-10"></h2>
        <p id="profileQuals" class="text-teal700 font-medium mt-1"></p>
        <p id="profileRole" class="text-ink/75 mt-1"></p>
        <p id="profileBio" class="mt-5 text-ink/75 leading-relaxed"></p>
        <div id="profileActions" class="mt-7 pt-5 border-t border-line flex flex-wrap gap-3">
          <a href="request-appointment.html" class="focus-ring spring inline-flex items-center justify-center rounded-full font-medium text-[15px] px-5 py-2.5 hover:scale-[1.03] active:scale-[0.97] duration-300 bg-teal900 hover:bg-teal700 text-white transition-[transform,background-color]">Request appointment</a>
          <a href="tel:0288599099" class="focus-ring spring inline-flex items-center justify-center rounded-full font-medium text-[15px] px-5 py-2.5 hover:scale-[1.03] active:scale-[0.97] duration-300 border border-ink/15 bg-white text-ink hover:border-teal700 hover:text-teal900 transition-[transform,border-color,color]">Call (02) 8859 9099</a>
        </div>
      </div>
    </div>
  </dialog>
''' % (intro('Our team', 'Meet the team', 'Experienced emergency physicians and nurses, working with specialists in orthopaedics, cardiology, paediatrics and more.'), '\n'.join(groups))

css = '''
  /* Team */
  .team-img { transition: transform .6s cubic-bezier(.22,1,.36,1); }
  .team-card:hover .team-img { transform: scale(1.04); }
  .team-dialog[open] { animation: dialogIn .35s cubic-bezier(.22,1,.36,1); }
  .team-dialog[open]::backdrop { animation: fadeIn .25s ease; }
  @keyframes dialogIn { from { opacity: 0; transform: translateY(14px) scale(.98); } to { opacity: 1; transform: none; } }
  @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
'''

js = '''  (function () {
    var dialog = document.getElementById('profile');
    if (!dialog || typeof dialog.showModal !== 'function') return;
    var photoEl = document.getElementById('profilePhoto');
    var lastCard = null;

    function open(card, push) {
      var d = card.dataset;
      document.getElementById('profileName').textContent = d.name;
      document.getElementById('profileQuals').textContent = d.quals;
      document.getElementById('profileQuals').hidden = !d.quals;
      document.getElementById('profileRole').textContent = d.role;
      // Advisors don't see patients, so no booking buttons on their profiles
      document.getElementById('profileActions').hidden = d.advisor === 'true';
      document.getElementById('profileBio').textContent = d.bio ||
        'A full profile for ' + d.name + ' is coming soon.';
      photoEl.innerHTML = '';
      if (d.photo) {
        var img = document.createElement('img');
        img.src = d.photo; img.alt = 'Portrait of ' + d.name;
        img.className = 'w-full h-full object-cover object-top';
        photoEl.appendChild(img);
        photoEl.className = 'aspect-square sm:aspect-auto sm:h-full bg-mint';
      } else {
        photoEl.className = 'aspect-square sm:aspect-auto sm:h-full bg-mint flex items-center justify-center';
        photoEl.innerHTML = '<span class="font-display font-bold text-6xl text-teal700">' + d.initials + '</span>';
      }
      lastCard = card;
      dialog.showModal();
      if (push && history.replaceState) history.replaceState(null, '', '#' + d.slug);
    }
    function close() { dialog.close(); }

    document.querySelectorAll('.team-card').forEach(function (card) {
      card.addEventListener('click', function () { open(card, true); });
    });
    document.getElementById('profileClose').addEventListener('click', close);
    // Click on the backdrop closes the dialog
    dialog.addEventListener('click', function (e) { if (e.target === dialog) close(); });
    dialog.addEventListener('close', function () {
      if (history.replaceState) history.replaceState(null, '', location.pathname);
      if (lastCard) lastCard.focus();
    });

    // Deep link: team.html#vijay-manivel opens that profile
    var hash = location.hash.slice(1);
    if (hash) {
      var target = document.getElementById(hash);
      if (target && target.classList.contains('team-card')) open(target, false);
    }
  })();
'''

build('team.html',
      'Our team — SWIFT Emergency &amp; Urgent Care, Rouse Hill',
      'Meet the emergency physicians and nurses at SWIFT Emergency &amp; Urgent Care in Rouse Hill, NSW.',
      main, active=None, css=css, js=js)
