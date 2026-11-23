# Sitio del Dr. Felipe Criollo Palacios

Sitio estático (GitHub Pages) más un Worker de Cloudflare para la consulta express con IA y el cobro.

- `_build/paginas.py`: el contenido de todas las páginas. `_build/datos.json`: teléfono, precios, horarios y enlaces.
- `python3 _build/build.py` regenera los HTML y `sitemap.xml`, y lista los datos pendientes del doctor (lo que va entre corchetes).
- `assets/sitio.css`: toda la paleta está en las variables de `:root`.
- `assets/consulta.js`: la consulta express. Lee `data/servicios.json` (dirección del asistente y formulario de envío). Sin esa configuración funciona en modo de prueba: no envía ni cobra.
- `worker/`: asistente con IA (`/guia`), precios y pagos verificados. Se despliega con `.github/workflows/asistente.yml` cuando existen los secretos `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID` y `ANTHROPIC_API_KEY` (y los de Payphone y PayPal para cobrar).

Antes de publicar en el dominio: aprobación legal de `privacidad/`, `condiciones/` y `consentimiento/` (luego poner `borradores_legales` en `false`), validación clínica de las preguntas y señales de alarma, y archivo `CNAME`.
