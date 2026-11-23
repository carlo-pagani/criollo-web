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


def rel(ruta_pagina, destino):
    """Enlace relativo desde una página (p. ej. 'segunda-opinion/') hacia otra ('' es el inicio)."""
    nivel = ruta_pagina.count("/")
    pre = "../" * nivel
    if destino.startswith(("http", "mailto:", "tel:", "#")):
        return destino
    return (pre + destino) or "./"


MENU = [
    ("especialidades/", "Especialidades"),
    ("segunda-opinion/", "Segunda opinión"),
    ("perfil/", "Sobre el doctor"),
    ("para-colegas/", "Para colegas"),
    ("donde-atiendo/", "Dónde atiendo"),
]


def cabecera(ruta):
    items = "".join(
        f'<a href="{rel(ruta, r)}"{" aria-current=page" if ruta.startswith(r) else ""}>{t}</a>' for r, t in MENU
    )
    return f"""<a class="saltar" href="#contenido">Saltar al contenido</a>
<header class="cabecera">
<div class="contenedor">
<a class="marca" href="{rel(ruta, '')}"><strong>{D['nombre']}</strong><span>{D['especialidad']} · Quito</span></a>
<button class="abrir-menu" type="button" aria-expanded="false" aria-controls="menu">Menú</button>
<nav class="menu" id="menu" aria-label="Principal">{items}<a class="btn" href="{rel(ruta, 'consulta-express/')}">Consulta express</a></nav>
</div>
</header>"""


def pie(ruta):
    r = lambda d: rel(ruta, d)
    tel = D["telefono"]
    tel_html = f'<a href="tel:{D["telefono_enlace"]}">{tel}</a>' if D["telefono_enlace"] else pend(tel)
    return f"""<footer class="pie">
<div class="contenedor">
<div class="columnas">
<div><h2>Consulta privada</h2><p>{D['direccion_citimed']}</p><p style="margin-top:8px">También atiende en el Hospital Metropolitano, Quito.</p><p style="margin-top:8px">Teléfono: {tel_html}</p></div>
<div><h2>Pacientes</h2><ul><li><a href="{r('consulta-express/')}">Consulta express</a></li><li><a href="{r('segunda-opinion/')}">Segunda opinión</a></li><li><a href="{r('fuera-de-quito/')}">Si vive fuera de Quito</a></li><li><a href="{r('cuando-consultar/')}">Cuándo consultar sin esperar</a></li><li><a href="{r('preguntas-frecuentes/')}">Preguntas frecuentes</a></li></ul></div>
<div><h2>Especialidad</h2><ul><li><a href="{r('especialidades/tumores-oseos/')}">Tumores óseos</a></li><li><a href="{r('especialidades/sarcoma-de-partes-blandas/')}">Sarcoma de partes blandas</a></li><li><a href="{r('especialidades/metastasis-oseas/')}">Metástasis óseas</a></li><li><a href="{r('biopsia/')}">La biopsia en un tumor óseo</a></li><li><a href="{r('casos-y-publicaciones/')}">Casos y publicaciones</a></li></ul></div>
<div><h2>El doctor</h2><ul><li><a href="{r('perfil/')}">Perfil y formación</a></li><li><a href="{r('para-colegas/')}">Para colegas que refieren</a></li><li><a href="{D['instagram']}" rel="noopener">Instagram</a></li></ul></div>
</div>
<p class="aviso-medico">La información de este sitio es educativa y no reemplaza una consulta médica. Ante una urgencia, acuda a emergencias o llame al 911.</p>
<div class="legal"><span>© {datetime.date.today().year} {D['nombre']} · {D['especialidad']}</span><span><a href="{r('privacidad/')}">Privacidad</a> · <a href="{r('condiciones/')}">Condiciones del servicio</a> · <a href="{r('accesibilidad/')}">Accesibilidad</a></span></div>
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
    robots = '<meta name="robots" content="noindex">' if sin_indice else ""
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
<meta name="theme-color" content="#7A1F2B">
<link rel="icon" href="{r('assets/img/icono.svg')}" type="image/svg+xml">
<link rel="preload" href="{r('assets/fuentes/literata-latin.woff2')}" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{r('assets/fuentes.css')}">
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
    "address": {"@type": "PostalAddress", "streetAddress": "Av. Mariana de Jesús y Nuño de Valderrama, Centro Médico CITIMED, piso 6, consultorio 628", "addressLocality": "Quito", "addressRegion": "Pichincha", "addressCountry": "EC"},
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
        cuerpo = pend(p["cuerpo"])
        if not D.get("borradores_legales") and p.get("legal"):
            cuerpo = re.sub(r'<div class="caja borrador">.*?</div>', "", cuerpo, flags=re.S)
        doc = documento(ruta, p["titulo"], p["descripcion"], cuerpo, p.get("jsonld"), p.get("scripts", ()), p.get("sin_indice", False))
        destino = os.path.join(RAIZ, ruta, "index.html") if ruta else os.path.join(RAIZ, "index.html")
        if p.get("archivo"):
            destino = os.path.join(RAIZ, p["archivo"])
        os.makedirs(os.path.dirname(destino), exist_ok=True)
        open(destino, "w", encoding="utf-8").write(doc)
        if not p.get("sin_indice"):
            urls.append((ruta, p.get("prioridad", "0.6")))
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
