#!/usr/bin/env python3
"""Genera el sitio estático del Dr. Felipe Criollo Palacios.

Uso:  python3 _build/build.py
Lee _build/datos.json (teléfono, precios, horarios…) y _build/paginas.py (el contenido) y escribe cada página
como carpeta/index.html en la raíz del repositorio, además de sitemap.xml.
Los enlaces son relativos, así el sitio funciona igual en la vista previa de GitHub Pages y en el dominio propio.
"""
import json, os, re, html, datetime, importlib.util

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(RAIZ, "_build", "datos.json"), encoding="utf-8"))
HOY = datetime.date.today().isoformat()


def pend(texto):
    """Resalta lo que falta completar (todo lo que va entre corchetes)."""
    return re.sub(r"\[([A-ZÁÉÍÓÚÑ0-9][^\]]*)\]", r'<span class="pendiente">[\1]</span>', texto)


PEND = r"\[[A-ZÁÉÍÓÚÑ0-9][^\]]*\]"


def limpiar(cuerpo):
    """Sitio publicado: quita con cuidado todo lo que sigue pendiente, para que nada se vea a medio hacer.
    Elimina el elemento más pequeño (frase suelta, viñeta, fila, tarjeta, pregunta) que contiene un dato pendiente,
    y después los títulos y listas que hayan quedado vacíos."""
    cuerpo = re.sub(r'\s*<span class="pendiente">[^<]*</span>', "", cuerpo)
    for etiqueta in ("li", "tr", "p", "details", "article"):
        patron = re.compile(rf"<{etiqueta}\b[^>]*>(?:(?!<{etiqueta}\b|</{etiqueta}>).)*?{PEND}(?:(?!<{etiqueta}\b).)*?</{etiqueta}>", re.S)
        cuerpo = patron.sub("", cuerpo)
    # lo que quedó como etiqueta sin dato («Horario:», una fila de tabla sin contenido)
    cuerpo = re.sub(r"<tr>\s*<th>[^<]*</th>\s*<td>\s*</td>\s*</tr>", "", cuerpo)
    cuerpo = re.sub(r"<(p|li)\b[^>]*>[^<]*:\s*</\1>", "", cuerpo)
    for _ in range(3):
        cuerpo = re.sub(r"<(ul|ol|tbody|table|p|li)\b[^>]*>\s*</\1>", "", cuerpo)
        cuerpo = re.sub(r"<table>\s*<tbody>\s*</tbody>\s*</table>", "", cuerpo)
        cuerpo = re.sub(r"<h2\b[^>]*>[^<]*</h2>\s*(?=<h2\b|</div>|<div class=\"botones\")", "", cuerpo)
    return cuerpo


def rel(ruta_pagina, destino):
    """Enlace relativo desde una página (p. ej. 'segunda-opinion/') hacia otra ('' es el inicio)."""
    nivel = ruta_pagina.count("/")
    pre = "../" * nivel
    if destino.startswith(("http", "mailto:", "tel:", "#")):
        return destino
    return (pre + destino) or "./"


# Páginas con contenido clínico redactado para el sitio nuevo. Se publican cuando el doctor las haya leído:
# basta poner "contenido_clinico": true en datos.json.
CLINICAS = ("especialidades/", "biopsia/", "cuando-consultar/", "casos-y-publicaciones/", "para-colegas/", "preguntas-frecuentes/")
def retenida(ruta):
    return not D.get("contenido_clinico") and ruta.startswith(CLINICAS)

MENU = [(r, t) for r, t in [
    ("especialidades/", "Especialidades"),
    ("segunda-opinion/", "Segunda opinión"),
    ("perfil/", "El doctor"),
    ("para-colegas/", "Para colegas"),
    ("fuera-de-quito/", "Fuera de Quito"),
    ("donde-atiendo/", "Consultorio"),
] if not retenida(r)]


def sin_enlaces_retenidos(doc):
    """Quita los enlaces a páginas que todavía no se publican: los botones y viñetas desaparecen, el resto queda como texto."""
    if D.get("contenido_clinico"):
        return doc
    pat = "(?:" + "|".join(re.escape(c) for c in CLINICAS) + ")"
    href = rf'href="(?:\.\./)*{pat}[^"]*"'
    doc = re.sub(rf'<li>\s*<a\b[^>]*{href}[^>]*>.*?</a>\s*</li>', "", doc, flags=re.S)
    doc = re.sub(rf'<a\b[^>]*class="[^"]*btn[^"]*"[^>]*{href}[^>]*>.*?</a>', "", doc, flags=re.S)
    doc = re.sub(rf'<a\b[^>]*{href}[^>]*class="[^"]*btn[^"]*"[^>]*>.*?</a>', "", doc, flags=re.S)
    doc = re.sub(rf'<a\b[^>]*{href}[^>]*>(.*?)</a>', r"\1", doc, flags=re.S)
    return doc


def cabecera(ruta):
    items = "".join(
        f'<a href="{rel(ruta, r)}"{" aria-current=page" if ruta.startswith(r) else ""}>{t}</a>' for r, t in MENU
    )
    return f"""<a class="saltar" href="#contenido">Saltar al contenido</a>
<header class="cabecera">
<div class="contenedor">
<a class="marca" href="{rel(ruta, '')}"><strong>Dr. Felipe Criollo</strong><span>Traumatología y ortopedia oncológica</span></a>
<button class="abrir-menu" type="button" aria-expanded="false" aria-controls="menu">Menú</button>
<nav class="menu" id="menu" aria-label="Principal"><a href="{rel(ruta, '')}#asistente">Guía inteligente</a>{items}<a class="btn" href="{rel(ruta, 'consulta-express/')}">Consulta en línea →</a></nav>
</div>
</header>"""


def pie(ruta):
    r = lambda d: rel(ruta, d)
    tel = D["telefono"]
    tel_html = f'<a href="tel:{D["telefono_enlace"]}">{tel}</a>' if D["telefono_enlace"] else pend(tel)
    ESPECIALIDAD = f"""<div><h2>Especialidad</h2><ul><li><a href="{r('especialidades/tumores-oseos/')}">Tumores óseos</a></li><li><a href="{r('especialidades/sarcoma-de-partes-blandas/')}">Sarcoma de partes blandas</a></li><li><a href="{r('especialidades/metastasis-oseas/')}">Metástasis óseas</a></li><li><a href="{r('biopsia/')}">La biopsia en un tumor óseo</a></li><li><a href="{r('casos-y-publicaciones/')}">Casos y publicaciones</a></li></ul></div>""" if D.get("contenido_clinico") else f"""<div><h2>En línea</h2><ul><li><a href="{r('')}#asistente">Guía inteligente</a></li><li><a href="{r('')}#oncologia">Especialidades</a></li></ul></div>"""
    return f"""<footer class="pie">
<div class="contenedor">
<div class="columnas">
<div><h2>Consulta privada</h2><p>{D['direccion_citimed']}</p><p style="margin-top:8px">También atiende en el Hospital Metropolitano y en el Hospital Vozandes, Quito.</p>{f'<p style="margin-top:8px">Teléfono: {tel_html}</p>' if tel else ''}{f'<p style="margin-top:8px"><a href="{D["whatsapp_enlace"]}" rel="noopener">Escribir por WhatsApp</a></p>' if D["whatsapp_enlace"] else ""}</div>
<div><h2>Pacientes</h2><ul><li><a href="{r('consulta-express/')}">Consulta express</a></li><li><a href="{r('segunda-opinion/')}">Segunda opinión</a></li><li><a href="{r('fuera-de-quito/')}">Si vive fuera de Quito</a></li><li><a href="{r('cuando-consultar/')}">Cuándo consultar sin esperar</a></li><li><a href="{r('preguntas-frecuentes/')}">Preguntas frecuentes</a></li></ul></div>
{ESPECIALIDAD}
<div><h2>El doctor</h2><ul><li><a href="{r('perfil/')}">Perfil y formación</a></li><li><a href="{r('para-colegas/')}">Para colegas que refieren</a></li><li><a href="{D['instagram']}" rel="noopener">Instagram</a></li></ul></div>
</div>
<p class="aviso-medico">La información de este sitio es educativa y no reemplaza una consulta médica. Ante una urgencia, acuda a emergencias o llame al 911.</p>
<div class="legal"><span>© {datetime.date.today().year} {D['nombre']} · {D['especialidad']}</span><span><a href="{r('privacidad/')}">Privacidad</a>{"" if D.get("borradores_legales") else f' · <a href="{r("condiciones/")}">Condiciones del servicio</a>'} · <a href="{r('accesibilidad/')}">Accesibilidad</a></span></div>
</div>
</footer>"""


def documento(ruta, titulo, descripcion, cuerpo, jsonld=None, scripts=(), sin_indice=False):
    r = lambda d: rel(ruta, d)
    canonica = D["dominio"] + "/" + ruta
    ld = ""
    for bloque in jsonld or []:
        ld += '<script type="application/ld+json">' + json.dumps(bloque, ensure_ascii=False) + "</script>\n"
    js = "".join(f'<script src="{r(s)}" defer></script>' for s in ("assets/sitio.js",) + tuple(scripts))
    titulo_completo = titulo if titulo.startswith(D["nombre"]) else f"{titulo} · {D['nombre']}"
    # Mientras el sitio esté en revisión (borradores legales sin aprobar), ninguna página se ofrece a los buscadores
    robots = '<meta name="robots" content="noindex, nofollow">' if sin_indice or not D.get("publicado") else ""
    if ruta == "" and not sin_indice:
        portada = open(os.path.join(RAIZ, "_build", "portada.html"), encoding="utf-8").read()
        cab = f"""<title>{html.escape(titulo_completo)}</title>
<meta name="description" content="{html.escape(descripcion)}">
{robots}<link rel="canonical" href="{canonica}">
<meta property="og:type" content="website"><meta property="og:locale" content="es_EC">
<meta property="og:title" content="{html.escape(titulo_completo)}"><meta property="og:description" content="{html.escape(descripcion)}">
<meta property="og:url" content="{canonica}"><meta property="og:image" content="{D['dominio']}/assets/img/og.jpg">
<meta name="theme-color" content="#12284C"><link rel="icon" href="assets/img/icono.svg" type="image/svg+xml">
{ld}"""
        return portada.replace("{{CABEZA}}", cab)
    return f"""<!doctype html>
<html lang="es-EC">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(titulo_completo)}</title>
<meta name="description" content="{html.escape(descripcion)}">
{robots}<link rel="canonical" href="{canonica}">
<meta property="og:type" content="website"><meta property="og:locale" content="es_EC">
<meta property="og:title" content="{html.escape(titulo_completo)}"><meta property="og:description" content="{html.escape(descripcion)}">
<meta property="og:url" content="{canonica}"><meta property="og:image" content="{D['dominio']}/assets/img/og.jpg">
<meta name="theme-color" content="#12284C">
<link rel="icon" href="{r('assets/img/icono.svg')}" type="image/svg+xml">
<link rel="preload" href="{r('assets/fuentes/plusjakartasans-latin.woff2')}" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{r('assets/jakarta.css')}">
<link rel="stylesheet" href="{r('assets/sitio.css')}">
{ld}{js}
</head>
<body>
{cabecera(ruta)}
<main id="contenido">
{cuerpo}
</main>
{pie(ruta)}
</body>
</html>
"""


def cabeza(ruta, migas, antetitulo, titulo, entrada=""):
    m = " / ".join(f'<a href="{rel(ruta, d)}">{t}</a>' for d, t in migas)
    return f"""<section class="cabeza-pagina"><div class="contenedor">
<nav class="migas" aria-label="Ruta">{m}</nav>
{f'<p class="antetitulo">{antetitulo}</p>' if antetitulo else ''}<h1>{titulo}</h1>
{f'<p class="entrada">{entrada}</p>' if entrada else ''}
</div></section>"""


def migas_ld(ruta, migas, titulo):
    items = [{"@type": "ListItem", "position": i + 1, "name": t, "item": D["dominio"] + "/" + d} for i, (d, t) in enumerate(migas)]
    items.append({"@type": "ListItem", "position": len(items) + 1, "name": titulo, "item": D["dominio"] + "/" + ruta})
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}


MEDICO_LD = {
    "@context": "https://schema.org",
    "@type": ["Physician", "MedicalBusiness"],
    "@id": D["dominio"] + "/#medico",
    "name": D["nombre"],
    "url": D["dominio"] + "/",
    "image": D["dominio"] + "/assets/img/felipe-retrato-900.webp",
    "description": "Cirujano ortopedista oncólogo en Quito: tumores óseos y de partes blandas, metástasis en extremidades, salvamento de extremidad y traumatología.",
    "medicalSpecialty": ["Oncologic", "Musculoskeletal"],
    "knowsAbout": ["Ortopedia oncológica", "Tumores óseos", "Sarcoma de partes blandas", "Metástasis óseas", "Fractura patológica", "Cirugía de salvamento de extremidad", "Traumatología"],
    "address": {"@type": "PostalAddress", "streetAddress": "Av. Mariana de Jesús y Nuño de Valderrama, Centro Médico Citimed, piso 6, consultorio 628", "addressLocality": "Quito", "addressRegion": "Pichincha", "addressCountry": "EC"},
    "hospitalAffiliation": {"@type": "Hospital", "name": "Hospital Metropolitano", "address": {"@type": "PostalAddress", "addressLocality": "Quito", "addressCountry": "EC"}},
    "areaServed": "Ecuador",
    "sameAs": [D["instagram"]],
}


def cargar_paginas():
    spec = importlib.util.spec_from_file_location("paginas", os.path.join(RAIZ, "_build", "paginas.py"))
    mod = importlib.util.module_from_spec(spec)
    mod.D, mod.rel, mod.pend, mod.cabeza, mod.migas_ld, mod.MEDICO_LD = D, rel, pend, cabeza, migas_ld, MEDICO_LD
    spec.loader.exec_module(mod)
    return mod.PAGINAS


def main():
    paginas = cargar_paginas()
    urls = []
    for p in paginas:
        ruta = p["ruta"]
        if retenida(ruta):
            continue
        cuerpo = limpiar(p["cuerpo"]) if D.get("publicado") else pend(p["cuerpo"])
        if D.get("publicado") and re.search(PEND, cuerpo):
            raise SystemExit(f"Quedó un dato pendiente visible en /{ruta}: {re.search(PEND, cuerpo).group(0)}")
        if not D.get("borradores_legales") and p.get("legal"):
            cuerpo = re.sub(r'<div class="caja borrador">.*?</div>', "", cuerpo, flags=re.S)
        oculta = p.get("sin_indice", False) or bool(p.get("servicio") and D.get("borradores_legales"))
        doc = sin_enlaces_retenidos(documento(ruta, p["titulo"], p["descripcion"], cuerpo, p.get("jsonld"), p.get("scripts", ()), oculta))
        destino = os.path.join(RAIZ, ruta, "index.html") if ruta else os.path.join(RAIZ, "index.html")
        if p.get("archivo"):
            destino = os.path.join(RAIZ, p["archivo"])
        os.makedirs(os.path.dirname(destino), exist_ok=True)
        open(destino, "w", encoding="utf-8").write(doc)
        if not p.get("sin_indice") and not (p.get("servicio") and D.get("borradores_legales")):
            urls.append((ruta, p.get("prioridad", "0.6")))
    # Direcciones del WordPress anterior. GitHub Pages no admite redirecciones 301: cada una es una página mínima
    # con enlace canónico y salto inmediato a la página nueva.
    for vieja, nueva in [("about", "perfil/"), ("services", ""), ("contact", "donde-atiendo/"), ("hello-world", "")]:
        destino_url = D["dominio"] + "/" + nueva
        os.makedirs(os.path.join(RAIZ, vieja), exist_ok=True)
        open(os.path.join(RAIZ, vieja, "index.html"), "w", encoding="utf-8").write(
            f'<!doctype html>\n<html lang="es-EC"><head><meta charset="utf-8"><title>{D["nombre"]}</title>'
            f'<link rel="canonical" href="{destino_url}"><meta name="robots" content="noindex, follow">'
            f'<meta http-equiv="refresh" content="0; url=../{nueva}"></head>'
            f'<body><p>Esta página cambió de dirección: <a href="../{nueva}">continuar</a>.</p></body></html>\n')
    mapa = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for ruta, pr in urls:
        mapa.append(f"<url><loc>{D['dominio']}/{ruta}</loc><lastmod>{HOY}</lastmod><priority>{pr}</priority></url>")
    mapa.append("</urlset>")
    open(os.path.join(RAIZ, "sitemap.xml"), "w").write("\n".join(mapa) + "\n")
    pendientes = sorted(set(re.findall(r"\[[A-ZÁÉÍÓÚÑ0-9][^\]]*\]", " ".join(p["cuerpo"] for p in paginas) + json.dumps(D, ensure_ascii=False))))
    print(f"{len(paginas)} páginas generadas. Datos pendientes del doctor: {len(pendientes)}")
    for x in pendientes:
        print("  ", x)


if __name__ == "__main__":
    main()
