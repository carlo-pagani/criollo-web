# Guía de traspaso

Este documento permite entregar el proyecto completo a otra persona, o al propio doctor, sin depender de quien lo construyó.

## Qué hay y dónde está

| Pieza | Dónde vive | Quién la administra hoy |
|---|---|---|
| Código del sitio y del asistente | Este repositorio (`carlo-pagani/criollo-web`) | Carlo Pagani |
| Vista previa para revisión | GitHub Pages de este repositorio: https://carlo-pagani.github.io/criollo-web/ | Carlo Pagani |
| Sitio publicado | Hosting Bluehost del doctor (ver `publicacion/LEEME.md`) | Pendiente de publicar |
| Asistente con IA y cobros | Worker de Cloudflare (`worker/`) | Pendiente: cuenta por crear |
| Dominios | doctorfelipecriollo.com y traumatologo.com.ec | Ver el inventario de hosting del proyecto |

Ninguna clave se guarda en el repositorio. Las claves viven como «secretos» en GitHub (Settings → Secrets and variables → Actions) y en Cloudflare.

## Cómo traspasar el repositorio

En GitHub: Settings → General → Danger Zone → **Transfer ownership**, y se escribe el usuario que lo recibe. Se traspasa con todo su historial. Después hay que volver a cargar los secretos en la cuenta nueva, porque GitHub no los transfiere.

## Cómo cambiar algo del sitio

1. Datos sueltos (teléfono, precios, horarios, enlaces): `_build/datos.json`.
2. Textos de las páginas: `_build/paginas.py`.
3. Colores: las variables de `:root` en `assets/sitio.css`.
4. Ejecutar `python3 _build/build.py`. El comando regenera las páginas y lista lo que sigue pendiente (todo lo que está entre corchetes).
5. Subir los cambios. La vista previa se actualiza sola; el sitio publicado se actualiza subiendo los archivos a Bluehost.

## Secretos que necesita el asistente

`CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID`, `ANTHROPIC_API_KEY`, y para cobrar: `PAYPHONE_TOKEN`, `PAYPHONE_STORE_ID`, `PAYPAL_SECRET`. Los precios y los topes de gasto están en `worker/wrangler.toml`.

## Antes de publicar

- Textos legales aprobados por el abogado; luego `"borradores_legales": false` en `_build/datos.json` (eso retira los avisos de borrador y permite que Google indexe el sitio).
- Validación clínica de las preguntas y de las señales de alarma con el doctor.
- Datos pendientes completos (los lista `build.py`).
