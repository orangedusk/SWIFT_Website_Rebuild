/* Demo tool: sample qualifications and profiles on the Team page (demo branch only, loaded by demo/demo.js).
   These are PLACEHOLDERS to show the client the layout. They are not real credentials and are labelled
   "(sample)" on the page. Real details come from Dr Manivel (item 5.3) and go into tools/build_team.py. */
(function () {
  if (!document.querySelector('.team-card')) return; // Team page only

  var QUALS = {
    'vijay-manivel': 'MBBS, FACEM (sample)',
    'berinder-shahpuri': 'MBBS, FACEM (sample)',
    'gopinath-betarayappa': 'MBBS, FACEM (sample)',
    'pramod-chandru': 'MBBS, FACEM (sample)',
    'nina-dhaliwal': 'MBBS, FACEM (sample)',
    'stephen-madden': 'MBBS, FRACGP (sample)'
  };
  var BIOS = {
    'vijay-manivel': 'Sample profile. A short paragraph about the doctor goes here: their training and experience in emergency medicine, special interests, and what they bring to patient care at SWIFT. Real profiles will be supplied by SWIFT.',
    'berinder-shahpuri': 'Sample profile. A short paragraph about the doctor goes here: their background, areas of clinical interest and their role leading the emergency team at SWIFT. Real profiles will be supplied by SWIFT.'
  };

  document.querySelectorAll('.team-card').forEach(function (card) {
    var slug = card.getAttribute('data-slug');
    if (QUALS[slug] && !card.getAttribute('data-quals')) {
      card.setAttribute('data-quals', QUALS[slug]);
      var name = card.querySelector('.font-display');
      var line = document.createElement('span');
      line.className = 'block text-sm font-medium text-teal700 mt-1';
      line.textContent = QUALS[slug];
      name.parentNode.insertBefore(line, name.nextSibling);
    }
    if (BIOS[slug] && !card.getAttribute('data-bio')) card.setAttribute('data-bio', BIOS[slug]);
  });
})();
