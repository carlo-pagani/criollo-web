#!/usr/bin/env python3
"""Genera las tres propuestas gráficas (propuestas/1, 2 y 3). Son solo portadas de muestra."""
import os, html
R = os.path.join(os.path.dirname(__file__), "..", "propuestas")
WA = "https://wa.me/593991827823"; TEL = "tel:+593991827823"; TELV = "099 182 7823"
DIR = "Edificio Citimed, 6.º piso, consultorio 628"; CALLE = "Av. Mariana de Jesús y Nuño de Valderrama, Quito"
SERV = [
 ("Diagnóstico de lesiones musculoesqueléticas", "Evaluación clínica apoyada en radiografía, resonancia magnética o ecografía, para definir el tratamiento que corresponde a cada caso."),
 ("Cirugía ortopédica", "Reparación de fracturas, corrección de deformidades y reemplazo de articulaciones dañadas."),
 ("Fracturas y luxaciones", "Inmovilización, reducción y, cuando el caso lo requiere, cirugía. Con rehabilitación posterior."),
 ("Lesiones deportivas", "Evaluación, fisioterapia y rehabilitación. Cirugía en los casos que la necesitan."),
 ("Infecciones óseas y articulares", "Diagnóstico temprano, antibióticos específicos y cirugía cuando hace falta retirar tejido infectado."),
 ("Prótesis y ortopedia", "Indicación y ajuste de prótesis y aparatos ortopédicos, adaptados a cada paciente."),
 ("Consultas preventivas", "Examen físico y valoración de riesgos para detectar problemas a tiempo."),
 ("Enfermedades congénitas y deformidades", "Manejo con cirugía, terapia física y seguimiento a largo plazo."),
 ("Emergencias traumatológicas", "Valoración de la lesión, inmovilización adecuada e intervención quirúrgica si es necesaria."),
]
CRED = [
 ("Formación", "Oncólogo ortopedista formado en la Universidad Militar Nueva Granada, Bogotá."),
 ("Trayectoria", "Ex coordinador de la Clínica de Ortopedia de SOLCA, núcleo de Quito."),
 ("Docencia", "Docente del posgrado de Ortopedia Oncológica de la Universidad Central del Ecuador. Docente invitado de la Universidad San Francisco de Quito."),
 ("Sociedades", "Miembro de ISOLS, de SLATME y de la Sociedad Ecuatoriana de Oncología."),
]
VAL = [
 ("Humanidad", "Comprender lo que necesita cada paciente: escuchar con atención y ponerse en su lugar."),
 ("Aprendizaje", "Seguir estudiando y adoptar lo que la especialidad va demostrando que funciona."),
 ("Respeto", "Tratar a cada persona, paciente o colega, como quisiéramos ser tratados."),
 ("Determinación", "Hacer lo correcto por el bien de la persona que tenemos delante."),
]
NOMBRES = {1: "Luz", 2: "Revista", 3: "Quirófano"}

def barra(n):
    o = "".join(f'<a href="../{i}/"{" aria-current=page" if i==n else ""}>{i} · {NOMBRES[i]}</a>' for i in (1,2,3))
    return f'<div class="pp"><span>Propuesta gráfica {n} de 3</span><nav>{o}</nav></div>'
PP = """.pp{position:sticky;top:0;z-index:99;display:flex;gap:16px;justify-content:space-between;align-items:center;flex-wrap:wrap;background:#111;color:#fff;font:500 12.5px/1 system-ui,sans-serif;padding:9px 16px;letter-spacing:.02em}
.pp nav{display:flex;gap:6px}.pp a{color:#fff;text-decoration:none;padding:6px 10px;border-radius:99px;border:1px solid #ffffff40}.pp a[aria-current]{background:#fff;color:#111}"""

def doc(n, css, body):
    return f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex"><title>Propuesta {n} · {NOMBRES[n]} · Dr. Felipe Criollo Palacios</title>
<link rel="stylesheet" href="../fuentes.css"><link rel="stylesheet" href="../../assets/fuentes.css">
<style>*,*:before,*:after{{box-sizing:border-box}}html{{scroll-behavior:smooth;-webkit-text-size-adjust:100%}}body{{margin:0}}img{{max-width:100%;display:block}}a{{color:inherit}}h1,h2,h3,p,ul,ol,dl,dd,figure{{margin:0;padding:0}}ul,ol{{list-style:none}}
{PP}
{css}</style></head><body>{barra(n)}{body}</body></html>"""

IMG = "../../assets/img/"

# ───────────────────────── 1 · LUZ ─────────────────────────
css1 = """
:root{--t:#0D1B2A;--s:#55627A;--a:#2747E8;--a2:#E9EDFE;--c:#FF6B4A;--l:#E4E8F0;--f:#fff;--g:#F5F7FB}
body{font:400 17px/1.6 'Hanken Grotesk',system-ui,sans-serif;color:var(--t);background:var(--f)}
.w{max-width:1180px;margin:0 auto;padding:0 24px}
h1,h2,h3,.d{font-family:'Bricolage Grotesque',sans-serif;font-weight:700;letter-spacing:-.02em;line-height:1.02}
header.c{display:flex;align-items:center;justify-content:space-between;padding:18px 0}
.logo{font:700 19px/1 'Bricolage Grotesque';letter-spacing:-.02em;text-decoration:none}.logo i{font-style:normal;color:var(--a)}
header.c nav{display:flex;gap:4px;background:var(--g);padding:5px;border-radius:99px}
header.c nav a{text-decoration:none;font-weight:500;font-size:15px;padding:9px 16px;border-radius:99px}header.c nav a:hover{background:#fff}
.b{display:inline-flex;align-items:center;gap:10px;background:var(--a);color:#fff;text-decoration:none;font-weight:600;padding:15px 24px;border-radius:99px;font-size:16px}
.b.o{background:#fff;color:var(--t);box-shadow:inset 0 0 0 1.5px var(--l)}.b.n{background:var(--t)}
.h{display:grid;grid-template-columns:1.15fr .85fr;gap:40px;align-items:end;padding:36px 0 0}
.et{display:inline-flex;gap:8px;align-items:center;font-size:14px;font-weight:600;color:var(--a);background:var(--a2);padding:8px 14px;border-radius:99px}
.et:before{content:"";width:8px;height:8px;border-radius:50%;background:var(--c)}
.h h1{font-size:clamp(44px,7.4vw,96px);margin:22px 0 24px}.h h1 em{font-style:normal;color:var(--a)}
.h p.l{font-size:20px;color:var(--s);max-width:520px}
.h .ac{display:flex;gap:12px;flex-wrap:wrap;margin:30px 0 56px}
.ret{position:relative;background:var(--a2);border-radius:220px 220px 32px 32px;overflow:hidden;aspect-ratio:.86}
.ret img{width:100%;height:100%;object-fit:cover;object-position:top;mix-blend-mode:multiply}
.chip{position:absolute;background:#fff;border-radius:18px;padding:12px 16px;font-size:13.5px;line-height:1.35;box-shadow:0 12px 32px #0d1b2a1f}
.chip b{display:block;font-size:15px}.chip.x{left:-18px;bottom:26%}.chip.y{right:-10px;bottom:7%}
.fr{position:relative}
.cr{display:grid;grid-template-columns:repeat(4,1fr);gap:0;border-top:1.5px solid var(--l);border-bottom:1.5px solid var(--l);margin-top:0}
.cr div{padding:26px 22px 28px;border-left:1.5px solid var(--l);font-size:15px;color:var(--s)}.cr div:first-child{border-left:0;padding-left:0}
.cr b{display:block;font:700 13px/1 'Hanken Grotesk';letter-spacing:.08em;text-transform:uppercase;color:var(--a);margin-bottom:10px}
section{padding:96px 0}.k{font-weight:600;color:var(--a);font-size:15px;margin-bottom:14px}
h2{font-size:clamp(34px,4.6vw,60px);max-width:760px}
.bento{display:grid;grid-template-columns:repeat(6,1fr);gap:14px;margin-top:48px}
.bento article{grid-column:span 2;background:var(--g);border-radius:28px;padding:28px;min-height:210px;display:flex;flex-direction:column;justify-content:space-between;transition:transform .2s}
.bento article:hover{transform:translateY(-4px)}
.bento article i{font:600 13px/1 'IBM Plex Mono';font-style:normal;color:var(--a)}
.bento h3{font-size:25px;letter-spacing:-.025em;line-height:1.08;margin:28px 0 10px}.bento p{font-size:15px;color:var(--s);line-height:1.5}
.bento .g{grid-column:span 3;background:var(--a);color:#fff}.bento .g p,.bento .g i{color:#ffffffc9}.bento .g h3{font-size:34px}
.bento article:last-child{grid-column:1/-1;min-height:0}
.bento .d2{grid-column:span 3;background:var(--t);color:#fff}.bento .d2 p,.bento .d2 i{color:#ffffffb0}.bento .d2 h3{font-size:34px}
.per{background:var(--g);border-radius:40px;padding:56px;display:grid;grid-template-columns:.9fr 1.1fr;gap:56px;align-items:center}
.per img{border-radius:28px;aspect-ratio:1.05;object-fit:cover;width:100%}
.per p{color:var(--s);margin-top:18px}
.vals{display:grid;grid-template-columns:1fr 1fr;gap:22px 28px;margin-top:34px}.vals b{display:block;font:700 19px/1.1 'Bricolage Grotesque';margin-bottom:6px}.vals span{font-size:15px;color:var(--s);line-height:1.5;display:block}
.ex{background:var(--t);color:#fff;border-radius:40px;padding:64px 56px;display:grid;grid-template-columns:1.2fr .8fr;gap:48px;align-items:center}
.ex h2{color:#fff}.ex p{color:#ffffffb5;margin-top:18px;max-width:520px}
.pas{display:grid;gap:10px}.pas li{background:#ffffff12;border-radius:18px;padding:16px 18px;display:flex;gap:14px;align-items:center;font-size:15.5px}
.pas li b{flex:none;width:32px;height:32px;border-radius:50%;background:var(--c);display:grid;place-items:center;font-size:14px}
.tag{display:inline-block;background:var(--c);color:#fff;font-size:13px;font-weight:700;padding:6px 12px;border-radius:99px;margin-bottom:18px}
.ct{display:grid;grid-template-columns:1fr 1fr;gap:14px}.ct>div{border-radius:32px;padding:44px;background:var(--a2)}
.ct .tel{font:700 clamp(38px,5vw,64px)/1 'Bricolage Grotesque';letter-spacing:-.04em;text-decoration:none;display:block;margin:14px 0 26px}
.ct h3{font-size:30px;margin:14px 0 12px}.ct p{color:var(--s)}
footer{padding:36px 0 110px;color:var(--s);font-size:14px;display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap}
.mov{display:none}
@media(max-width:860px){header.c nav{display:none}.h{grid-template-columns:1fr;gap:8px}.h .ac{margin-bottom:32px}.fr{max-width:380px;margin:0 auto;width:100%}.chip.x{left:-6px}.chip.y{right:-6px}
.cr{grid-template-columns:1fr 1fr}.cr div{padding:20px 14px;border-left:0;border-top:1.5px solid var(--l)}.cr div:nth-child(-n+2){border-top:0}.cr div:first-child{padding-left:14px}
section{padding:64px 0}.bento{grid-template-columns:1fr}.bento article,.bento .g,.bento .d2{grid-column:auto;min-height:0}.per,.ex{grid-template-columns:1fr;padding:28px;border-radius:28px;gap:28px}.vals{grid-template-columns:1fr}.ct{grid-template-columns:1fr}.ct>div{padding:28px}
.mov{display:flex;position:fixed;left:12px;right:12px;bottom:12px;gap:8px;background:#fff;padding:8px;border-radius:99px;box-shadow:0 10px 40px #0d1b2a40;z-index:50}.mov a{flex:1;justify-content:center;padding:13px 10px;font-size:15px}}
"""
def p1():
    s = SERV
    def card(i, cls=""):
        return f'<article class="{cls}"><i>{i+1:02d}</i><div><h3>{s[i][0]}</h3><p>{s[i][1]}</p></div></article>'
    bento = card(0,"g")+card(1,"d2")+"".join(card(i) for i in range(2,8))+card(8,"g")
    bento = bento.replace('</article><article class="g"><i>09','</article><article class="g" style="grid-column:span 2"><i>09')
    cr = "".join(f"<div><b>{a}</b>{b}</div>" for a,b in CRED)
    vals = "".join(f"<div><b>{a}</b><span>{b}</span></div>" for a,b in VAL)
    return f"""<div class="w"><header class="c"><a class="logo" href="#">Dr. Felipe Criollo<i>.</i></a>
<nav><a href="#servicios">Servicios</a><a href="#perfil">El doctor</a><a href="#express">Consulta en línea</a><a href="#contacto">Contacto</a></nav>
<a class="b n" href="{WA}">Agendar cita</a></header>
<div class="h"><div><span class="et">Quito · Edificio Citimed</span>
<h1>Traumatología y ortopedia <em>oncológica.</em></h1>
<p class="l">Dr. Felipe Criollo Palacios. Diagnóstico y tratamiento de lesiones de huesos, articulaciones y músculos, y de tumores del sistema musculoesquelético.</p>
<div class="ac"><a class="b" href="{WA}">Escribir por WhatsApp</a><a class="b o" href="{TEL}">Llamar al {TELV}</a></div></div>
<div class="fr"><div class="ret"><img src="{IMG}felipe-retrato-900.webp" alt="Dr. Felipe Criollo Palacios"></div>
<div class="chip x"><b>Ortopedia oncológica</b>Universidad Militar Nueva Granada</div><div class="chip y"><b>ISOLS · SLATME</b>Sociedades científicas</div></div></div>
<div class="cr">{cr}</div>
<section id="servicios"><p class="k">Servicios</p><h2>Todo lo que necesita de traumatología, en un solo lugar.</h2><div class="bento">{bento}</div></section>
<section id="perfil" style="padding-top:0"><div class="per"><img src="{IMG}felipe-consultorio-900.webp" alt="El doctor Criollo en su consultorio de Citimed"><div><p class="k">El doctor</p><h2>Cómo trabajamos.</h2><p>Atención en consultorio y en quirófano, con el mismo criterio: explicar con claridad qué tiene el paciente y qué opciones existen.</p><div class="vals">{vals}</div></div></div></section>
<section id="express" style="padding-top:0"><div class="ex"><div><span class="tag">Muy pronto</span><h2>Consulta en línea, desde cualquier ciudad.</h2><p>Cuente su caso, adjunte sus radiografías o resonancias y reciba la respuesta del doctor por escrito. Para quienes viven fuera de Quito o quieren una segunda opinión.</p></div>
<ol class="pas"><li><b>1</b>Cuenta qué le ocurre</li><li><b>2</b>Sube sus estudios</li><li><b>3</b>El doctor revisa su caso</li><li><b>4</b>Recibe su respuesta</li></ol></div></section>
<section id="contacto" style="padding-top:0"><div class="ct"><div><p class="k">Citas</p><a class="tel" href="{TEL}">{TELV}</a><a class="b" href="{WA}">Escribir por WhatsApp</a></div>
<div><p class="k">Consultorio</p><h3>{DIR}</h3><p>{CALLE}</p></div></div></section>
<footer><span>© 2026 Dr. Felipe Criollo Palacios · Traumatología y ortopedia oncológica</span><span>Privacidad · Accesibilidad</span></footer></div>
<div class="mov"><a class="b" href="{WA}">WhatsApp</a><a class="b o" href="{TEL}">Llamar</a></div>"""

# ───────────────────────── 2 · REVISTA ─────────────────────────
css2 = """
:root{--p:#F3EEE4;--t:#191510;--s:#5E564B;--r:#C4361A;--l:#19151026}
body{font:400 19px/1.55 'Newsreader',Georgia,serif;color:var(--t);background:var(--p)}
.w{max-width:1240px;margin:0 auto;padding:0 28px}
.m{font:500 11.5px/1.3 'IBM Plex Mono',monospace;letter-spacing:.12em;text-transform:uppercase}
h1,h2,h3{font-family:'Fraunces',serif;font-weight:400;letter-spacing:-.025em;line-height:.98;font-variation-settings:'opsz' 144}
em{font-style:italic}
.top{display:flex;justify-content:space-between;gap:16px;padding:14px 0;border-bottom:1px solid var(--t)}
.top nav{display:flex;gap:26px}.top a{text-decoration:none}.top a:hover{color:var(--r)}
.mast{padding:34px 0 26px;border-bottom:4px double var(--t);display:grid;grid-template-columns:1fr auto;align-items:end;gap:24px}
.mast h1{font-size:clamp(50px,10.6vw,168px);letter-spacing:-.045em;line-height:.86}.mast h1 em{color:var(--r);font-weight:300}
.mast p{text-align:right;max-width:190px;padding-bottom:10px}
.cov{display:grid;grid-template-columns:5fr 4fr 3fr;gap:36px;padding:36px 0 56px;border-bottom:1px solid var(--t)}
.cov h2{font-size:clamp(34px,4.3vw,62px);font-weight:300}.cov h2 em{color:var(--r)}
.cov .lead{margin-top:24px;font-size:21px;color:var(--s)}.cov .lead:first-letter{font:400 4.1em/.8 'Fraunces';float:left;padding:6px 10px 0 0;color:var(--t)}
.cta{display:flex;gap:22px;flex-wrap:wrap;margin-top:32px;align-items:center}
.bt{font:500 12.5px/1 'IBM Plex Mono';letter-spacing:.1em;text-transform:uppercase;text-decoration:none;background:var(--t);color:var(--p);padding:17px 22px}
.bt:hover{background:var(--r)}.ln{font-style:italic;text-underline-offset:5px;text-decoration-thickness:1px}
figure img{width:100%;filter:grayscale(1) contrast(1.08);mix-blend-mode:multiply}
figure.ph{background:#E6DFD1}figure.ph img{aspect-ratio:.82;object-fit:cover;object-position:top}
figcaption{margin-top:10px;color:var(--s)}
.col3 dl{border-top:1px solid var(--t)}.col3 dt{padding-top:14px;color:var(--r)}.col3 dd{font-size:16.5px;line-height:1.42;padding:6px 0 16px;border-bottom:1px solid var(--l)}
section{padding:72px 0;border-bottom:1px solid var(--t)}
.sh{display:grid;grid-template-columns:3fr 9fr;gap:36px;margin-bottom:44px;align-items:start}.sh .m{padding-top:12px;color:var(--r)}
.sh h2{font-size:clamp(38px,5.6vw,84px);font-weight:300}
.idx{columns:2;column-gap:56px}.idx li{break-inside:avoid;display:grid;grid-template-columns:54px 1fr;gap:6px;padding:20px 0;border-top:1px solid var(--l)}
.idx li>span{font:300 34px/1 'Fraunces';font-style:italic;color:var(--r)}.idx h3{font-size:27px;letter-spacing:-.02em;line-height:1.06;margin-bottom:8px;font-variation-settings:'opsz' 40}
.idx p{font-size:17px;color:var(--s);line-height:1.45}
.rep{display:grid;grid-template-columns:7fr 5fr;gap:48px;align-items:start}
.rep figure img{aspect-ratio:1.25;object-fit:cover}
.q{font:300 clamp(28px,3.2vw,44px)/1.12 'Fraunces';font-style:italic;letter-spacing:-.02em}.q:before{content:"“";color:var(--r)}.q:after{content:"”";color:var(--r)}
.vl{margin-top:30px}.vl li{padding:14px 0;border-top:1px solid var(--l);font-size:17.5px;line-height:1.45}.vl b{font:500 12px/1 'IBM Plex Mono';letter-spacing:.1em;text-transform:uppercase;display:block;margin-bottom:6px}
.exp{background:var(--t);color:var(--p);padding:64px 56px;display:grid;grid-template-columns:7fr 5fr;gap:48px}
.exp h2{font-size:clamp(36px,4.8vw,70px);font-weight:300}.exp h2 em{color:#F08A6E}.exp p{margin-top:20px;color:#F3EEE4B8;max-width:540px}
.exp ol li{display:flex;gap:16px;padding:15px 0;border-top:1px solid #F3EEE433;font-size:18px}.exp ol span{font:500 12px/1.9 'IBM Plex Mono';color:#F08A6E}
.col{display:grid;grid-template-columns:repeat(3,1fr);gap:36px}.col .tel{font:300 clamp(40px,4.6vw,64px)/1 'Fraunces';letter-spacing:-.03em;text-decoration:none;display:block;margin:12px 0}
.col p{font-size:18px}.col .m{color:var(--r);margin-bottom:10px}
footer{padding:22px 0 40px;display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;color:var(--s)}
@media(max-width:900px){.top nav{display:none}.mast{grid-template-columns:1fr}.mast p{text-align:left;max-width:none;padding:0}.cov{grid-template-columns:1fr;gap:28px}.cov figure{max-width:420px}
.sh,.rep,.exp,.col{grid-template-columns:1fr;gap:20px}.idx{columns:1}.exp{padding:36px 24px}section{padding:52px 0}body{font-size:18px}}
"""
def p2():
    idx = "".join(f"<li><span>{i+1}</span><div><h3>{a}</h3><p>{b}</p></div></li>" for i,(a,b) in enumerate(SERV))
    dl = "".join(f'<dt class="m">{a}</dt><dd>{b}</dd>' for a,b in CRED)
    vl = "".join(f"<li><b>{a}</b>{b}</li>" for a,b in VAL)
    return f"""<div class="w"><div class="top m"><span>Traumatología y ortopedia oncológica</span><nav><a href="#servicios">Servicios</a><a href="#perfil">Perfil</a><a href="#express">Consulta en línea</a><a href="#contacto">Contacto</a></nav><span>Quito, Ecuador</span></div>
<div class="mast"><h1>Felipe <em>Criollo</em><br>Palacios</h1><p class="m">Médico traumatólogo<br>y ortopedista oncólogo<br>Edificio Citimed</p></div>
<div class="cov"><div><h2>Huesos, articulaciones y músculos, <em>y los tumores que los afectan.</em></h2>
<p class="lead">El doctor Criollo atiende en Quito lesiones y enfermedades del sistema musculoesquelético: del diagnóstico a la cirugía, y de la fractura al tumor óseo.</p>
<div class="cta"><a class="bt" href="{WA}">Agendar por WhatsApp</a><a class="ln" href="{TEL}">o llame al {TELV}</a></div></div>
<figure class="ph"><img src="{IMG}felipe-retrato-900.webp" alt="Dr. Felipe Criollo Palacios"></figure>
<div class="col3"><dl>{dl}</dl></div></div>
<section id="servicios"><div class="sh"><p class="m">N.º 01 — Servicios</p><h2>Todas sus necesidades de traumatología, <em>en un solo lugar.</em></h2></div><ol class="idx">{idx}</ol></section>
<section id="perfil"><div class="sh"><p class="m">N.º 02 — Perfil</p><h2>Del consultorio <em>al quirófano.</em></h2></div>
<div class="rep"><figure><img src="{IMG}felipe-quirofano-900.webp" alt="El doctor Criollo durante una cirugía"><figcaption class="m">El doctor Criollo (izq.) durante una cirugía.</figcaption></figure>
<div><p class="q">Hacer lo correcto por el bien de la persona que tenemos delante.</p><ul class="vl">{vl}</ul></div></div></section>
<section id="express" style="border:0;padding-bottom:0"><div class="exp"><div><p class="m" style="color:#F08A6E;margin-bottom:18px">N.º 03 — Muy pronto</p><h2>Consulta en línea, <em>desde cualquier ciudad.</em></h2><p>Cuente su caso, adjunte sus radiografías o resonancias y reciba la respuesta del doctor por escrito. Para quienes viven fuera de Quito o buscan una segunda opinión.</p></div>
<ol><li><span>01</span>Cuenta qué le ocurre</li><li><span>02</span>Sube sus estudios</li><li><span>03</span>El doctor revisa su caso</li><li><span>04</span>Recibe su respuesta por escrito</li></ol></div></section>
<section id="contacto"><div class="col"><div><p class="m">Citas</p><a class="tel" href="{TEL}">{TELV}</a><a class="ln" href="{WA}">Escribir por WhatsApp</a></div>
<div><p class="m">Consultorio</p><p>{DIR}<br>{CALLE}</p></div><div><p class="m">También atiende en</p><p>Hospital Metropolitano, Quito</p></div></div></section>
<footer class="m"><span>© 2026 Dr. Felipe Criollo Palacios</span><span>Privacidad · Accesibilidad</span></footer></div>"""

# ───────────────────────── 3 · QUIRÓFANO ─────────────────────────
css3 = """
:root{--az:#0F4FA8;--ma:#0A2D5E;--ci:#8FE3F2;--am:#FFD43B;--t:#0B1F3A;--s:#4A5D78;--f:#F2F6FA}
body{font:400 17px/1.6 'Archivo',system-ui,sans-serif;color:var(--t);background:#fff}
.w{max-width:1260px;margin:0 auto;padding:0 28px}
h1,h2,h3,.u{font-family:'Barlow Condensed',sans-serif;font-weight:700;text-transform:uppercase;line-height:.9;letter-spacing:-.005em}
.hero{position:relative;color:#fff;background:var(--ma);overflow:hidden;min-height:min(880px,calc(100vh - 34px));display:flex;flex-direction:column}
.hero>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:0% 20%}
.hero:before{content:"";position:absolute;inset:0;z-index:1;background:linear-gradient(90deg,#0A2D5EE6 0%,#0F4FA8B8 45%,#0F4FA833 100%),linear-gradient(0deg,#0A2D5E 0%,#0A2D5E00 40%)}
.hero>*:not(img){position:relative;z-index:2;width:100%}
header.c{display:flex;align-items:center;justify-content:space-between;padding:22px 0}
.logo{font:700 24px/1 'Barlow Condensed';text-transform:uppercase;letter-spacing:.02em;text-decoration:none}.logo span{color:var(--ci)}
header.c nav{display:flex;gap:30px}header.c nav a{text-decoration:none;font:600 16px/1 'Barlow Condensed';letter-spacing:.09em;text-transform:uppercase}header.c nav a:hover{color:var(--am)}
.b{display:inline-flex;gap:10px;align-items:center;background:var(--am);color:var(--t);text-decoration:none;font:700 18px/1 'Barlow Condensed';letter-spacing:.07em;text-transform:uppercase;padding:17px 26px}
.b.o{background:transparent;color:#fff;box-shadow:inset 0 0 0 2px #fff}.b.z{background:var(--az);color:#fff}
.hc{flex:1;display:flex;flex-direction:column;justify-content:flex-end;padding:40px 0 0}
.hc .u.s{font-size:20px;letter-spacing:.14em;color:var(--ci);font-weight:600}
.hc h1{font-size:clamp(58px,11.5vw,184px);margin:14px 0 26px;letter-spacing:-.015em}.hc h1 span{color:var(--ci)}
.hc p{font-size:20px;max-width:560px;color:#ffffffd9}
.ac{display:flex;gap:12px;flex-wrap:wrap;margin:30px 0 44px}
.band{display:grid;grid-template-columns:repeat(4,1fr);border-top:1px solid #ffffff40}
.band div{padding:22px 22px 26px 0;font-size:14.5px;line-height:1.45;color:#ffffffc9}.band div+div{padding-left:22px;border-left:1px solid #ffffff40}
.band b{display:block;font:700 15px/1 'Barlow Condensed';letter-spacing:.14em;text-transform:uppercase;color:var(--am);margin-bottom:8px}
section{padding:100px 0}
.st{display:flex;justify-content:space-between;align-items:end;gap:24px;flex-wrap:wrap;margin-bottom:40px}
h2{font-size:clamp(46px,7vw,104px);color:var(--ma)}h2 span{color:var(--az)}
.st p{max-width:330px;color:var(--s)}
.rows li{display:grid;grid-template-columns:90px 1fr 1.1fr 40px;gap:24px;align-items:center;padding:22px 0;border-top:2px solid var(--t);transition:background .15s,padding .15s}
.rows li:last-child{border-bottom:2px solid var(--t)}.rows li:hover{background:var(--am);padding-left:18px;padding-right:18px}
.rows i{font:700 44px/1 'Barlow Condensed';font-style:normal;color:var(--az)}.rows h3{font-size:34px;line-height:.95}
.rows p{color:var(--s);font-size:16px;line-height:1.45}.rows li:hover p{color:var(--t)}.rows u{text-decoration:none;font-size:26px}
.azul{background:var(--az);color:#fff}.azul h2{color:#fff}.azul h2 span{color:var(--ci)}
.per{display:grid;grid-template-columns:1fr 1fr;gap:56px;align-items:center}
.per img{width:100%;aspect-ratio:1.1;object-fit:cover}
.vals{display:grid;grid-template-columns:1fr 1fr;gap:0;margin-top:36px;border-top:1px solid #ffffff59}
.vals div{padding:20px 20px 22px 0;border-bottom:1px solid #ffffff59;font-size:15px;line-height:1.45;color:#ffffffd4}.vals div:nth-child(even){padding-left:20px;border-left:1px solid #ffffff59}
.vals b{display:block;font:700 24px/1 'Barlow Condensed';text-transform:uppercase;letter-spacing:.03em;color:var(--am);margin-bottom:8px}
.ex{background:var(--f)}.exg{display:grid;grid-template-columns:1.1fr .9fr;gap:56px;align-items:end}
.tag{display:inline-block;background:var(--t);color:var(--am);font:700 15px/1 'Barlow Condensed';letter-spacing:.14em;text-transform:uppercase;padding:8px 12px;margin-bottom:20px}
.exg p{color:var(--s);margin-top:22px;max-width:520px;font-size:18px}
.pas{display:grid;grid-template-columns:1fr 1fr;gap:10px}.pas li{background:#fff;padding:22px;font-weight:500;line-height:1.3;border-bottom:4px solid var(--az)}.pas b{display:block;font:700 46px/1 'Barlow Condensed';color:var(--az);margin-bottom:10px}
.ct{background:var(--ma);color:#fff;padding:90px 0 40px}.ct h2{color:#fff}
.tel{font:700 clamp(70px,13vw,210px)/.85 'Barlow Condensed';color:var(--am);text-decoration:none;display:block;letter-spacing:-.01em;margin:10px 0 34px}
.cg{display:grid;grid-template-columns:auto 1fr 1fr;gap:48px;align-items:start;border-top:1px solid #ffffff40;padding-top:30px}.cg b{display:block;font:700 15px/1 'Barlow Condensed';letter-spacing:.14em;text-transform:uppercase;color:var(--ci);margin-bottom:8px}
.fo{margin-top:60px;font-size:13.5px;color:#ffffff99;display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap}
@media(max-width:900px){header.c nav,header.c .b{display:none}.hero:before{background:linear-gradient(0deg,#0A2D5E 30%,#0F4FA8B3 100%)}.band{grid-template-columns:1fr 1fr}.band div{padding:16px 12px 16px 0!important;border-left:0!important;border-bottom:1px solid #ffffff40}
section{padding:64px 0}.rows li{grid-template-columns:48px 1fr;gap:8px 12px}.rows i{font-size:30px}.rows p{grid-column:2}.rows u{display:none}.rows h3{font-size:28px}
.per,.exg{grid-template-columns:1fr;gap:28px}.vals{grid-template-columns:1fr}.vals div:nth-child(even){padding-left:0;border-left:0}.cg{grid-template-columns:1fr;gap:24px}.hc .u.s{font-size:16px}}
"""
def p3():
    rows = "".join(f"<li><i>{i+1:02d}</i><h3>{a}</h3><p>{b}</p><u>→</u></li>" for i,(a,b) in enumerate(SERV))
    band = "".join(f"<div><b>{a}</b>{b}</div>" for a,b in CRED)
    vals = "".join(f"<div><b>{a}</b>{b}</div>" for a,b in VAL)
    return f"""<div class="hero"><img src="{IMG}felipe-quirofano-900.webp" alt="El doctor Criollo durante una cirugía">
<div class="w"><header class="c"><a class="logo" href="#">Dr. Felipe <span>Criollo</span></a><nav><a href="#servicios">Servicios</a><a href="#perfil">El doctor</a><a href="#express">Consulta en línea</a><a href="#contacto">Contacto</a></nav><a class="b" href="{WA}">Agendar cita</a></header></div>
<div class="w hc"><p class="u s">Dr. Felipe Criollo Palacios · Quito</p><h1>Traumatología<br>y ortopedia <span>oncológica</span></h1>
<p>Diagnóstico y tratamiento de lesiones de huesos, articulaciones y músculos, y de tumores del sistema musculoesquelético.</p>
<div class="ac"><a class="b" href="{WA}">Escribir por WhatsApp</a><a class="b o" href="{TEL}">Llamar · {TELV}</a></div>
<div class="band">{band}</div></div></div>
<section id="servicios"><div class="w"><div class="st"><h2>Nueve <span>servicios.</span><br>Un solo lugar.</h2><p>Todas sus necesidades de traumatología, atendidas por el mismo especialista.</p></div><ol class="rows">{rows}</ol></div></section>
<section id="perfil" class="azul"><div class="w per"><img src="{IMG}felipe-consultorio-900.webp" alt="El doctor Criollo en su consultorio de Citimed"><div><h2>Cómo <span>trabajamos</span></h2><div class="vals">{vals}</div></div></div></section>
<section id="express" class="ex"><div class="w exg"><div><span class="tag">Muy pronto</span><h2>Consulta <span>en línea</span></h2><p>Cuente su caso, adjunte sus radiografías o resonancias y reciba la respuesta del doctor por escrito. Para quienes viven fuera de Quito o buscan una segunda opinión.</p></div>
<ol class="pas"><li><b>1</b>Cuenta qué le ocurre</li><li><b>2</b>Sube sus estudios</li><li><b>3</b>El doctor revisa su caso</li><li><b>4</b>Recibe su respuesta</li></ol></div></section>
<div class="ct" id="contacto"><div class="w"><h2>Agende su cita</h2><a class="tel" href="{TEL}">{TELV}</a>
<div class="cg"><a class="b" href="{WA}">Escribir por WhatsApp</a><div><b>Consultorio</b>{DIR}<br>{CALLE}</div><div><b>También atiende en</b>Hospital Metropolitano, Quito</div></div>
<div class="fo"><span>© 2026 Dr. Felipe Criollo Palacios · Traumatología y ortopedia oncológica</span><span>Privacidad · Accesibilidad</span></div></div></div>"""

for n, css, f in ((1,css1,p1),(2,css2,p2),(3,css3,p3)):
    os.makedirs(os.path.join(R,str(n)), exist_ok=True)
    open(os.path.join(R,str(n),"index.html"),"w").write(doc(n,css,f()))
open(os.path.join(R,"index.html"),"w").write('<!doctype html><meta charset="utf-8"><meta name="robots" content="noindex"><meta http-equiv="refresh" content="0;url=1/"><a href="1/">Ver propuestas</a>')
print("ok")
