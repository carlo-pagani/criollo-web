# Publicación en Bluehost

Producción: el Bluehost del doctor. GitHub es solo código fuente y vista previa.

1. Subir a la carpeta de doctorfelipecriollo.com todo el repositorio **menos** `worker/`, `_build/`, `publicacion/`, `.github/`, `README.md` y `_config.yml`.
2. Copiar `doctorfelipecriollo.com.htaccess` a esa carpeta con el nombre `.htaccess` (antes, respaldar el WordPress y su `.htaccess`).
3. Cuando el sitio nuevo esté verificado, copiar `traumatologo.com.ec.htaccess` como `.htaccess` en la carpeta de traumatologo.com.ec (respaldando antes sus archivos). Ojo: si esa carpeta es `public_html` y la del .com es una subcarpeta suya, las reglas del .ec deben limitarse a ese dominio con `RewriteCond %{HTTP_HOST} traumatologo\.com\.ec$ [NC]` delante de cada regla.
4. No tocar correo ni DNS.

Requisitos previos: textos legales aprobados, datos del doctor completos y validación clínica de la consulta express.

## Alternativa: publicar con GitHub Pages (vía elegida el 2026-11-23)

1. Añadir en la raíz un archivo `CNAME` con `doctorfelipecriollo.com` **solo el día del lanzamiento** (si se añade antes, la vista previa deja de funcionar).
2. En el DNS: registros A del dominio raíz a 185.199.108.153, 185.199.109.153, 185.199.110.153 y 185.199.111.153; `www` como CNAME a `carlo-pagani.github.io`. No tocar MX, SPF ni DKIM.
3. En GitHub: Settings → Pages → Custom domain y activar «Enforce HTTPS».
4. `_config.yml` ya excluye `worker/`, `_build/`, `publicacion/` y los documentos internos. Las direcciones del WordPress anterior (`/about/`, `/services/`, `/contact/`, `/hello-world/`) ya tienen su página de salto.
5. traumatologo.com.ec sigue en Bluehost solo con su `.htaccess` de redirecciones.
