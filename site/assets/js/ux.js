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

    /* Arrivée depuis une autre page sur prestations.html#p-xxx : ouvrir ce détail. */
    var demande = location.hash && document.getElementById(location.hash.slice(1));
    if (demande && demande.classList.contains('detail-panel')) {
      var ouvert = document.querySelector('.detail-panel.is-active');
      if (ouvert) ouvert.classList.remove('is-active');
      demande.classList.add('is-active');
      demande.scrollIntoView({ block: 'start' });
    }
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

  /* Prestations : la vidéo de chaque carte de la grille démarre au survol (ou au focus
     clavier) et revient à sa première image — identique au poster — quand le curseur s'en va
     (décision validée : pas de lecture automatique sur ordinateur).
     Sans survol (tactile) : elle tourne dès qu'elle est à l'écran, en pause hors champ.
     Rien n'est téléchargé avant (preload="none"). Mouvement réduit : le poster reste affiché. */
  var boucles = document.querySelectorAll('[data-boucle]');
  if (boucles.length && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    var lire = function (zone) {
      zone.classList.add('est-en-lecture');
      zone.querySelector('video').play().catch(function () { zone.classList.remove('est-en-lecture'); });
    };
    var arreter = function (zone, rembobiner) {
      var v = zone.querySelector('video');
      zone.classList.remove('est-en-lecture');
      v.pause();
      if (rembobiner && v.readyState) v.currentTime = 0;
    };
    if (window.matchMedia('(hover: hover) and (pointer: fine)').matches) {
      boucles.forEach(function (zone) {
        zone.addEventListener('mouseenter', function () { lire(zone); });
        zone.addEventListener('mouseleave', function () { arreter(zone, true); });
        zone.addEventListener('focusin', function () { lire(zone); });
        zone.addEventListener('focusout', function () { arreter(zone, true); });
      });
    } else {
      var ioBoucles = new IntersectionObserver(function (entrees) {
        entrees.forEach(function (e) {
          if (e.isIntersecting) lire(e.target); else arreter(e.target, false);
        });
      }, { threshold: 0.25 });
      boucles.forEach(function (zone) { ioBoucles.observe(zone); });
    }
  }

  /* Prestations : au survol d'une vignette de film, un aperçu muet du film démarre dans la
     vignette, à l'instant de son image d'attente (data-debut) pour que l'image ne saute pas.
     La vidéo n'est créée et chargée qu'au premier survol ; elle se met en pause quand le
     curseur s'en va. Souris uniquement, et jamais en mouvement réduit. */
  if (window.matchMedia('(hover: hover) and (pointer: fine)').matches &&
      !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    document.querySelectorAll('.film[data-film]').forEach(function (vignette) {
      var apercu = null;
      vignette.addEventListener('mouseenter', function () {
        if (!apercu) {
          apercu = document.createElement('video');
          apercu.className = 'film__apercu';
          apercu.muted = true; apercu.loop = true; apercu.playsInline = true;
          apercu.setAttribute('aria-hidden', 'true');
          apercu.preload = 'auto';
          apercu.addEventListener('loadedmetadata', function () {
            apercu.currentTime = parseFloat(vignette.dataset.debut) || 0;
          }, { once: true });
          apercu.addEventListener('playing', function () {
            if (vignette.matches(':hover')) vignette.classList.add('est-en-lecture');
          });
          apercu.src = vignette.dataset.film;
          vignette.querySelector('.film__media').appendChild(apercu);
        }
        apercu.play().catch(function () {});
      });
      vignette.addEventListener('mouseleave', function () {
        vignette.classList.remove('est-en-lecture');
        if (apercu) apercu.pause();
      });
    });
  }

  /* Prestations : une vignette de film ouvre le film complet, avec le son, dans la
     visionneuse (<dialog> modale : Échap ferme, le focus revient sur la vignette).
     La source n'est posée qu'à l'ouverture et retirée à la fermeture, pour couper le
     téléchargement en cours. Un clic hors de la vidéo ferme aussi. */
  var visionneuse = document.querySelector('.visionneuse');
  if (visionneuse && visionneuse.showModal) {
    var film = visionneuse.querySelector('video');
    document.querySelectorAll('.film[data-film]').forEach(function (vignette) {
      vignette.addEventListener('click', function () {
        visionneuse.querySelector('.visionneuse__titre').textContent = vignette.dataset.titre;
        film.poster = vignette.dataset.poster;
        film.src = vignette.dataset.film;
        visionneuse.showModal();
        film.play().catch(function () {});
      });
    });
    visionneuse.querySelector('.visionneuse__fermer').addEventListener('click', function () {
      visionneuse.close();
    });
    visionneuse.addEventListener('click', function (e) {
      if (e.target === visionneuse) visionneuse.close();
    });
    visionneuse.addEventListener('close', function () {
      film.pause();
      film.removeAttribute('src');
      film.load();
    });
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
