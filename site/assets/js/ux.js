/* Petites interactions communes à toutes les pages :
   en-tête qui passe en verre au défilement, apparitions au scroll,
   et l'accordéon FAQ de la page Prestations. */
(function () {
  var entete = document.querySelector('.site-header');
  if (entete) {
    var bascule = function () { entete.classList.toggle('est-descendu', window.scrollY > 12); };
    window.addEventListener('scroll', bascule, { passive: true });
    bascule();
  }

  var cibles = document.querySelectorAll('.reveal-in');
  if (cibles.length) {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      cibles.forEach(function (el) { el.classList.add('is-visible'); });
    } else {
      var io = new IntersectionObserver(function (entrees) {
        entrees.forEach(function (e) {
          if (e.isIntersecting) { e.target.classList.add('is-visible'); io.unobserve(e.target); }
        });
      }, { threshold: 0, rootMargin: '0px 0px -4% 0px' });
      cibles.forEach(function (el) { io.observe(el); });
    }
  }

  /* Prestations : un seul détail affiché, la sélection du haut fait défiler
     jusqu'à celui choisi et le fait apparaître en fondu. */
  var selecteurs = document.querySelectorAll('.detail-select');
  if (selecteurs.length) {
    selecteurs.forEach(function (lien) {
      lien.addEventListener('click', function (e) {
        e.preventDefault();
        var cible = document.getElementById(lien.getAttribute('href').slice(1));
        if (!cible) return;
        var actif = document.querySelector('.detail-panel.is-active');
        if (actif !== cible) {
          if (actif) actif.classList.remove('is-active');
          cible.classList.add('is-active');
        }
        cible.scrollIntoView({ behavior: 'smooth', block: 'start' });
      });
    });
  }

  /* Cartes "Trois façons de voir votre projet" : la vidéo se lance toute seule
     dès que sa carte entre à l'écran (mobile compris) et reboucle en continu ;
     elle se met en pause hors champ pour ne pas décoder inutilement. */
  var clips = document.querySelectorAll('.service-card__clip');
  if (clips.length && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    var ioClips = new IntersectionObserver(function (entrees) {
      entrees.forEach(function (e) {
        if (e.isIntersecting) { e.target.play().catch(function () {}); }
        else { e.target.pause(); }
      });
    }, { threshold: 0.4 });
    clips.forEach(function (video) { ioClips.observe(video); });
  }

  document.querySelectorAll('.accordion__item').forEach(function (item) {
    var bouton = item.querySelector('.accordion__q');
    if (!bouton) return;
    bouton.addEventListener('click', function () {
      var ouvert = item.classList.contains('is-open');
      item.parentElement.querySelectorAll('.accordion__item').forEach(function (autre) {
        autre.classList.remove('is-open');
      });
      if (!ouvert) item.classList.add('is-open');
    });
  });
})();
