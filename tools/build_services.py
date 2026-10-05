import sys, re, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from build_page import build, ROOT, intro, CARD, H2, BTN_PRIMARY, BTN_SECONDARY

# Service icons, kept here so homepage redesigns can't break this build
ICONS = {
    'emergency-health-care': '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M3 12h3.5l2-5 3 10 2-7 1.5 2H21" stroke="#00728F" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    'specialty-orthopaedics': '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" aria-hidden="true"><g stroke="#00728F" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M7.5 16.5 16.5 7.5"/><circle cx="6" cy="18" r="2.3"/><circle cx="18" cy="6" r="2.3"/></g></svg>',
    'sports-injuries': '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" aria-hidden="true"><g stroke="#00728F" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><circle cx="14.5" cy="5" r="1.8"/><path d="M13 8l-3 3 1 4-3 4M13 8l3 1 2 5M10 11l3-1"/></g></svg>',
    'paediatrics': '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" aria-hidden="true"><g stroke="#00728F" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="13" r="6"/><circle cx="7" cy="6.5" r="2"/><circle cx="17" cy="6.5" r="2"/><path d="M9.5 14c.7.8 1.6 1.2 2.5 1.2s1.8-.4 2.5-1.2"/></g><circle cx="9.5" cy="12" r=".7" fill="#00728F" stroke="none"/><circle cx="14.5" cy="12" r=".7" fill="#00728F" stroke="none"/></svg>',
    'cardiology': '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M12 20s-7-4.6-9.3-9.3C1.2 7.6 3 4.5 6.2 4.2c1.8-.2 3.4.7 4.3 2.1a4.9 4.9 0 0 1 3-2c3.2-.5 5.4 2.6 4 5.9C15.8 15 12 20 12 20Z" stroke="#00728F" stroke-width="1.5" stroke-linejoin="round"/><path d="M6 11h2.5l1.3-2.4L11.5 13l1.2-2h3.3" stroke="#0098BA" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    'infusion-clinic': '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M8 4h8l-1 5H9L8 4Z" stroke="#00728F" stroke-width="1.5" stroke-linejoin="round"/><path d="M9 9h6l-.8 7.5a2.2 2.2 0 0 1-4.4 0L9 9Z" stroke="#00728F" stroke-width="1.5" stroke-linejoin="round"/><path d="M12 17v3" stroke="#00728F" stroke-width="1.5" stroke-linecap="round"/><circle cx="12" cy="21.2" r=".9" fill="#0098BA" stroke="none"/></svg>',
    'physiotherapy': '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M5 16a7 7 0 0 1 12.6-4.2" stroke="#00728F" stroke-width="1.6" stroke-linecap="round"/><path d="M17.6 8.5 18.5 12l-3.6-.7" stroke="#00728F" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/><circle cx="5" cy="16" r="1.4" fill="#0098BA" stroke="none"/></svg>',
    'pathology': '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M10 3h4M10.5 3v11.5a3.5 3.5 0 1 0 3 0V3" stroke="#00728F" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/><path d="M10.5 13.5h3" stroke="#0098BA" stroke-width="1.6" stroke-linecap="round"/></svg>',
    'imaging': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden="true"><rect x="4" y="3.5" width="16" height="17" rx="2" stroke="currentColor" stroke-width="1.7"/><path d="M12 7v10M9 9.5h6M9.5 12.5h5M10 15.5h4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>',
}
def icon_for(slug):
    return ICONS[slug]
DENTAL_ICON = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M12 3c-2.2 0-3.6 1-4.6 1-1.3 0-2.4 1.3-2.4 3.4 0 3 1 5.7 1.6 8.3.4 1.7.8 3.3 2 3.3 1.3 0 1.4-2.6 1.9-4.4.3-1.1.7-2 1.5-2s1.2.9 1.5 2c.5 1.8.6 4.4 1.9 4.4 1.2 0 1.6-1.6 2-3.3.6-2.6 1.6-5.3 1.6-8.3 0-2.1-1.1-3.4-2.4-3.4-1 0-2.4-1-4.6-1Z" stroke="#00728F" stroke-width="1.4" stroke-linejoin="round"/></svg>'

WALK = ('Walk in', 'chip-solid')
APPT = ('By appointment', '')
INDEP = ('Independent provider', 'chip-quiet')

def tag(t): return '<span class="chip %s">%s</span>' % (t[1], t[0])

def btn(href, label, primary=True):
    ext = ' target="_blank" rel="noopener"' if href.startswith('http') else ''
    return '<a href="%s"%s class="%s">%s</a>' % (href, ext, BTN_PRIMARY if primary else BTN_SECONDARY, label)

DIRECTIONS = 'https://www.google.com/maps/dir/?api=1&amp;destination=G38%2C+32+Civic+Way%2C+Rouse+Hill+NSW+2155'
CALL = btn('tel:0288599099', 'Call (02) 8859 9099', False)

# Service photos (most from the current SWIFT site). Decorative: the heading says what the service is.
IMAGES = {
    'emergency':     ('brand_assets/services/emergency.jpg', '50% 55%'),
    'orthopaedics':  ('brand_assets/Treatment.jpeg', '65% 40%'),
    'sports':        ('brand_assets/services/sports.jpg', '50% 40%'),
    'paediatrics':   ('brand_assets/services/paediatrics.jpg', '50% 45%'),
    'cardiology':    ('brand_assets/services/cardiology.jpg', '50% 40%'),
    'infusion':      ('brand_assets/services/infusion.jpg', '50% 40%'),
    'physiotherapy': ('brand_assets/services/physiotherapy.jpg', '50% 62%'),
    'pathology':     ('brand_assets/services/pathology.jpg', '50% 50%'),
    'imaging':       ('brand_assets/services/imaging.jpg', '50% 55%'),
}

def section(sid, name, icon, tags, summary, points, ctas, extra=''):
    pts = ''.join('<li class="flex gap-2.5"><span class="shrink-0 mt-2 w-1.5 h-1.5 rounded-full bg-teal500" aria-hidden="true"></span><span>%s</span></li>' % p for p in points)
    img = IMAGES.get(sid)
    photo = ''
    if img:
        photo = ('''
          <div class="relative h-48 sm:h-64 rounded-[14px] overflow-hidden bg-mint">
            <img src="%s" alt="" loading="lazy" class="absolute inset-0 w-full h-full object-cover" style="object-position:%s">
            <div class="absolute inset-0 bg-teal900 mix-blend-multiply opacity-[0.08]" aria-hidden="true"></div>
            <div class="absolute inset-x-0 bottom-0 h-1/3 bg-gradient-to-t from-black/25 to-transparent" aria-hidden="true"></div>
          </div>''' % img)
    pad = 'p-3 sm:p-3' if img else 'p-5 sm:p-8'
    inner = 'px-2 pt-5 pb-2 sm:px-5 sm:pt-6 sm:pb-5' if img else ''
    return '''
        <article id="%s" class="svc scroll-mt-[125px] sm:scroll-mt-[129px] bg-white rounded-[20px] border border-line shadow-[0_1px_2px_rgba(43,65,92,0.05),0_12px_28px_-20px_rgba(43,65,92,0.35)] %s">%s
          <div class="%s">
          <div class="flex items-start gap-4">
            <span class="shrink-0 hidden sm:flex items-center justify-center w-12 h-12 rounded-full bg-gradient-to-br from-foam to-mint">%s</span>
            <div class="flex-1 min-w-0">
              <div class="flex flex-wrap items-center gap-x-3 gap-y-2">
                <h2 class="font-display font-bold text-xl sm:text-2xl tracking-[-0.02em] text-ink">%s</h2>
                <div class="flex flex-wrap gap-1.5">%s</div>
              </div>
              <p class="mt-2 text-ink/70 leading-relaxed">%s</p>
            </div>
          </div>
          <ul class="mt-5 grid sm:grid-cols-2 gap-x-6 gap-y-2 text-[15px] text-ink/80 leading-relaxed">%s</ul>%s
          <div class="mt-6 pt-5 border-t border-line flex flex-wrap gap-3">%s</div>
          </div>
        </article>''' % (sid, pad, photo, inner, icon, name, ''.join(tag(t) for t in tags), summary, pts, extra, ''.join(ctas))

SWIFT_SERVICES = [
  section('emergency', 'Emergency &amp; urgent care', icon_for('emergency-health-care'), [WALK],
    'Emergency physicians treat minor injuries through to severe, non-life-threatening illness, usually faster than a hospital ED.',
    ['A triage nurse assesses you on arrival, using the Australian Triage Scale',
     'You\'re then seen by a doctor trained in emergency medicine',
     'If you need hospital care, we arrange your transfer to a nearby emergency department',
     'Scans and pathology are in the same building'],
    [btn(DIRECTIONS, 'Get directions'), CALL]),
  section('orthopaedics', 'Fractures &amp; orthopaedics', icon_for('specialty-orthopaedics'), [WALK, APPT],
    'Orthopaedic surgeons follow up fractures and joint injuries, and can arrange surgery at nearby private hospitals if you need it.',
    ['Specialist follow-up within 24 hours if needed',
     'Hip, knee, shoulder, elbow, hand and wrist, and foot and ankle',
     'Walk in with a new injury; follow-up visits are booked'],
    [btn('request-appointment.html?service=ortho', 'Request appointment'), CALL],
    extra='''
          <details class="svc-more mt-5 rounded-[14px] bg-paper border border-line">
            <summary class="focus-ring flex items-center justify-between gap-3 px-4 py-3 text-[15px] font-medium text-ink rounded-[14px] hover:bg-mint/60 transition-colors">Our orthopaedic surgeons
              <svg class="chev shrink-0 transition-transform duration-300" width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M6 9l6 6 6-6" stroke="#00728F" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
            </summary>
            <ul class="px-4 pb-4 grid sm:grid-cols-2 gap-x-6 gap-y-2.5 text-sm">
              <li><span class="block text-ink font-medium">Dr Mohammed Baba</span><span class="text-ink/70">Shoulder, elbow, wrist and hand</span></li>
              <li><span class="block text-ink font-medium">A/Prof Roderick Kuo</span><span class="text-ink/70">Foot and ankle, trauma</span></li>
              <li><span class="block text-ink font-medium">Dr Adrian Low</span><span class="text-ink/70">Shoulder, knee and trauma</span></li>
              <li><span class="block text-ink font-medium">Dr Jun Nagamori</span><span class="text-ink/70">Sports knee surgery</span></li>
              <li><span class="block text-ink font-medium">A/Prof Nicholas C Smith</span><span class="text-ink/70">Hand and wrist</span></li>
              <li><span class="block text-ink font-medium">Dr Louis Shidiak</span><span class="text-ink/70">Hip and knee surgery, sports injuries</span></li>
              <li><span class="block text-ink font-medium">A/Prof James Sullivan</span><span class="text-ink/70">Hip and knee surgery, joint replacement</span></li>
              <li><span class="block text-ink font-medium">Dr Timothy Yeoh</span><span class="text-ink/70">Knee and shoulder surgery</span></li>
            </ul>
          </details>'''),
  section('sports', 'Sports injuries', icon_for('sports-injuries'), [WALK],
    'Emergency physicians, orthopaedic surgeons and physiotherapists treat sports injuries and plan your return to play.',
    ['Saturday morning sports injury clinic, 10am to 1pm',
     'X-ray, ultrasound and MRI to find the extent of the injury',
     'A recovery plan, with physiotherapy if you need it',
     'Advice on preventing the next injury'],
    [btn(DIRECTIONS, 'Get directions'), CALL]),
  section('paediatrics', 'Paediatrics', icon_for('paediatrics'), [WALK, APPT],
    'Specialist urgent care for children 3 months and up, with follow-up clinics so care doesn\'t stop when you go home.',
    ['Walk in when your child is sick or hurt',
     'Paediatric follow-up clinics, booked ahead',
     'Specialist care through Children\'s Health Hub, run by paediatricians affiliated with The Children\'s Hospital at Westmead',
     'Newborns to teenagers, including allergy, gastroenterology, surgery and dietetics'],
    [btn('request-appointment.html', 'Request appointment'), CALL]),
  section('cardiology', 'Cardiology', icon_for('cardiology'), [WALK],
    'A fast-track pathway for low-risk chest pain, once our emergency team has assessed you as safe.',
    ['Urgent review by a specialist cardiologist',
     'Exercise stress test and echocardiogram',
     'Transfer to a nearby hospital if you need admission'],
    [CALL],
    extra='''
          <p class="mt-5 flex gap-2.5 rounded-[14px] bg-urgent/[0.07] border border-urgent/20 px-4 py-3 text-[15px] text-urgentDk">
            <svg class="shrink-0 mt-0.5" width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M12 9v4M12 16.5h.01M10.29 3.86 1.82 18a1.5 1.5 0 0 0 1.3 2.25h17.76a1.5 1.5 0 0 0 1.3-2.25L13.71 3.86a1.5 1.5 0 0 0-2.42 0Z" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>
            <span>Severe or crushing chest pain, or chest pain with shortness of breath, can be life-threatening. <a href="tel:000" class="font-semibold underline underline-offset-2 focus-ring rounded">Call 000</a>.</span>
          </p>'''),
  section('infusion', 'Infusion clinic', icon_for('infusion-clinic'), [APPT],
    'Infusions for adults and children in a monitored setting, supervised by a senior emergency physician.',
    ['<strong class="font-medium text-ink">Iron infusion</strong>: about 1 hour. Bring your Ferinject from the pharmacy, or we can supply it',
     '<strong class="font-medium text-ink">Zoledronate</strong> for osteoporosis or high calcium: under 1 hour',
     '<strong class="font-medium text-ink">IV antibiotics</strong> after a SWIFT visit or on your GP\'s prescription',
     'Open 10am to 10pm, every day'],
    [btn('request-appointment.html?service=infusion', 'Request appointment'), btn('fees.html#infusion', 'See infusion fees', False)],
    extra='''
          <details class="svc-more mt-5 rounded-[14px] bg-paper border border-line">
            <summary class="focus-ring flex items-center justify-between gap-3 px-4 py-3 text-[15px] font-medium text-ink rounded-[14px] hover:bg-mint/60 transition-colors">Before a zoledronate infusion
              <svg class="chev shrink-0 transition-transform duration-300" width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M6 9l6 6 6-6" stroke="#00728F" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
            </summary>
            <ul class="px-4 pb-4 space-y-1.5 text-sm text-ink/75 list-disc pl-8">
              <li>Stop oral osteoporosis tablets (oral bisphosphonates)</li>
              <li>Keep taking daily calcium and vitamin D</li>
              <li>Finish any dental work first</li>
              <li>Drink plenty of fluids on the day</li>
            </ul>
          </details>'''),
  section('physiotherapy', 'Physiotherapy', icon_for('physiotherapy'), [APPT],
    'On-site physiotherapists follow up muscle, bone and joint injuries, working alongside our orthopaedic team.',
    ['Recovery after an injury or procedure',
     'Follow-up for fractures, sprains and sports injuries'],
    [btn('request-appointment.html?service=physio', 'Request appointment'), CALL]),
  section('pathology', 'Pathology', icon_for('pathology'), [WALK],
    'An in-house lab collects samples during your visit, so results come back faster and treatment isn\'t held up.',
    ['Blood and other tests taken on-site',
     'Results go straight to your SWIFT doctor'],
    [btn(DIRECTIONS, 'Get directions'), CALL]),
]

INDEPENDENT = [
  section('imaging', 'Imaging &amp; radiology', icon_for('imaging'), [INDEP],
    'X-ray, CT, ultrasound and MRI in the same building, run by Imaging Specialists, an independent practice.',
    ['X-ray and CT every day, 10am to 9pm',
     'Ultrasound weekdays 10am to 5pm, plus after-hours sessions',
     'MRI, subject to availability',
     'Interventional radiology for back, shoulder and joint pain'],
    [btn('tel:0286148400', 'Call Imaging Specialists'), btn('fees.html#radiology', 'See scan fees', False)]),
  section('dental', 'Dental', DENTAL_ICON, [INDEP],
    'An independent dental practice shares our building, for general and emergency dental care.',
    ['Toothache, broken teeth and dental emergencies',
     'Book with the dental practice directly'],
    []).replace('<div class="mt-6 pt-5 border-t border-line flex flex-wrap gap-3"></div>', ''),
]

index_links = [('emergency','Emergency'),('orthopaedics','Orthopaedics'),('sports','Sports injuries'),('paediatrics','Paediatrics'),('cardiology','Cardiology'),('infusion','Infusions'),('physiotherapy','Physiotherapy'),('pathology','Pathology'),('imaging','Imaging'),('dental','Dental')]
jump = '\n'.join('          <li><a href="#%s" class="jump-link focus-ring block rounded-full lg:rounded-lg border border-line lg:border-0 bg-white lg:bg-transparent px-4 lg:px-3 py-1.5 lg:py-2 text-ink/75 hover:text-teal900 hover:bg-white active:scale-[0.97] transition-[transform,background-color,color] duration-200">%s</a></li>' % l for l in index_links)

main = '''
%s
  <section class="max-w-6xl mx-auto px-5 sm:px-8 pb-16 sm:pb-24">
    <div class="grid lg:grid-cols-[200px_1fr] gap-8 lg:gap-12 items-start">
      <nav aria-label="Services on this page" class="lg:sticky lg:top-[132px] -mx-5 px-5 lg:mx-0 lg:px-0 overflow-x-auto">
        <ul class="flex lg:flex-col gap-2 lg:gap-1 text-[15px] whitespace-nowrap pb-1">
%s
        </ul>
      </nav>

      <div class="max-w-3xl">
        <div class="space-y-5">
%s
        </div>

        <div class="mt-14">
          <h2 class="font-display font-bold text-2xl sm:text-3xl leading-[1.12] tracking-[-0.02em] text-ink">Also in this building</h2>
          <p class="text-ink/70 mt-2 mb-6 leading-[1.7]">Independent practices, not part of SWIFT's clinical team. Book with them directly.</p>
          <div class="space-y-5">
%s
          </div>
        </div>
      </div>
    </div>
  </section>
''' % (intro('Services', 'Services', 'Everything we treat and offer at Rouse Hill, led by emergency physicians and working with specialists.'), jump, '\n'.join(SWIFT_SERVICES), '\n'.join(INDEPENDENT))

css = '''
  /* Services */
  .svc-more summary { list-style: none; cursor: pointer; }
  .svc-more summary::-webkit-details-marker { display: none; }
  .svc-more[open] .chev { transform: rotate(180deg); }
  .svc:target { box-shadow: 0 0 0 2px #0098BA, 0 14px 28px -10px rgba(43,65,92,0.25); }
'''

build('services.html',
      'Services — SWIFT Emergency &amp; Urgent Care, Rouse Hill',
      'Emergency and specialist urgent care, orthopaedics, sports injuries, paediatrics, cardiology, infusions, physiotherapy and pathology at SWIFT Rouse Hill.',
      main, active='services.html', css=css)
