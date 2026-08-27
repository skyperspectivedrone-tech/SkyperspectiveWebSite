/* Formulaire de contact — envoi direct par Web3Forms, même service que le
   calculateur de devis (voir devis.js). Pas d'étapes ici : un seul écran. */
(function () {
  var form = document.getElementById('contact-form');
  if (!form) return;

  var config = JSON.parse(document.getElementById('contact-config').textContent);
  var champs = {
    nom: form.querySelector('#ct-nom'),
    tel: form.querySelector('#ct-tel'),
    email: form.querySelector('#ct-email'),
    projet: form.querySelector('#ct-projet'),
    botcheck: form.querySelector('#ct-botcheck'),
  };
  var bouton = form.querySelector('#ct-envoyer');
  var etat = form.querySelector('#ct-etat');
  var ecranEnvoi = document.getElementById('ct-envoye');

  function valide() {
    return champs.nom.value.trim() && champs.tel.value.trim()
      && champs.email.checkValidity() && champs.email.value.trim();
  }

  function majBouton() { bouton.disabled = !valide(); }
  ['input', 'change'].forEach(function (evt) {
    form.addEventListener(evt, majBouton);
  });
  majBouton();

  function dire(texte, type) {
    etat.textContent = texte;
    etat.className = 'formulaire__etat' + (type ? ' is-' + type : '');
  }

  function lienSecours() {
    var sujet = 'Message depuis le site — ' + champs.nom.value;
    var corps = champs.nom.value + '\nTéléphone : ' + champs.tel.value
      + '\nE-mail : ' + champs.email.value + '\n\n' + (champs.projet.value || '(non renseigné)');
    return 'mailto:' + config.email + '?subject=' + encodeURIComponent(sujet)
      + '&body=' + encodeURIComponent(corps);
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (!valide() || champs.botcheck.checked) return;

    if (!config.cle) {
      dire("L’envoi automatique n’est pas encore configuré : votre messagerie va s’ouvrir avec le message déjà rédigé.", 'info');
      window.location.href = lienSecours();
      return;
    }

    bouton.disabled = true;
    dire('Envoi en cours…', 'info');

    fetch(config.endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify({
        access_key: config.cle,
        subject: 'Message depuis le site — ' + champs.nom.value,
        from_name: 'Site Sky Perspective',
        name: champs.nom.value,
        email: champs.email.value,
        message: 'Téléphone : ' + champs.tel.value + '\n\n' + (champs.projet.value || '(non renseigné)'),
      }),
    })
      .then(function (r) { return r.json(); })
      .then(function (j) {
        if (!j.success) throw new Error(j.message || 'envoi refusé');
        form.hidden = true;
        if (ecranEnvoi) ecranEnvoi.hidden = false;
      })
      .catch(function (e) {
        bouton.disabled = false;
        dire('L’envoi a échoué (' + e.message + '). Votre messagerie va s’ouvrir avec le message déjà rédigé.', 'erreur');
        window.setTimeout(function () { window.location.href = lienSecours(); }, 1200);
      });
  });
})();
