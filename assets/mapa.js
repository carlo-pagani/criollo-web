// Los mapas de Google solo se cargan si el visitante lo pide: así Google no recibe datos de quien solo lee la página.
(function () {
  document.querySelectorAll('[data-mapa]').forEach(function (caja) {
    var boton = caja.querySelector('button');
    if (!boton) return;
    boton.addEventListener('click', function () {
      var marco = document.createElement('iframe');
      marco.className = 'mapa';
      marco.title = caja.getAttribute('data-titulo') || 'Mapa';
      marco.loading = 'lazy';
      marco.referrerPolicy = 'no-referrer';
      marco.src = 'https://www.google.com/maps?q=' + caja.getAttribute('data-mapa') + '&output=embed';
      caja.replaceWith(marco);
    });
  });
})();
