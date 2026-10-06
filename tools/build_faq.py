import sys, os, re, html, json; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from build_page import build, ROOT, intro, H2

# FAQs: one list for the FAQ page and the homepage. Answers use only facts already on the site;
# the newer ones are drafts for SWIFT to review (6 Oct meeting). HOME marks the five shown on the homepage,
# in HOME order. Running this script rewrites faq.html and the homepage FAQ block and its search-engine data.
L = 'font-medium text-teal700 hover:text-teal900 underline underline-offset-2 decoration-teal500/40 hover:decoration-teal700 focus-ring rounded'
def a(href, text): return '<a href="%s" class="%s">%s</a>' % (href, L, text)

GROUPS = [
  ('visiting', 'Visiting SWIFT', [
    ('appointment', 'Do I need an appointment?',
     ["No. For urgent illness or injury you can walk in any time we're open. The only exception is the infusion clinic, which is by appointment."]),
    ('hours', 'What are your opening hours?',
     ['Every day, 10am to 10pm. The last patient registration is at 9pm.']),
    ('ages', 'What ages does SWIFT treat?',
     ['Patients aged 3 months and up, from minor injuries to non-life-threatening illness.',
      'For a baby under 3 months, call 000 or go to your nearest hospital emergency department.']),
    ('referral', 'Do I need a referral?',
     ['No. You can walk in without a referral from your GP.']),
    ('bring', 'What should I bring?',
     ['Your Medicare card, if you have one, and a debit or credit card. SWIFT is cashless.']),
    ('wait', 'How long will I wait?',
     ['It depends on how busy we are. A triage nurse sees you first, and patients are seen in order of urgency, using the Australian Triage Scale. Call us on ' + a('tel:0288599099', '(02) 8859 9099') + " to check today's wait before you come in."]),
  ]),
  ('fees', 'Fees', [
    ('cost', 'How much does a visit cost?',
     ['A walk-in visit is a $396 facility fee plus standard Medicare charges for the doctor consultation and any procedures. Reception explains the fees before you are seen. ' + a('fees.html', 'See detailed pricing') + '.']),
    ('bulk-billed', 'Is SWIFT bulk billed?',
     ['No. SWIFT is a private clinic, so the facility fee applies to every walk-in visit. With a Medicare card, pathology and X-ray, CT and weekday ultrasound are bulk billed.']),
    ('medicare', 'Do I need a Medicare card?',
     ['No. Without a Medicare card you pay the facility fee plus Medicare-equivalent charges when you leave. Pathology and scans are invoiced separately by Australian Clinical Labs (ACL) and Imaging Specialists.']),
    ('return', 'Is a return visit charged?',
     ['A return visit for the same issue within 24 hours is bulk billed.']),
  ]),
  ('care', 'Care at SWIFT', [
    ('different', 'How is SWIFT different from a medical centre or hospital ED?',
     ['SWIFT is an emergency physician-led urgent care clinic for non-life-threatening cases. It sits in between a medical centre and a hospital-grade emergency department in regards to services provided, care offered and complexity of patients seen.',
      'SWIFT can manage more complex patients that are usually not managed in GP-led medical centres. However, for all life-threatening emergencies, patients will need to call 000 or present to the nearest emergency department.']),
    ('000', 'When should I call 000 instead?',
     ['Call 000 for anything life-threatening or getting worse fast: signs of a heart attack or stroke, someone unconscious or not breathing, struggling to breathe, severe bleeding, or a major injury. Don&rsquo;t drive yourself to SWIFT.']),
    ('tests', 'Are X-ray and pathology on site?',
     ['Yes. Pathology is collected on site during your visit. X-ray, CT and ultrasound are in the same building, run by Imaging Specialists, an independent practice. ' + a('services.html#imaging', 'About on-site imaging') + '.']),
    ('infusion', 'Can I book an infusion?',
     ['Yes. Infusions are the only care SWIFT books ahead, including iron infusions (about an hour), zoledronate and IV antibiotics. ' + a('request-appointment.html?service=infusion', 'Request an infusion') + " and we'll confirm a time."]),
  ]),
]
HOME = ['appointment', 'cost', 'hours', 'ages', 'different']

ALL = {q[0]: q for g in GROUPS for q in g[2]}

def item(q, open_=False, last=False):
    qid, question, paras = q
    ps = ''.join('\n          <p class="text-ink/70 pr-8 %s">%s</p>' % (('pb-4' if i == len(paras) - 1 else '') + (' mt-3' if i else ''), p) for i, p in enumerate(paras))
    return ('''        <details id="q-%s" class="faq-item scroll-mt-[125px] border-b border-line py-1%s"%s>
          <summary class="focus-ring flex items-center justify-between gap-4 py-3">
            <span class="font-medium text-ink">%s</span>
            <span class="plus text-teal700 text-xl leading-none shrink-0" aria-hidden="true">+</span>
          </summary>%s
        </details>''' % (qid, ' last:border-b-0' if last else '', ' open' if open_ else '', question, ps))

def schema(qs):
    def plain(t): return html.unescape(re.sub(r'<[^>]+>', '', t))
    data = {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': plain(q[1]), 'acceptedAnswer': {'@type': 'Answer', 'text': ' '.join(plain(p) for p in q[2])}} for q in qs]}
    return '<script type="application/ld+json">\n' + json.dumps(data, indent=2, ensure_ascii=False) + '\n</script>'

# ---- FAQ page --------------------------------------------------------------------------------
sections = []
for gid, title, qs in GROUPS:
    sections.append('''
      <section id="%s" class="scroll-mt-[125px] sm:scroll-mt-[129px]" aria-labelledby="%sHeading">
        <h2 id="%sHeading" class="%s">%s</h2>
        <div class="mt-4 bg-white rounded-[20px] border border-line px-5 sm:px-7">
%s
        </div>
      </section>''' % (gid, gid, gid, H2, title, '\n'.join(item(q, last=(i == len(qs) - 1)) for i, q in enumerate(qs))))

aside = ('<p class="text-ink/70 leading-[1.7]">Can&rsquo;t find your answer? Call us on ' + a('tel:0288599099', '(02) 8859 9099') +
         '. In a life-threatening emergency, call ' + a('tel:000', '000') + '.</p>')
main = intro('FAQs', 'Frequently asked questions', 'Visiting SWIFT, fees, and the care we provide.', '        ' + aside) + '''
  <div class="max-w-6xl mx-auto px-5 sm:px-8 pb-16 sm:pb-24">
    <div class="max-w-3xl space-y-12 sm:space-y-16">''' + ''.join(sections) + '''
    </div>
  </div>
'''
css = '''
  /* FAQ accordions */
  .faq-item summary { list-style: none; cursor: pointer; }
  .faq-item summary::-webkit-details-marker { display: none; }
  .faq-item summary:hover span:first-child { color: #1E453F; }
  .faq-item .plus { transition: transform 0.2s ease; }
  .faq-item[open] .plus { transform: rotate(45deg); }
'''
js = '''
  // Deep link: faq.html#q-cost opens that question
  (function () {
    var t = location.hash && document.getElementById(location.hash.slice(1));
    if (t && t.tagName === 'DETAILS') t.open = true;
  })();
'''
build('faq.html',
      'FAQs — SWIFT Emergency &amp; Urgent Care, Rouse Hill',
      'Answers about visiting SWIFT Emergency &amp; Urgent Care in Rouse Hill: appointments, opening hours, ages, fees, Medicare and on-site tests.',
      main, active=None, css=css, js=js)
# Search-engine data for every question
page = open(ROOT + 'faq.html').read()
page = page.replace('</head>', schema(list(ALL.values())) + '\n</head>', 1)
open(ROOT + 'faq.html', 'w').write(page)

# ---- Homepage: the five HOME questions and their search-engine data ------------------------
home = open(ROOT + 'index.html').read()
qs = [ALL[k] for k in HOME]
block = '\n'.join(item(q, open_=(i == 0), last=(i == len(qs) - 1)) for i, q in enumerate(qs))
home, n1 = re.subn(r'(<!-- FAQ:START[^>]*-->).*?<!-- FAQ:END -->', lambda m: m.group(1) + '\n' + block + '\n        <!-- FAQ:END -->', home, flags=re.S)
home, n2 = re.subn(r'<script type="application/ld\+json">\s*\{\s*"@context": "https://schema.org",\s*"@type": "FAQPage".*?</script>', lambda m: schema(qs), home, flags=re.S)
assert n1 == 1 and n2 == 1, (n1, n2)
open(ROOT + 'index.html', 'w').write(home)
print('updated index.html FAQ block (%d questions)' % len(qs))
