// Menú en celular y pequeños comportamientos comunes a todas las páginas.
(function () {
  var boton = document.querySelector('.abrir-menu'), menu = document.getElementById('menu');
  if (boton && menu) {
    boton.addEventListener('click', function () {
      var abierto = menu.classList.toggle('abierto');
      boton.setAttribute('aria-expanded', abierto ? 'true' : 'false');
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && menu.classList.contains('abierto')) { menu.classList.remove('abierto'); boton.setAttribute('aria-expanded', 'false'); boton.focus(); }
    });
  }
})();
