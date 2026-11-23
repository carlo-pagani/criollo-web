# Publicación en Bluehost

Producción: el Bluehost del doctor. GitHub es solo código fuente y vista previa.

1. Subir a la carpeta de doctorfelipecriollo.com todo el repositorio **menos** `worker/`, `_build/`, `publicacion/`, `.github/`, `README.md` y `_config.yml`.
2. Copiar `doctorfelipecriollo.com.htaccess` a esa carpeta con el nombre `.htaccess` (antes, respaldar el WordPress y su `.htaccess`).
3. Cuando el sitio nuevo esté verificado, copiar `traumatologo.com.ec.htaccess` como `.htaccess` en la carpeta de traumatologo.com.ec (respaldando antes sus archivos). Ojo: si esa carpeta es `public_html` y la del .com es una subcarpeta suya, las reglas del .ec deben limitarse a ese dominio con `RewriteCond %{HTTP_HOST} traumatologo\.com\.ec$ [NC]` delante de cada regla.
4. No tocar correo ni DNS.

Requisitos previos: textos legales aprobados, datos del doctor completos y validación clínica de la consulta express.
