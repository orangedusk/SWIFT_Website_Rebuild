# Page build scripts

`fees.html`, `team.html` and `services.html` are generated. Edit the content in these scripts, not in the HTML, then rebuild:

```
python3 tools/build_fees.py
python3 tools/build_team.py
python3 tools/build_services.py
```

- `build_page.py` wraps each page in the shared site chrome (emergency banner, header, mobile menu and bottom bar, footer) taken from `request-appointment.html`. Change the chrome there and rebuild to update all three pages.
- `build_services.py` reuses the service icons from the homepage tiles in `index.html`.
- `build_team.py` holds the staff list. Bios are empty until SWIFT supplies them; fill in the last field of each entry. Photos live in `brand_assets/team/`.

## Copy deck (client copy review)

```
python3 tools/copy_deck.py                                  # export: writes SWIFT_copy_deck.xlsx
python3 tools/apply_copy.py SWIFT_copy_deck.xlsx            # preview the client's edits
python3 tools/apply_copy.py SWIFT_copy_deck.xlsx --apply    # apply them and rebuild the pages
```

- `copy_deck.py` reads every page (plus the visit steps, search results and form messages in the page scripts, and the search terms in `symptoms.js`) into a spreadsheet: *Read me*, *Website copy* (ID, Page, Section, Element, Current copy, New copy, Notes) and *Symptom search*. Shared parts (banner, menus, footer) are listed once. Demo-only content is left out.
- `apply_copy.py` replaces each row's *Current copy* with its *New copy* wherever that exact piece of text appears in the sources, and changes search outcomes in `symptoms.js`. Text that wraps a link, or that doesn't appear as one whole piece, is listed as "Needs a manual edit". Always preview first.
- Export again after any change to the site, so the client reviews the current copy.
