import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from build_page import build, ROOT, intro, CARD, H2, BTN_PRIMARY

BULK = '<span class="chip chip-solid">Bulk-billed</span>'
EXTRA = '<span class="text-[15px] text-ink/70">Extra charges</span>'

def price(amount, medicare=True):
    tail = ' <span class="block sm:inline text-sm font-normal text-ink/65">+ Medicare</span>' if medicare else ''
    return '<span class="font-display font-bold text-lg text-ink tabular-nums">' + amount + '</span>' + tail

def rows(items):
    out = []
    for i, (label, sub, cost) in enumerate(items):
        border = '' if i == len(items) - 1 else ' border-b border-line'
        subhtml = '<span class="block text-sm text-ink/65 mt-0.5">' + sub + '</span>' if sub else ''
        out.append('          <tr class="align-top' + border + '">\n'
                   '            <th scope="row" class="text-left font-normal py-4 pr-4"><span class="text-[15px] text-ink">' + label + '</span>' + subhtml + '</th>\n'
                   '            <td class="text-right py-4 whitespace-nowrap">' + cost + '</td>\n          </tr>')
    return '\n'.join(out)

def table(tid, heading, intro, items, caption):
    return '''
      <section id="%s" class="scroll-mt-[125px] sm:scroll-mt-[129px]">
        <h2 class="font-display font-bold text-2xl sm:text-3xl leading-[1.12] tracking-[-0.02em] text-ink">%s</h2>
        %s
        <div class="mt-4 %s px-5 sm:px-6">
          <table class="w-full">
            <caption class="sr-only">%s</caption>
            <thead><tr class="border-b border-line text-sm text-ink/65"><th scope="col" class="text-left font-normal py-3">Service</th><th scope="col" class="text-right font-normal py-3">Cost</th></tr></thead>
            <tbody>
%s
            </tbody>
          </table>
        </div>
      </section>''' % (tid, heading, ('<p class="text-ink/70 mt-2 leading-[1.7]">' + intro + '</p>') if intro else '', CARD, caption, rows(items))

# Item 6 (Dr Manivel, 3 Oct): what Medicare covers, pathology, how you pay. Client wording, exact.
MEDICARE_COVERS = ['Doctor consultation', 'Any procedures performed']
PATHOLOGY = ['Bloods, swabs and urine tests',
             'Collected on site by your treating team',
             'Processed in Australian clinical labs',
             'Medicare card holders: bulk billed, no pathology charge',
             'No Medicare card: extra charge, paid separately',
             'Australian Clinical Labs (ACL) sends you its own invoice after your test']
PAY_MEDICARE = ['Pay one amount: facility fee + Medicare charges', 'Get an instant refund of the Medicare part only']
PAY_NO_MEDICARE = ['Pay one amount on discharge: facility fee + Medicare-equivalent charges', 'Pathology is billed separately by ACL']

def bullets(items, dot='bg-teal500'):
    return '<ul class="mt-3 space-y-2 text-[15px] text-ink/80 leading-snug">' + ''.join(
        '<li class="flex gap-2.5"><span class="shrink-0 mt-[7px] w-1.5 h-1.5 rounded-full %s" aria-hidden="true"></span><span>%s</span></li>' % (dot, i) for i in items) + '</ul>'

emergency = table('emergency', 'Emergency &amp; urgent care', 'Walk-in visits for illness and injury.', [
    ('First visit', 'SWIFT facility fee', price('$396')),
    ('Return visit for the same issue', 'Within 24 hours', BULK),
    ('Return visit for the same issue', '2 to 7 days later', price('$150')),
], 'Emergency and urgent care fees')

infusion = table('infusion', 'Infusion clinic', 'By appointment.', [
    ('Iron infusion', 'You bring your own Ferinject or iron medicine', price('$246')),
    ('Iron infusion', 'We supply Ferinject 1g for $77', price('$246 + $77')),
    ('IV antibiotics', 'After a SWIFT consultation, or prescribed by your GP', price('$150')),
    ('Other infusions', None, '<a href="tel:0288599099" class="inline-block py-1 focus-ring rounded text-[15px] font-medium text-teal700 hover:text-teal900 underline underline-offset-2 decoration-teal500/40 hover:decoration-teal700">Call us</a>'),
], 'Infusion clinic fees')

wound = table('wound', 'Wound care clinic', None, [
    ('Simple wound care or dressing', None, price('$80')),
    ('Complex wound care or dressing', None, price('$140')),
    ('Stitches removal', None, price('$80')),
], 'Wound care clinic fees')

radiology = '''
      <section id="radiology" class="scroll-mt-[125px] sm:scroll-mt-[129px]">
        <h2 class="font-display font-bold text-2xl sm:text-3xl leading-[1.12] tracking-[-0.02em] text-ink">Scans and imaging</h2>
        <p class="text-ink/70 mt-2 leading-[1.7]">Provided on-site by Imaging Specialists, an independent practice. Questions about scans: <a href="tel:0286148400" class="focus-ring rounded font-medium text-teal700 hover:text-teal900">(02) 8614 8400</a>.</p>
        <div class="mt-4 %s px-5 sm:px-6">
          <table class="w-full">
            <caption class="sr-only">Radiology hours and fees for patients with Medicare</caption>
            <thead><tr class="border-b border-line text-sm text-ink/65"><th scope="col" class="text-left font-normal py-3">Scan and hours</th><th scope="col" class="text-right font-normal py-3">With Medicare</th></tr></thead>
            <tbody>
%s
            </tbody>
          </table>
        </div>
        <p class="mt-3 text-sm text-ink/70">Without Medicare, extra charges apply to all scans. These fees apply to patients seen at SWIFT.</p>
      </section>''' % (CARD, rows([
    ('X-ray and CT', 'Every day, 10am to 9pm', BULK),
    ('Ultrasound', 'Monday to Friday, 10am to 5pm', BULK),
    ('Ultrasound, after hours', 'Monday to Friday, 5pm to 8pm', EXTRA),
    ('Ultrasound, weekends', 'Saturday and Sunday, subject to availability', EXTRA),
    ('MRI', 'Subject to availability', EXTRA),
]))

FEE_ASIDE = '''          <!-- Headline fee -->
          <div class="relative overflow-hidden rounded-[20px] bg-gradient-to-br from-foam to-mint p-6 sm:p-8">
            <svg class="absolute -right-6 -top-6 w-36 h-36 text-teal900/[0.07]" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="0.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 2.5h10v19l-2.5-1.5-2 1.5-2-1.5-2.5 1.5V2.5Z"/><path d="M9.5 8h5M9.5 11.5h5M9.5 15h3"/></svg>
            <p class="relative text-ink/70">Walk-in visit, facility fee</p>
            <p class="relative font-display font-extrabold text-6xl sm:text-7xl tracking-[-0.04em] text-ink mt-2">$396</p>
            <p class="relative text-ink/70 mt-2">plus standard Medicare charges</p>
          </div>'''

pathology = '''
      <section id="pathology" class="scroll-mt-[125px] sm:scroll-mt-[129px]">
        <h2 class="font-display font-bold text-2xl sm:text-3xl leading-[1.12] tracking-[-0.02em] text-ink">Pathology</h2>
        <div class="mt-4 %s p-5 sm:p-6">
          %s
        </div>
      </section>''' % (CARD, bullets(PATHOLOGY))

main = '''
%s
  <section class="max-w-6xl mx-auto px-5 sm:px-8 pb-16 sm:pb-24">
    <div class="grid lg:grid-cols-[200px_1fr] gap-8 lg:gap-12 items-start">

      <!-- Jump menu -->
      <nav aria-label="On this page" class="lg:sticky lg:top-[132px] -mx-5 px-5 lg:mx-0 lg:px-0 overflow-x-auto">
        <ul class="flex lg:flex-col gap-2 lg:gap-1 text-[15px] whitespace-nowrap pb-1">
          <li><a href="#medicare" class="jump-link focus-ring block rounded-full lg:rounded-lg border border-line lg:border-0 bg-white lg:bg-transparent px-4 lg:px-3 py-1.5 lg:py-2 text-ink/75 hover:text-teal900 hover:bg-white active:scale-[0.97] transition-[transform,background-color,color] duration-200">How you pay</a></li>
          <li><a href="#emergency" class="jump-link focus-ring block rounded-full lg:rounded-lg border border-line lg:border-0 bg-white lg:bg-transparent px-4 lg:px-3 py-1.5 lg:py-2 text-ink/75 hover:text-teal900 hover:bg-white active:scale-[0.97] transition-[transform,background-color,color] duration-200">Urgent care</a></li>
          <li><a href="#pathology" class="jump-link focus-ring block rounded-full lg:rounded-lg border border-line lg:border-0 bg-white lg:bg-transparent px-4 lg:px-3 py-1.5 lg:py-2 text-ink/75 hover:text-teal900 hover:bg-white active:scale-[0.97] transition-[transform,background-color,color] duration-200">Pathology</a></li>
          <li><a href="#infusion" class="jump-link focus-ring block rounded-full lg:rounded-lg border border-line lg:border-0 bg-white lg:bg-transparent px-4 lg:px-3 py-1.5 lg:py-2 text-ink/75 hover:text-teal900 hover:bg-white active:scale-[0.97] transition-[transform,background-color,color] duration-200">Infusions</a></li>
          <li><a href="#wound" class="jump-link focus-ring block rounded-full lg:rounded-lg border border-line lg:border-0 bg-white lg:bg-transparent px-4 lg:px-3 py-1.5 lg:py-2 text-ink/75 hover:text-teal900 hover:bg-white active:scale-[0.97] transition-[transform,background-color,color] duration-200">Wound care</a></li>
          <li><a href="#radiology" class="jump-link focus-ring block rounded-full lg:rounded-lg border border-line lg:border-0 bg-white lg:bg-transparent px-4 lg:px-3 py-1.5 lg:py-2 text-ink/75 hover:text-teal900 hover:bg-white active:scale-[0.97] transition-[transform,background-color,color] duration-200">Scans</a></li>
          <li><a href="#extras" class="jump-link focus-ring block rounded-full lg:rounded-lg border border-line lg:border-0 bg-white lg:bg-transparent px-4 lg:px-3 py-1.5 lg:py-2 text-ink/75 hover:text-teal900 hover:bg-white active:scale-[0.97] transition-[transform,background-color,color] duration-200">Other costs</a></li>
        </ul>
      </nav>

      <div class="space-y-12 max-w-3xl">

      <!-- How you pay (item 6, block C) and what Medicare charges cover (block A) -->
      <section id="medicare" class="scroll-mt-[125px] sm:scroll-mt-[129px]">
        <h2 class="font-display font-bold text-2xl sm:text-3xl leading-[1.12] tracking-[-0.02em] text-ink">How you pay</h2>
        <div class="mt-4 grid sm:grid-cols-2 gap-4">
          <div class="%s p-5 sm:p-6">
            <h3 class="font-display font-semibold text-lg text-ink">Medicare card holders</h3>
            %s
          </div>
          <div class="%s p-5 sm:p-6">
            <h3 class="font-display font-semibold text-lg text-ink">No Medicare card</h3>
            %s
          </div>
        </div>
        <div class="mt-4 rounded-[20px] bg-gradient-to-br from-foam to-mint p-5 sm:p-6">
          <h3 class="font-display font-semibold text-ink">What Medicare charges cover</h3>
          %s
        </div>
      </section>
%s
%s
%s
%s

      <!-- Other costs -->
      <section id="extras" class="scroll-mt-[125px] sm:scroll-mt-[129px]">
        <h2 class="font-display font-bold text-2xl sm:text-3xl leading-[1.12] tracking-[-0.02em] text-ink">Other costs</h2>
        <p class="text-ink/70 mt-2 leading-relaxed">Depending on your treatment, you may need items like crutches or a moon boot. These cost extra.</p>
      </section>

      <!-- Questions -->
      <div class="rounded-[28px] bg-teal900 text-white p-6 sm:p-10 flex flex-col sm:flex-row sm:items-center gap-5 justify-between shadow-[0_24px_48px_-24px_rgba(30,69,63,0.6)]">
        <div>
          <h2 class="font-display font-bold text-2xl sm:text-3xl leading-[1.12] tracking-[-0.02em]">Questions about fees?</h2>
          <p class="text-white/75 mt-1">Call us before you come in and we'll talk you through it.</p>
        </div>
        <a href="tel:0288599099" class="focus-ring spring shrink-0 inline-flex items-center justify-center rounded-full bg-white text-teal900 hover:bg-mint hover:scale-[1.03] font-medium px-6 py-3 transition-[transform,background-color] duration-300 active:scale-[0.97]">Call (02) 8859 9099</a>
      </div>

      </div>
    </div>
  </section>
''' % (intro('Fees', 'Fees', "What you'll pay at SWIFT, with or without a Medicare card. No referral needed.", FEE_ASIDE), CARD, bullets(PAY_MEDICARE), CARD, bullets(PAY_NO_MEDICARE), bullets(MEDICARE_COVERS), emergency + pathology, infusion, wound, radiology)

build('fees.html',
      'Fees — SWIFT Emergency &amp; Urgent Care, Rouse Hill',
      'SWIFT fees for specialist urgent care, infusions, wound care and on-site imaging, with and without Medicare. Walk-in facility fee $396 plus Medicare charges.',
      main, active='fees.html')
