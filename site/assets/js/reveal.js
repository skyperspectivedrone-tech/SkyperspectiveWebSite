/* Reveal 3D piloté au scroll.
   Une séquence d'images est dessinée dans un <canvas> collé à l'écran ;
   la position de défilement détermine l'image affichée.
   Pas de scrub sur <video> : saccadé sur iOS et dépendant des images-clés. */
(function () {
  var sections = document.querySelectorAll("[data-reveal]");
  if (!sections.length) return;

  var reduit = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function sources(section) {
    var json = section.dataset.framesJson;
    if (json) {
      var noeud = document.getElementById(json);
      if (noeud) return JSON.parse(noeud.textContent);
    }
    var base = section.dataset.base;
    var total = parseInt(section.dataset.count, 10);
    var taille = window.innerWidth < 900 ? "900" : "1280";
    var liste = [];
    for (var i = 1; i <= total; i++) {
      liste.push(base + "/" + taille + "/" + String(i).padStart(4, "0") + ".jpg");
    }
    return liste;
  }

  sections.forEach(function (section) {
    var canvas = section.querySelector(".reveal__canvas");
    var legendes = section.querySelectorAll(".reveal__caption");
    var reperes = section.querySelectorAll(".reveal__marker");
    var ctx = canvas.getContext("2d", { alpha: false });
    var urls = sources(section);
    var images = new Array(urls.length);
    var derniere = -1;      // image actuellement dessinée
    var voulue = -1;        // image réclamée par le dernier rendu
    var enAttente = false;

    function charger(index) {
      if (images[index]) return images[index];
      var img = new Image();
      img.decoding = "async";
      // Toute image doit pouvoir relancer le rendu, préchargée ou non : sans cela,
      // une image encore en cours de décodage au moment où on la réclame laisse le
      // canvas noir jusqu'au prochain défilement — et si le visiteur s'est arrêté,
      // il ne voit jamais rien.
      img.onload = function () {
        if (index === voulue) { derniere = -1; rendre(); }
      };
      img.src = urls[index];
      images[index] = img;
      return img;
    }

    function tailleAttendue() {
      var dpr = Math.min(window.devicePixelRatio || 1, 2);
      return [Math.round(canvas.clientWidth * dpr), Math.round(canvas.clientHeight * dpr)];
    }

    function dessiner(img) {
      if (!img.complete || !img.naturalWidth) return false;
      var taille = tailleAttendue();
      var l = taille[0];
      var h = taille[1];
      if (!l || !h) return false;   // conteneur masqué : rien à dessiner
      if (canvas.width !== l || canvas.height !== h) { canvas.width = l; canvas.height = h; }
      // remplissage type "cover" : l'image occupe toute la surface, jamais de bande vide
      var ratio = Math.max(l / img.naturalWidth, h / img.naturalHeight);
      var w = img.naturalWidth * ratio;
      var y = img.naturalHeight * ratio;
      ctx.drawImage(img, (l - w) / 2, (h - y) / 2, w, y);
      return true;
    }

    function progression() {
      var rect = section.getBoundingClientRect();
      var course = section.offsetHeight - window.innerHeight;
      if (course <= 0) return 0;
      return Math.min(1, Math.max(0, -rect.top / course));
    }

    function rendre() {
      enAttente = false;
      var p = reduit ? 1 : progression();
      var index = Math.min(urls.length - 1, Math.round(p * (urls.length - 1)));

      // Le canvas peut avoir été dimensionné à zéro pendant que la page était masquée :
      // dans ce cas il faut redessiner même si l'image n'a pas changé.
      var attendue = tailleAttendue();
      var aRedimensionner = canvas.width !== attendue[0] || canvas.height !== attendue[1];

      voulue = index;
      if (index !== derniere || aRedimensionner) {
        if (dessiner(charger(index))) derniere = index;
        // pré-charge les images voisines pour éviter les trous au défilement
        for (var d = 1; d <= 6; d++) {
          if (index + d < urls.length) charger(index + d);
          if (index - d >= 0) charger(index - d);
        }
      }

      if (legendes.length) {
        var actif = Math.min(legendes.length - 1, Math.floor(p * legendes.length));
        for (var i = 0; i < legendes.length; i++) {
          legendes[i].classList.toggle("is-active", i === actif);
          if (reperes[i]) reperes[i].classList.toggle("is-active", i === actif);
        }
      }
    }

    function planifier() {
      if (enAttente) return;
      // requestAnimationFrame est gelé quand le document est masqué
      // (onglet en arrière-plan, panneau intégré) : on rend alors directement.
      if (document.visibilityState === "hidden") return rendre();
      enAttente = true;
      window.requestAnimationFrame(rendre);
    }

    // première image tout de suite, puis le reste en tâche de fond
    charger(0);
    if (reduit) {
      section.classList.add("reveal--statique");
      charger(urls.length - 1);
      legendes.forEach(function (l) { l.classList.add("is-active"); });
    } else {
      window.addEventListener("scroll", planifier, { passive: true });
      window.addEventListener("resize", function () { derniere = -1; planifier(); });
      document.addEventListener("visibilitychange", function () { derniere = -1; planifier(); });
      planifier();
      // préchargement progressif, sans bloquer le rendu initial.
      // setTimeout plutôt que requestIdleCallback : ce dernier ne se déclenche pas
      // quand le document est masqué, et sa signature diffère (options, pas un délai).
      var suivant = 1;
      (function precharger() {
        if (suivant >= urls.length) return;
        charger(suivant++);
        window.setTimeout(precharger, 16);
      })();
    }
  });
})();
