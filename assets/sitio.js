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
// La regla del borde (como la escala de una placa) marca cuánto se ha leído de la página.
(function () {
  var marca = document.querySelector('.regla i');
  if (!marca) return;
  var pendiente = false;
  function mover() {
    pendiente = false;
    var total = document.documentElement.scrollHeight - innerHeight;
    marca.style.top = (total > 0 ? Math.min(1, scrollY / total) * (innerHeight - 3) : 0) + 'px';
  }
  addEventListener('scroll', function () { if (!pendiente) { pendiente = true; requestAnimationFrame(mover); } }, { passive: true });
  mover();
})();
