# SWIFT Emergency & Urgent Care — Website Redesign

A from-scratch, patient-centric redesign of the SWIFT Emergency & Urgent Care homepage (Rouse Hill, NSW). Currently a single-page static build (`index.html`) — no framework or build step.

## Running locally

Requires [Node.js](https://nodejs.org) (v18+).

```
npm install
node serve.mjs
```

Then open **http://localhost:3000**.

## Branches

| Branch | What it is |
|---|---|
| `main` | The real website. Only patient-facing code goes here — this is what gets deployed live. |
| `demo` | `main` plus the client demo tools: the guided tour, campaign preview and desktop/tablet/mobile preview. Used for client demos only. |

The demo tools live in `demo/` on the `demo` branch, and each page loads them with one line: `<script src="demo/demo.js" defer></script>`. Nothing demo-related is on `main`.

Day-to-day work happens on `demo`, so every change can be shown to the client with the demo tools. `main` only changes once a change is approved:

1. Commit website changes on `demo`. Keep them in **separate commits** from changes to the demo tools (`demo/` and the demo script tags) — never mix the two in one commit.
2. When changes are approved, copy just those commits onto `main` and push:
   ```
   git checkout main
   git cherry-pick <commit> [<commit> ...]
   git push
   git checkout demo
   git merge main
   ```
   The final merge keeps the two branches in sync, so later cherry-picks stay clean.
3. Never merge `demo` into `main` — that would bring the demo tools onto the live site.

If you add a page, add the demo script tag to it on `demo` in its own commit (generated pages get it from `tools/build_page.py` on that branch).

## Screenshot tooling

Two Puppeteer scripts for visual review — always screenshot from `localhost`, never a `file://` URL:

```
node screenshot.mjs http://localhost:3000 [label]     # desktop, full page
node mobile_shot.mjs http://localhost:3000 [label]     # mobile viewport, full page
```

Screenshots save to `./temporary screenshots/` (git-ignored, auto-incremented filenames).

## Project structure

```
index.html          Single-page homepage — all markup, Tailwind (CDN), and JS inline
serve.mjs            Local static file server (port 3000)
screenshot.mjs        Desktop screenshot tool
mobile_shot.mjs       Mobile-viewport screenshot tool
brand_assets/         Logo marks and real clinic photography
```

## Brand assets

- `SWIFT_7.png` (full colour logo) and `SwiftLogoA.jpg` (round mark): the official logos, supplied by SWIFT. Web versions in `logo/`: `swift-logo.png` (header and password screen), `swift-mark.png` (the cross alone, for the footer and the Come to SWIFT badge), favicons and `apple-touch-icon.png` (from the round mark), and `social-preview.png` (1200 × 630 link preview; its URL in the page head points at the live domain, so update it if the site launches elsewhere)
- `swift-icon-dark.png` / `swift-icon-white.png`: older single-colour crops, no longer used
- `clinic-reception.jpg`, `clinic-waiting-area.jpg` — real architectural renders of the actual Rouse Hill clinic, sourced from the current live site
- `hero-doctor-patient.jpg` — supplied by the client, used in the hero and the featured services tile
- `clinic-reception-photo.jpg` — real photo of SWIFT's reception (with the SWIFT sign), from the current live site; used in the clinic facilities gallery
- `services/` — one photo per service on the Services page, taken from the current live site's service pages (resized to about 1400px). `pathology.jpg` is a Wix stock photo; orthopaedics reuses `Treatment.jpeg`; dental has no photo yet

## Known placeholders — needs real input before launch

- **Google Analytics**: `G-XXXXXXXXXX` in `index.html` is a placeholder — swap in the real GA4 Measurement ID
- **Nearby ED wait times**: the "Weighing up where to go?" section is hidden (`hidden` attribute in `index.html`) because it only had sample data. No public real-time NSW Health API was identified — needs a data source decision before it goes back on
- **Booking**: "Request appointment" now goes to `request-appointment.html`. The clinic uses Best Practice (Bp Premier), so live online booking should come from Best Health Booking: paste its embed code into `#bookingEmbedMount` and set `BOOKING_EMBED_ENABLED = true`. Until then the page shows a request form, which only shows a confirmation and sends nothing until `APPT_FORM_ENDPOINT` is set (the destination must be suitable for health information)
- **Other old-site links**: "Meet the full team" / "See detailed pricing" and the service tiles still point to the *current* live site (`swiftemergencycare.com.au`) as stand-ins
- **Services list**: reflects the current site's services, with radiology and dental separated out as co-located independent providers per the new brief. Final add/remove list from the client is still pending
- **Gallery**: "From SWIFT" shows the two real clinic photos. The article teaser card was removed until there is a real post to link to

## Design notes

Full brief and design rationale live in `CLAUDE.md` (frontend workflow rules) and the project conversation history — teal-driven custom palette (not Tailwind defaults), Bricolage Grotesque + IBM Plex Sans type pairing, mobile-first, symptom/need-based triage navigation in the hero.
