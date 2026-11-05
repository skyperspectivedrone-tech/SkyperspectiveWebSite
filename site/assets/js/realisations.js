/* Réalisations : la vidéo YouTube ne se charge qu'au clic (aucun appel ni cookie avant). */
(function () {
  document.querySelectorAll('.lecteur[data-youtube]').forEach(function (bouton) {
    bouton.addEventListener('click', function () {
      var iframe = document.createElement('iframe');
      iframe.src = 'https://www.youtube-nocookie.com/embed/' +
        encodeURIComponent(bouton.dataset.youtube) + '?autoplay=1&rel=0&playsinline=1';
      iframe.title = bouton.getAttribute('aria-label');
      iframe.allow = 'autoplay; encrypted-media; picture-in-picture; fullscreen';
      iframe.allowFullscreen = true;
      bouton.parentNode.appendChild(iframe);
      bouton.remove();
      iframe.focus();
    });
  });
})();
