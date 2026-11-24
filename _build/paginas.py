# Contenido del sitio. Cada página es un diccionario con ruta, título, descripción y cuerpo (HTML).
# build.py inyecta aquí: D (datos.json), rel, pend, cabeza, migas_ld y MEDICO_LD.
# Regla editorial: datos verificables en lugar de adjetivos; sin promesas de plazos ni de resultados.
PAGINAS = []


def pagina(**k):
    PAGINAS.append(k)


def img(ruta, nombre, alt, proporcion="4/5", clase="", eager=False):
    a = rel(ruta, f"assets/img/{nombre}")
    ancho, alto = (int(x) for x in proporcion.split("/"))
    carga = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return (f'<img src="{a}-900.webp" srcset="{a}-480.webp 480w, {a}-900.webp 900w" sizes="(max-width: 700px) 100vw, 480px" '
            f'alt="{alt}" style="aspect-ratio:{proporcion};object-fit:cover;object-position:center top" width="900" height="{round(900 * alto / ancho)}" {carga} class="{clase}">')


def cta(ruta, motivo=None, texto="Llena tu ficha médica", clase="btn"):
    q = f"?motivo={motivo}" if motivo else ""
    return f'<a class="{clase}" href="{rel(ruta, "consulta-express/")}{q}">{texto}</a>'


def revisado(extra=""):
    if D["revision_medica"].startswith("["):
        return f'<p class="revision">{extra}Esta página es informativa y no reemplaza una consulta: cada caso necesita una valoración personal.</p>'
    return (f'<p class="revision">Revisado por el {D["nombre"]}, {D["especialidad"].lower()}. Última revisión: {D["revision_medica"]}. '
            f'{extra}Esta página es informativa y no reemplaza una consulta: cada caso necesita una valoración personal.</p>')


# Frases que dependen de un dato que puede faltar
def precio(clave, con, sin):
    return con.format(D[clave]) if not D[clave].startswith("[") else sin


CORREO_O_SITIO = D["correo"] if not D["correo"].startswith("[") else "una solicitud escrita entregada en el consultorio del doctor"


def ld_pagina_medica(ruta, titulo, descripcion, tema):
    return {"@context": "https://schema.org", "@type": "MedicalWebPage", "name": titulo, "description": descripcion,
            "url": D["dominio"] + "/" + ruta, "inLanguage": "es-EC", "about": {"@type": "MedicalCondition", "name": tema},
            "author": {"@id": D["dominio"] + "/#medico"}, "audience": "https://schema.org/Patient"}


# ---------------------------------------------------------------- Inicio
r = ""
pagina(ruta=r, prioridad="1.0",
       titulo=f"{D['nombre']} · Ortopedista oncólogo en Quito",
       descripcion="Cirujano ortopedista oncólogo en Quito. Tumores óseos y de partes blandas, metástasis en extremidades, segunda opinión y traumatología. Ficha médica inteligente previa a la cita, con subida de estudios.",
       jsonld=[MEDICO_LD, {"@context": "https://schema.org", "@type": "WebSite", "name": D["nombre"], "url": D["dominio"] + "/", "inLanguage": "es-EC"}],
       cuerpo=f"""
<section class="negatoscopio"><div class="contenedor">
<div>
<p class="antetitulo">{D['especialidad']} · Quito</p>
<h1>Tumores óseos y sarcomas, tratados por <span class="marcador">quien los opera</span>.</h1>
<p class="lema">Soy el {D['nombre']}. Cuénteme su caso y suba sus estudios: los reviso personalmente antes de la cita.</p>
</div>
<figure class="placa">{img(r, 'felipe-retrato', 'Retrato del Dr. Felipe Criollo Palacios con bata blanca', eager=True)}<span class="lado" aria-hidden="true">D</span><figcaption><span>Criollo Palacios, F.</span><span>Citimed · Quito</span></figcaption></figure>
<nav class="visor" aria-labelledby="visor-t">
<div class="visor-titulo"><h2 id="visor-t">¿Qué le trae hoy?</h2><p>Elija su situación y empezamos por ahí.</p></div>
<ul>
<li><a href="{rel(r,'consulta-express/')}?motivo=tumor"><span class="rotulo">Placa 01</span><strong>Noté un bulto o un dolor en el hueso</strong><span>Le hago las preguntas de una primera consulta y recibo sus estudios.</span></a></li>
<li><a href="{rel(r,'segunda-opinion/')}"><span class="rotulo">Placa 02</span><strong>Ya tengo un diagnóstico</strong><span>Segunda opinión antes de una cirugía o un tratamiento largo.</span></a></li>
<li><a href="{rel(r,'consulta-express/')}?motivo=lesion"><span class="rotulo">Placa 03</span><strong>Tuve una lesión o una fractura</strong><span>Traumatología: fracturas, lesiones deportivas, mano y prótesis.</span></a></li>
<li><a href="{rel(r,'para-colegas/')}"><span class="rotulo">Placa 04</span><strong>Soy médico y quiero referir</strong><span>Qué enviar, cómo le respondo y cómo vuelve su paciente.</span></a></li>
</ul>
</nav>
</div></section>

<section class="ficha" aria-label="Trayectoria"><div class="contenedor"><dl>
<div><dt>Subespecialidad</dt><dd>Ortopedia oncológica<small>Universidad Militar Nueva Granada, Bogotá</small></dd></div>
<div><dt>Cargo</dt><dd>Ex jefe del Servicio de Ortopedia Oncológica<small>Directivo en SOLCA Quito</small></dd></div>
<div><dt>Investigación</dt><dd>152 pacientes<small>Serie de biopsia percutánea, publicada en 2015</small></dd></div>
<div><dt>Docencia y sociedades</dt><dd>Posgrado de Ortopedia<small>Universidad Central del Ecuador · ISOLS · SLATME</small></dd></div>
</dl></div></section>

<section class="seccion"><div class="contenedor">
<p class="antetitulo">Lo primero que conviene saber</p>
<p class="tesis">Antes de la biopsia, <span class="marcador">el cirujano</span>. El trayecto de la aguja decide cómo será la operación.</p>
<div class="tesis-pie"><p>En un posible tumor maligno, la biopsia es el primer paso de la cirugía. Si se toma por el lugar equivocado, la operación debe ser más amplia y la reconstrucción, más difícil.</p><a class="btn btn-linea" href="{rel(r,'biopsia/')}">Por qué importa quién la planifica</a></div>
</div></section>

<hr class="incision">

<section class="seccion"><div class="contenedor">
<p class="antetitulo">Especialidades</p>
<h2>Dos campos, un mismo cirujano</h2>
<div class="campos">
<article><span class="rotulo" style="color:var(--acento)">Su campo de mayor experiencia</span><h3>Ortopedia oncológica</h3>
<ol><li><a href="{rel(r,'especialidades/tumores-oseos/')}">Tumores óseos benignos y malignos</a></li><li><a href="{rel(r,'especialidades/sarcoma-de-partes-blandas/')}">Sarcomas de partes blandas</a></li><li><a href="{rel(r,'especialidades/metastasis-oseas/')}">Metástasis en huesos de brazos y piernas</a></li><li><a href="{rel(r,'especialidades/fractura-patologica/')}">Fracturas patológicas</a></li><li><a href="{rel(r,'especialidades/salvamento-de-extremidad/')}">Cirugía de salvamento de extremidad</a></li></ol></article>
<article><span class="rotulo" style="color:var(--gris)">Atención general</span><h3>Traumatología y ortopedia</h3>
<ol><li><span>Fracturas y luxaciones</span></li><li><span>Lesiones deportivas</span></li><li><span>Cirugía de mano</span></li><li><span>Prótesis de cadera y rodilla</span></li></ol>
<a class="mas" href="{rel(r,'especialidades/traumatologia/')}">Ver traumatología</a></article>
</div>
</div></section>

<section class="seccion oscura"><div class="contenedor dos">
<div class="texto">
<p class="antetitulo">Segunda opinión</p>
<h2>Una decisión que no tiene vuelta atrás merece <span class="marcador">una segunda mirada</span>.</h2>
<p class="entrada">Si ya tiene un diagnóstico, una resonancia o una biopsia, envíe sus estudios antes de viajar a Quito. El doctor los revisa, le entrega un informe escrito y se lo explica por videollamada.</p>
<div class="botones" style="margin-top:30px"><a class="btn" href="{rel(r,'segunda-opinion/')}">Cómo funciona y qué enviar</a>{cta(r,'segunda','Enviar mis estudios','btn btn-neutro')}</div>
</div>
<div class="media"><figure class="montada">{img(r,'felipe-quirofano','El Dr. Felipe Criollo Palacios operando junto a otro cirujano','8/7')}<figcaption><span>Quirófano</span><span>Quito</span></figcaption></figure></div>
</div></section>

<section class="seccion"><div class="contenedor">
<p class="antetitulo">Ficha médica inteligente</p>
<h2>Su caso, ordenado antes de la cita</h2>
<p class="entrada">La ficha médica inteligente le hace las preguntas que el doctor haría en la primera consulta. Usted responde con sus palabras y sube sus estudios. La valoración la hace el doctor.</p>
<ol class="pasos">
<li><strong>Elija el motivo</strong><span>Masa o tumor, lesión, dolor articular o control de una cirugía.</span></li>
<li><strong>Cuente su caso</strong><span>Una pregunta a la vez: cuándo empezó, cómo evoluciona, qué tratamientos recibió.</span></li>
<li><strong>Suba sus estudios</strong><span>Radiografías, resonancias, tomografías, informes o biopsias.</span></li>
<li><strong>Confirme y envíe</strong><span>Revisa el resumen y autoriza el uso de sus datos de salud{precio('precio_consulta', ', y paga {}, que se descuenta de su consulta', '')}.</span></li>
<li><strong>El doctor responde</strong><span>Su equipo le contacta con la propuesta: cita, teleconsulta o derivación.</span></li>
</ol>
<div class="botones" style="margin-top:40px;align-items:center">{cta(r)}<p class="nota" style="max-width:600px">La guía inteligente no diagnostica ni receta. Si describe una señal de alarma, le indica acudir a emergencias. <a href="{rel(r,'cuando-consultar/')}">Cuándo consultar sin esperar</a></p></div>
</div></section>

<section class="seccion blanca"><div class="contenedor">
<p class="antetitulo">Para leer con calma</p>
<h2>Las preguntas que más angustian</h2>
<div class="rejilla chica">
<a class="tarjeta" href="{rel(r,'especialidades/tumores-oseos/')}"><span class="eti">Tumores óseos</span><strong>¿Es benigno o maligno? Cómo se estudia un tumor en el hueso</strong></a>
<a class="tarjeta" href="{rel(r,'especialidades/sarcoma-de-partes-blandas/')}"><span class="eti">Partes blandas</span><strong>Un bulto que crece: por qué estudiarlo antes de operarlo</strong></a>
<a class="tarjeta" href="{rel(r,'especialidades/fractura-patologica/')}"><span class="eti">Fracturas</span><strong>Cuándo sospechar un tumor detrás de una fractura</strong></a>
<a class="tarjeta" href="{rel(r,'cuando-consultar/')}"><span class="eti">Señales de alarma</span><strong>Lo que no debe esperar a una cita</strong></a>
</div>
</div></section>

<section class="seccion"><div class="contenedor dos">
<div class="texto">
<p class="antetitulo">Dónde atiendo</p>
<h2>Citimed y Hospital Metropolitano, Quito</h2>
<p class="entrada">{D['direccion_citimed']}.</p>
<div class="botones" style="margin-top:28px"><a class="btn btn-linea" href="{rel(r,'donde-atiendo/')}">Horarios y cómo llegar</a><a class="btn btn-neutro" href="{rel(r,'fuera-de-quito/')}">Si vives fuera de Quito</a></div>
</div>
<div class="media"><figure class="montada">{img(r,'felipe-consultorio','El Dr. Felipe Criollo Palacios en su consultorio de Citimed','10/9')}<figcaption><span>Consultorio 628</span><span>Citimed</span></figcaption></figure></div>
</div></section>
""")

# ---------------------------------------------------------------- Especialidades
r = "especialidades/"
pagina(ruta=r, prioridad="0.8", titulo="Especialidades: ortopedia oncológica y traumatología",
       descripcion="Tumores óseos, sarcomas de partes blandas, metástasis óseas, fractura patológica, salvamento de extremidad y traumatología en Quito.",
       jsonld=[migas_ld(r, [("", "Inicio")], "Especialidades")],
       cuerpo=cabeza(r, [("", "Inicio")], "Especialidades", "Ortopedia oncológica y traumatología",
                     "La ortopedia oncológica trata los tumores de los huesos y de los tejidos blandos de brazos, piernas y pelvis. Es una subespecialidad poco frecuente: requiere coordinar el diagnóstico con radiología y patología, y el tratamiento con oncología clínica y radioterapia.") + f"""
<section class="seccion"><div class="contenedor">
<div class="rejilla chica">
<a class="tarjeta" href="{rel(r,'especialidades/tumores-oseos/')}"><span class="eti">Ortopedia oncológica</span><strong>Tumores óseos benignos y malignos</strong><p>Qué son, cómo se estudian y cuándo se operan.</p></a>
<a class="tarjeta" href="{rel(r,'especialidades/sarcoma-de-partes-blandas/')}"><span class="eti">Ortopedia oncológica</span><strong>Sarcoma de partes blandas</strong><p>Bultos en músculos y tejidos que merecen estudio antes de operarlos.</p></a>
<a class="tarjeta" href="{rel(r,'especialidades/metastasis-oseas/')}"><span class="eti">Ortopedia oncológica</span><strong>Metástasis óseas</strong><p>Prevenir y tratar fracturas cuando el cáncer llega al hueso.</p></a>
<a class="tarjeta" href="{rel(r,'especialidades/fractura-patologica/')}"><span class="eti">Ortopedia oncológica</span><strong>Fractura patológica</strong><p>Cuando el hueso se rompe porque estaba debilitado.</p></a>
<a class="tarjeta" href="{rel(r,'especialidades/salvamento-de-extremidad/')}"><span class="eti">Ortopedia oncológica</span><strong>Cirugía de salvamento de extremidad</strong><p>Quitar el tumor y reconstruir para conservar brazo o pierna.</p></a>
<a class="tarjeta" href="{rel(r,'biopsia/')}"><span class="eti">Diagnóstico</span><strong>La biopsia en un tumor óseo</strong><p>Por qué debe planificarla el cirujano que va a operar.</p></a>
<a class="tarjeta" href="{rel(r,'especialidades/traumatologia/')}"><span class="eti" style="color:var(--gris)">Atención general</span><strong>Traumatología y ortopedia</strong><p>Fracturas, lesiones deportivas, mano y prótesis.</p></a>
</div>
<p class="nota" style="margin-top:32px">¿Tiene dudas sobre si su caso corresponde a esta especialidad? {cta(r, None, 'Cuéntelo en la ficha médica inteligente', '')}.</p>
</div></section>""")


def condicion(slug, tema, titulo, descripcion, entrada, cuerpo, motivo="tumor"):
    r = f"especialidades/{slug}/"
    migas = [("", "Inicio"), ("especialidades/", "Especialidades")]
    pagina(ruta=r, prioridad="0.7", titulo=titulo, descripcion=descripcion,
           jsonld=[ld_pagina_medica(r, titulo, descripcion, tema), migas_ld(r, migas, tema)],
           cuerpo=cabeza(r, migas, "Ortopedia oncológica" if motivo == "tumor" else "Traumatología", titulo, entrada) +
           f'<section class="seccion"><div class="contenedor"><div class="prosa">{cuerpo}'
           f'<div class="caja"><p><strong>¿Quiere que el doctor revise su caso?</strong> Cuente su historia y suba sus estudios en la ficha médica inteligente. Si ya tiene un diagnóstico, puede pedir una <a href="{rel(r,"segunda-opinion/")}">segunda opinión</a>.</p><div class="botones" style="margin-top:14px">{cta(r, motivo)}</div></div>'
           f'{revisado()}</div></div></section>')


condicion("tumores-oseos", "Tumores óseos", "Tumores óseos: benignos y malignos",
          "Qué es un tumor óseo, cuáles son benignos y cuáles malignos, qué síntomas deben estudiarse y cómo se llega al diagnóstico.",
          "La mayoría de los tumores que aparecen en un hueso no son cáncer. Pero distinguir uno de otro exige estudiarlo bien, y en el orden correcto.", f"""
<h2>Qué es un tumor óseo</h2>
<p>Es un crecimiento anormal de células dentro de un hueso. Puede nacer en el propio hueso (tumor primario) o llegar desde otro órgano (metástasis). En adultos mayores de 40 años, una lesión agresiva en el hueso es con más frecuencia una metástasis o un mieloma que un tumor primario.</p>
<h2>Benignos y malignos</h2>
<p><strong>Benignos.</strong> Son los más frecuentes. Muchos se descubren por casualidad en una radiografía y solo necesitan controles. Algunos ejemplos son el osteocondroma, el encondroma, el quiste óseo y el fibroma no osificante. Otros, como el tumor de células gigantes, no se diseminan pero destruyen el hueso a su alrededor y requieren cirugía.</p>
<p><strong>Malignos primarios (sarcomas óseos).</strong> Son raros. Los más conocidos son el osteosarcoma y el sarcoma de Ewing, más frecuentes en niños, adolescentes y adultos jóvenes, y el condrosarcoma, más frecuente en adultos. Su tratamiento lo decide un equipo: cirugía, y según el tipo, quimioterapia o radioterapia.</p>
<h2>Síntomas que deben estudiarse</h2>
<ul><li>Dolor en un hueso que no se explica por un golpe, que dura semanas y que empeora de noche o en reposo.</li><li>Un bulto duro que crece.</li><li>Una fractura con un golpe menor, o sin golpe.</li><li>Cojera o limitación del movimiento sin causa clara, sobre todo en niños y adolescentes.</li></ul>
<p>Ninguno de estos síntomas significa por sí solo que haya un tumor. Significan que conviene una valoración. Vea también <a href="{rel('especialidades/tumores-oseos/','cuando-consultar/')}">cuándo consultar sin esperar</a>.</p>
<h2>Cómo se llega al diagnóstico</h2>
<ol><li><strong>Radiografía.</strong> Es el primer estudio y orienta mucho: dice si la lesión parece tranquila o agresiva.</li><li><strong>Resonancia magnética.</strong> Muestra la extensión dentro del hueso y hacia los tejidos de alrededor.</li><li><strong>Tomografía, gammagrafía o PET.</strong> Según el caso, para ver el detalle del hueso o buscar otras lesiones.</li><li><strong>Biopsia.</strong> Cuando la imagen no basta, se toma una muestra. En un posible tumor maligno, la biopsia debe planificarse con el cirujano que operará. <a href="{rel('especialidades/tumores-oseos/','biopsia/')}">Por qué importa tanto</a>.</li></ol>
<p>El orden importa: la biopsia va al final, cuando ya se cuenta con las imágenes, porque son ellas las que indican dónde y cómo tomar la muestra.</p>
""")

condicion("sarcoma-de-partes-blandas", "Sarcoma de partes blandas", "Sarcoma de partes blandas: cuándo un bulto merece estudio",
          "Los sarcomas de partes blandas son tumores raros de músculos, grasa y tejidos. Qué bultos deben estudiarse con resonancia antes de operarlos y por qué.",
          "Casi todos los bultos en los músculos o bajo la piel son benignos, como los lipomas. Unos pocos son sarcomas, y en ellos la primera cirugía decide mucho.", f"""
<h2>Qué es un sarcoma de partes blandas</h2>
<p>Es un tumor maligno que nace en los tejidos que unen y sostienen el cuerpo: músculo, grasa, tejido fibroso, vasos o nervios. Es poco frecuente y aparece sobre todo en muslos, brazos, glúteos y tronco. Suele crecer sin dolor, y por eso se confunde con un bulto inofensivo o con una lesión deportiva.</p>
<h2>Cuándo un bulto merece estudio</h2>
<p>Conviene que un especialista valore un bulto que reúne alguna de estas características:</p>
<ul><li>Mide más de 5 centímetros, el tamaño aproximado de una pelota de golf.</li><li>Está en la profundidad, debajo del músculo o fijo a él.</li><li>Crece con el paso de las semanas.</li><li>Reaparece después de haberse extirpado.</li></ul>
<h2>Por qué no conviene operarlo sin estudiarlo antes</h2>
<p>Cuando un sarcoma se extirpa como si fuera un bulto benigno, sin resonancia ni biopsia previas, suelen quedar células tumorales en la zona. Entonces hace falta una segunda cirugía más amplia, a veces con radioterapia, y la reconstrucción se vuelve más difícil. Por eso, ante un bulto con las características anteriores, el orden recomendado es: resonancia magnética, biopsia planificada por el cirujano oncólogo y, con el diagnóstico confirmado, la cirugía con márgenes adecuados.</p>
<div class="caja"><p>Si ya le operaron un bulto y el informe de patología dice «sarcoma», no se alarme por la palabra: pida una valoración con ese informe y las imágenes previas. Es justamente el tipo de caso en el que una <a href="{rel('especialidades/sarcoma-de-partes-blandas/','segunda-opinion/')}">segunda opinión</a> ayuda a decidir el siguiente paso.</p></div>
<h2>Tratamiento</h2>
<p>La base es la cirugía que extirpa el tumor con un margen de tejido sano, conservando la extremidad siempre que sea posible. Según el tipo y el tamaño, se combina con radioterapia o quimioterapia, en coordinación con oncología clínica y radioterapia.</p>
""")

condicion("metastasis-oseas", "Metástasis óseas", "Metástasis óseas en brazos y piernas",
          "Qué son las metástasis óseas, cuándo hay riesgo de fractura y cómo la cirugía ortopédica ayuda a aliviar el dolor y conservar la movilidad.",
          "Cuando un cáncer llega al hueso, el objetivo de la ortopedia oncológica es aliviar el dolor, evitar las fracturas y mantener la independencia del paciente.", f"""
<h2>Qué son</h2>
<p>Son focos de un cáncer que se originó en otro órgano y llegó al hueso. Son mucho más frecuentes que los tumores óseos primarios. Los cánceres que con más frecuencia afectan el hueso son los de mama, próstata, pulmón, riñón y tiroides; el mieloma múltiple también afecta el hueso.</p>
<h2>Por qué importa el ortopedista oncólogo</h2>
<p>Una metástasis debilita el hueso. En los huesos largos que cargan peso, como el fémur, puede llegar a romperlo. Valorar a tiempo ese riesgo permite decidir si basta con radioterapia y controles, o si conviene reforzar el hueso con una cirugía antes de que se fracture. Una cirugía programada suele ser más sencilla y de mejor recuperación que una de urgencia.</p>
<h2>Señales que deben consultarse pronto</h2>
<ul><li>Dolor que aumenta al cargar peso o al usar el brazo, en una persona con diagnóstico de cáncer.</li><li>Dolor que no cede con la medicación habitual o que despierta en la noche.</li><li>Debilidad u hormigueo en las piernas con dolor de espalda: esto requiere atención de emergencia.</li></ul>
<h2>Cómo se trabaja</h2>
<p>El tratamiento se decide en conjunto con el oncólogo clínico y el radioterapeuta, según el tipo de cáncer, el estado general del paciente y lo que el paciente prioriza. La cirugía puede estabilizar el hueso con clavos o placas, o reemplazar la zona afectada con una prótesis. La meta es que el paciente pueda caminar, cuidarse y continuar su tratamiento oncológico con el menor dolor posible.</p>
""")

condicion("fractura-patologica", "Fractura patológica", "Fractura patológica: cuando el hueso se rompe porque estaba débil",
          "Qué es una fractura patológica, cuándo sospechar un tumor detrás de una fractura y por qué conviene estudiarla antes de fijarla.",
          "Algunas fracturas no se deben al golpe sino a que el hueso ya estaba debilitado. Reconocerlas a tiempo cambia el tratamiento.", f"""
<h2>Qué es</h2>
<p>Es una fractura que ocurre en un hueso debilitado por otra causa: un quiste, un tumor benigno, una metástasis, un tumor maligno primario o una enfermedad del hueso como la osteoporosis. Lo característico es que el golpe que la produjo es menor que el que normalmente rompería un hueso sano, o que no hubo golpe.</p>
<h2>Cuándo sospecharla</h2>
<ul><li>La fractura ocurrió con un movimiento cotidiano o una caída leve.</li><li>Había dolor en esa zona desde semanas antes, sobre todo de noche.</li><li>La radiografía muestra una zona del hueso con aspecto distinto alrededor de la fractura.</li><li>El paciente tiene o tuvo un cáncer.</li></ul>
<h2>Por qué se estudia antes de fijarla</h2>
<p>Si detrás de la fractura hay un tumor maligno primario, fijarla de inmediato con clavos o placas sin conocer el diagnóstico puede diseminar el tumor por el hueso y los tejidos, y complicar una futura cirugía de salvamento. Por eso, cuando la fractura o el dolor previo hacen sospechar una lesión, conviene inmovilizar, estudiar con imágenes y, si hace falta, tomar una biopsia planificada antes de decidir la cirugía definitiva.</p>
<div class="caja"><p>El {D['nombre']} escribió sobre este tema en su artículo «Sobre las fracturas patológicas». <span class="pendiente">[ENLACE AL ARTÍCULO O VERSIÓN EN EL BLOG]</span></p></div>
""")

condicion("salvamento-de-extremidad", "Cirugía de salvamento de extremidad", "Cirugía de salvamento de extremidad",
          "Qué es la cirugía de salvamento de extremidad en tumores óseos y de partes blandas, cómo se reconstruye el hueso y qué esperar de la recuperación.",
          "Hoy, en la mayoría de los tumores malignos de brazos y piernas, es posible quitar el tumor y conservar la extremidad. Lograrlo depende de un diagnóstico bien planificado desde el principio.", f"""
<h2>Qué es</h2>
<p>Es la cirugía que extirpa el tumor con un margen de tejido sano y reconstruye la zona para conservar un brazo o una pierna funcional, en lugar de amputar. Se planifica con las imágenes y la biopsia, y casi siempre se combina con quimioterapia o radioterapia según el tipo de tumor.</p>
<h2>Cómo se reconstruye</h2>
<ul><li><strong>Endoprótesis.</strong> Una prótesis metálica a medida reemplaza el hueso y, con frecuencia, la articulación cercana.</li><li><strong>Injertos de hueso.</strong> Hueso de banco o del propio paciente rellena el defecto.</li><li><strong>Peroné vascularizado.</strong> Se traslada un segmento del peroné con sus vasos sanguíneos, para que siga vivo en su nueva ubicación. El doctor ha aplicado esta técnica, por ejemplo, en la reconstrucción del húmero proximal.</li><li><strong>Combinaciones.</strong> En casos complejos se combinan prótesis e injertos.</li></ul>
<h2>Cuándo no es posible</h2>
<p>A veces el tumor compromete nervios o vasos principales, o la amputación ofrece un mejor control de la enfermedad y una mejor función con prótesis externa. Es una decisión que se toma con el paciente y el equipo, con información clara de las opciones.</p>
<h2>Qué esperar</h2>
<p>La recuperación incluye rehabilitación prolongada y controles periódicos de imagen. El resultado funcional depende del sitio del tumor, de la reconstrucción y del tratamiento complementario, por lo que se conversa de manera individual en la consulta.</p>
""")

condicion("traumatologia", "Traumatología y ortopedia", "Traumatología y ortopedia en Quito",
          "Fracturas, luxaciones, lesiones deportivas, cirugía de mano y prótesis de cadera y rodilla con el Dr. Felipe Criollo Palacios en Quito.",
          "Además de la ortopedia oncológica, el doctor atiende la traumatología y la ortopedia de todos los días.", f"""
<h2>Qué atiende</h2>
<ul><li><strong>Fracturas y luxaciones</strong> de brazos, piernas, mano y pie, con tratamiento conservador o quirúrgico.</li><li><strong>Lesiones deportivas</strong>: esguinces, lesiones de ligamentos y tendones.</li><li><strong>Cirugía de mano.</strong></li><li><strong>Prótesis de cadera y rodilla</strong> por artrosis u otras causas.</li><li><strong>Diagnóstico de dolor y lesiones musculoesqueléticas</strong>.</li></ul>
<h2>Cuándo ir a emergencias</h2>
<div class="alarma-caja"><p><strong>No espere a una cita</strong> si hay una deformidad visible, el hueso asoma por la piel, pierde la sensibilidad o la fuerza de un brazo o una pierna, la extremidad se pone fría o pálida, o tiene fiebre con una herida quirúrgica que supura. Acuda a emergencias o llame al 911.</p></div>
<h2>Para todo lo demás</h2>
<p>Cuente su caso en la ficha médica inteligente y suba la radiografía o el informe que tenga. El equipo del doctor le contactará para proponerle el siguiente paso.</p>
""", motivo="lesion")

# ---------------------------------------------------------------- Biopsia
r = "biopsia/"
t = "Por qué la biopsia de un tumor óseo debe planificarla el cirujano que va a operar"
d = "En un posible tumor maligno del hueso o de partes blandas, una biopsia mal ubicada puede complicar la cirugía. Qué es la biopsia percutánea y por qué se planifica con el cirujano."
pagina(ruta=r, prioridad="0.8", titulo=t, descripcion=d,
       jsonld=[ld_pagina_medica(r, t, d, "Biopsia de tumor óseo"), migas_ld(r, [("", "Inicio"), ("especialidades/", "Especialidades")], "Biopsia")],
       cuerpo=cabeza(r, [("", "Inicio"), ("especialidades/", "Especialidades")], "Antes de cualquier biopsia", t,
                     "Es el mensaje más importante de la ortopedia oncológica, y uno de los menos conocidos: la biopsia no es solo tomar una muestra; es el primer paso de la cirugía.") + f"""
<section class="seccion"><div class="contenedor"><div class="prosa">
<h2>Qué es una biopsia</h2>
<p>Es tomar una muestra del tumor para que el patólogo la analice al microscopio y diga qué es. Sin ese diagnóstico no se puede decidir el tratamiento: un tumor benigno, un sarcoma y una metástasis se tratan de maneras muy distintas.</p>
<h2>Por qué importa quién la planifica</h2>
<p>En un tumor maligno, el trayecto por donde pasa la aguja o el bisturí queda contaminado con células tumorales. Por eso, en la cirugía definitiva ese trayecto debe extirparse junto con el tumor. Si la biopsia se tomó por un lugar que el cirujano no habría elegido, por ejemplo atravesando un compartimento muscular sano o cerca de un nervio, la cirugía tiene que ser más amplia, la reconstrucción más difícil y, en algunos casos, se pierde la posibilidad de conservar la extremidad.</p>
<div class="caja"><p><strong>La regla práctica:</strong> si una radiografía o una resonancia muestran una lesión que podría ser maligna, lo recomendable es consultar con el ortopedista oncólogo antes de la biopsia, no después. Él decide el sitio y el método pensando en la cirugía que vendrá.</p></div>
<h2>La biopsia percutánea</h2>
<p>En la mayoría de los casos la muestra puede tomarse con una aguja gruesa, guiada por tomografía o ecografía, a través de un pequeño orificio en la piel. Es menos invasiva que una biopsia abierta, se hace con anestesia local o sedación y deja un trayecto pequeño y fácil de extirpar después. El radiólogo intervencionista y el cirujano acuerdan de antemano el punto de entrada.</p>
<h2>La experiencia del doctor</h2>
<p>El {D['nombre']} publicó en 2015 el artículo «Biopsia percutánea en ortopedia oncológica. Serie de casos», en la Revista Colombiana de Ortopedia y Traumatología, con una serie de 152 pacientes. <span class="pendiente">[ENLACE AL ARTÍCULO Y, SI EL DOCTOR LO APRUEBA, UNA FRASE CON SU HALLAZGO PRINCIPAL]</span></p>
<h2>Si ya le hicieron una biopsia</h2>
<p>No se preocupe: muchas biopsias se hacen bien en cualquier centro. Lo importante es que el cirujano que va a operar conozca dónde y cómo se tomó. Envíe el informe de patología, las imágenes previas y, si la tiene, la descripción del procedimiento en la ficha médica inteligente o en una <a href="{rel(r,'segunda-opinion/')}">segunda opinión</a>.</p>
<div class="botones" style="margin:28px 0">{cta(r,'tumor')}<a class="btn btn-neutro" href="{rel(r,'para-colegas/')}">Soy médico y quiero referir</a></div>
{revisado()}
</div></div></section>""")

# ---------------------------------------------------------------- Segunda opinión
r = "segunda-opinion/"
pagina(ruta=r, prioridad="0.9", titulo="Segunda opinión en ortopedia oncológica",
       descripcion="Segunda opinión sobre tumores óseos, sarcomas y metástasis: qué enviar, quién revisa, qué recibes y cuánto cuesta. Para pacientes de Quito, provincia y el exterior.",
       jsonld=[migas_ld(r, [("", "Inicio")], "Segunda opinión"),
               {"@context": "https://schema.org", "@type": "MedicalProcedure", "name": "Segunda opinión en ortopedia oncológica", "procedureType": "https://schema.org/NoninvasiveProcedure",
                "description": "Revisión de estudios, informe escrito y videollamada con el Dr. Felipe Criollo Palacios.", "url": D["dominio"] + "/" + r}],
       cuerpo=cabeza(r, [("", "Inicio")], "Servicio en línea", "Segunda opinión en ortopedia oncológica",
                     "Si ya tienes un diagnóstico o una propuesta de tratamiento y quieres confirmarla antes de decidir: una cirugía, un salvamento de extremidad, una amputación o un tratamiento largo.") + f"""
<section class="seccion"><div class="contenedor">
<h2>Cómo funciona</h2>
<ol class="pasos">
<li><strong>Cuenta tu caso</strong><span>En la ficha médica inteligente, elige «Segunda opinión». La guía inteligente te pregunta por el diagnóstico, el tratamiento propuesto y cómo llegaste hasta aquí.</span></li>
<li><strong>Sube tus documentos</strong><span>Informes, imágenes y patología. Más abajo está la lista exacta.</span></li>
<li><strong>Autoriza el envío</strong><span>Autorizas el uso de tus datos de salud para la revisión{precio('precio_segunda', ' y pagas {}', '')}.</span></li>
<li><strong>El doctor revisa</strong><span>Revisa personalmente tus estudios. Si falta algo importante, su equipo te lo pide.</span></li>
<li><strong>Recibes tu informe</strong><span>Un informe escrito y una videollamada con el doctor para explicártelo y responder tus preguntas.</span></li>
</ol>
<div class="botones" style="margin-top:32px">{cta(r,'segunda','Pedir una segunda opinión')}</div>
<p class="nota" style="margin-top:16px">El equipo del doctor te contacta cuando tu caso esté revisado. El tiempo depende de la complejidad y de que los estudios estén completos.</p>
</div></section>

<section class="seccion blanca"><div class="contenedor"><div class="prosa">
<h2>Qué documentos enviar</h2>
<p>Cuanto más completo llegue tu caso, más precisa será la opinión. Reúne lo que tengas de esta lista:</p>
<table><thead><tr><th>Documento</th><th>Por qué importa</th></tr></thead><tbody>
<tr><td><strong>Imágenes originales</strong>: resonancia, tomografía, radiografías, PET o gammagrafía. Idealmente en formato DICOM (el disco o el enlace que entrega el centro de imagen).</td><td>El doctor necesita ver las imágenes, no solo leer el informe. Si solo tienes fotos o PDF, envíalos igual.</td></tr>
<tr><td><strong>Informes de radiología</strong> de cada estudio.</td><td>Ubican cada hallazgo y su fecha.</td></tr>
<tr><td><strong>Informe de patología</strong> de la biopsia o de la cirugía, si se hizo.</td><td>Es la base del diagnóstico. En algunos casos se pedirán las láminas o los bloques para revisión.</td></tr>
<tr><td><strong>Nota operatoria</strong>, si ya te operaron.</td><td>Indica qué se hizo, por dónde y qué quedó.</td></tr>
<tr><td><strong>Tratamientos recibidos</strong>: quimioterapia, radioterapia, medicamentos.</td><td>Cambian las opciones de cirugía y reconstrucción.</td></tr>
<tr><td><strong>La propuesta de tratamiento</strong> que te hicieron.</td><td>Es lo que la segunda opinión va a confirmar o a matizar.</td></tr>
</tbody></table>
<p>Los archivos muy pesados, como los discos DICOM completos, pueden enviarse con el enlace de descarga del centro de imagen. <span class="pendiente">[CONFIRMAR CON EL DOCTOR EL CANAL PARA DICOM GRANDES]</span></p>

<h2>Qué recibe</h2>
<ul><li>Un <strong>informe escrito</strong> del {D['nombre']} con su lectura del caso, su opinión sobre el diagnóstico y el tratamiento propuesto, y los estudios adicionales que recomendaría si hacen falta.</li><li>Una <strong>videollamada</strong> para explicarte el informe a ti y a tu familia.</li><li>Si tu caso lo requiere, la propuesta de una cita presencial en Quito. <a href="{rel(r,'fuera-de-quito/')}">Si vives fuera de Quito</a>.</li></ul>
<h2>Cuánto cuesta</h2>
<p>{precio('precio_segunda', 'La segunda opinión con informe escrito y videollamada cuesta {}. Se paga en línea al enviar el caso.', 'El consultorio te informa el valor de la segunda opinión antes de iniciar la revisión.')} <span class="pendiente">[CONFIRMAR SI SE DESCUENTA DE UNA CIRUGÍA O CONSULTA POSTERIOR]</span></p>
<h2>Lo que la segunda opinión no es</h2>
<p>No es una atención de urgencia ni reemplaza el seguimiento con tu médico tratante. Si tu médico te refirió, el doctor puede enviarle también a él el informe, con tu autorización. Si presentas una <a href="{rel(r,'cuando-consultar/')}">señal de alarma</a>, acude a emergencias.</p>
<h2>Preguntas frecuentes</h2>
</div>
<div class="estrecho">
<details><summary>¿Tengo que decirle a mi médico que pido una segunda opinión?</summary><p>No es obligatorio, pero es lo habitual y la mayoría de los médicos lo ven bien. Una segunda opinión suele dar tranquilidad a todos y, si tu médico lo desea, el doctor puede comentarle el caso.</p></details>
<details><summary>Me dijeron que la única opción es amputar. ¿Vale la pena consultar?</summary><p>Sí. Es una decisión irreversible y merece una segunda mirada. A veces la amputación sí es la mejor opción, y otras veces existe una alternativa de salvamento. El doctor te explicará con claridad cuál es tu caso.</p></details>
<details><summary>¿Puedo pedirla si vivo en el exterior?</summary><p>Sí. Todo el proceso es en línea. La videollamada se coordina según tu zona horaria.</p></details>
<details><summary>¿Quién ve mis estudios?</summary><p>El doctor y su equipo, solo para revisar tu caso, conforme a la Ley Orgánica de Protección de Datos Personales. Detalles en el <a href="{rel(r,'privacidad/')}">aviso de privacidad</a>.</p></details>
</div>
</div></section>""")

# ---------------------------------------------------------------- Perfil
r = "perfil/"
cv = f'<a class="btn btn-linea" href="{rel(r, D["cv_pdf"])}">Descargar currículum (PDF)</a>' if D["cv_pdf"] else '<span class="pendiente">[CURRÍCULUM EN PDF]</span>'
pagina(ruta=r, prioridad="0.9", titulo="Perfil y formación",
       descripcion="Formación, cargos, publicaciones y sociedades científicas del Dr. Felipe Criollo Palacios, cirujano ortopedista oncólogo en Quito.",
       jsonld=[MEDICO_LD, migas_ld(r, [("", "Inicio")], "Perfil")],
       cuerpo=cabeza(r, [("", "Inicio")], "Sobre el doctor", D["nombre"], "Cirujano ortopedista oncólogo. Atiende en su consultorio de Citimed e interviene en casos complejos en el Hospital Metropolitano y en el Hospital Vozandes, en Quito.") + f"""
<section class="seccion"><div class="contenedor dos" style="align-items:flex-start">
<div class="texto prosa">
<h2 style="margin-top:0">A qué se dedica</h2>
<p>El doctor Criollo es cirujano ortopedista oncólogo. Su práctica se concentra en el diagnóstico y el tratamiento de los tumores musculoesqueléticos y en las reconstrucciones de extremidades de alta complejidad, además de la traumatología y la ortopedia general.</p>
<ul><li>Tumores óseos y sarcomas, primarios y secundarios</li><li>Metástasis óseas en las extremidades</li><li>Cirugía de salvamento de extremidad</li><li>Reconstrucciones con prótesis tumorales, aloinjertos y osteosíntesis</li><li>Lesiones pseudotumorales, como los quistes óseos</li><li>Traumatología y ortopedia</li></ul>
<h2>Formación</h2>
<table><tbody>
<tr><th>Subespecialidad</th><td>Fellowship en Ortopedia Oncológica. Universidad Militar Nueva Granada e Instituto Nacional de Cancerología, Bogotá, Colombia.</td></tr>
<tr><th>Especialidad</th><td>Ortopedia y Traumatología. Universidad Central del Ecuador.</td></tr>
<tr><th>Medicina</th><td>Médico. Universidad Central del Ecuador. Fue ayudante de cátedra de Bioquímica y de Anatomía Patológica.</td></tr>
<tr><th>Otros estudios</th><td>Diplomado en Medicina Transfusional. Universidad Central del Ecuador.</td></tr>
</tbody></table>
<h2>Dónde ejerce</h2>
<ul><li><strong>Hospital Metropolitano, Quito.</strong> Cirujano ortopedista oncólogo y coordinador de Tumores Musculoesqueléticos.</li><li><strong>Hospital Vozandes Quito.</strong> Traumatólogo oncólogo; interviene en los casos complejos para los que se le llama.</li><li><strong>Consulta privada</strong> en el Centro Médico Citimed, Quito.</li></ul>
<h2>Trayectoria</h2>
<ul><li><strong>SOLCA Quito.</strong> Ortopedista oncólogo y directivo de la institución durante más de diez años: sarcomas, lesiones metastásicas y lesiones pseudotumorales.</li><li><strong>Instituto Ecuatoriano de Seguridad Social, Latacunga.</strong> Traumatólogo y ortopedista.</li></ul>
<h2>Docencia</h2>
<p>Desde 2013 es docente del Instituto Superior de Posgrado de la Universidad Central del Ecuador, donde enseña ortopedia oncológica y manejo de sarcomas en los posgrados de Ortopedia y Traumatología, Oncología Clínica y Cirugía Oncológica. Ha sido profesor ocasional del posgrado de Traumatología y Ortopedia de la Universidad San Francisco de Quito.</p>
<h2>Sociedades científicas</h2>
<ul><li>ISOLS, International Society of Limb Salvage</li><li>SLATME, Sociedad Latinoamericana de Tumores Musculoesqueléticos</li><li>Sociedad Ecuatoriana de Oncología</li></ul>
<h2>Trabajo en equipo</h2>
<p>La ortopedia oncológica se hace en equipo. Cada caso se coordina con especialistas de radiología, patología, oncología clínica, radioterapia, cirugía plástica y reconstructiva, y rehabilitación física.</p>
<p>El doctor comparte casos clínicos con otros especialistas en <a href="https://www.linkedin.com/in/felipecriollo/" rel="noopener">su perfil de LinkedIn</a>.</p>
</div>
<div class="media" style="position:sticky;top:100px">{img(r,'felipe-retrato','Retrato del Dr. Felipe Criollo Palacios')}
<div class="botones" style="margin-top:16px">{cta(r)}</div></div>
</div></section>""")

# ---------------------------------------------------------------- Para colegas
r = "para-colegas/"
pagina(ruta=r, prioridad="0.8", titulo="Para colegas que refieren pacientes",
       descripcion="Cómo referir un paciente con un tumor óseo, un sarcoma o una metástasis al Dr. Felipe Criollo Palacios: cuándo referir, qué enviar y cómo se informa al médico de origen.",
       jsonld=[migas_ld(r, [("", "Inicio")], "Para colegas")],
       cuerpo=cabeza(r, [("", "Inicio")], "Para médicos", "Para colegas que refieren pacientes",
                     "Si atiende a un paciente con una lesión ósea o de partes blandas que le preocupa, puede enviarme el caso con sus estudios. Le respondo a usted, y el paciente vuelve a su consulta para el seguimiento que le corresponde.") + f"""
<section class="seccion"><div class="contenedor"><div class="prosa">
<h2>Cuándo conviene referir</h2>
<ul><li>Una lesión ósea con signos de agresividad en la radiografía: bordes mal definidos, reacción perióstica, destrucción cortical o masa de partes blandas asociada.</li><li>Un bulto de partes blandas de más de 5 cm, profundo o que crece.</li><li><strong>Antes de la biopsia</strong> de una lesión que podría ser maligna. Es el momento más útil para referir. <a href="{rel(r,'biopsia/')}">Por qué</a>.</li><li>Un resultado de patología inesperado tras extirpar un bulto que parecía benigno.</li><li>Un paciente oncológico con dolor óseo en un hueso que carga peso o con riesgo de fractura.</li><li>Una fractura con sospecha de lesión subyacente, antes de fijarla.</li></ul>
<h2>Qué enviar</h2>
<ul><li>Resumen clínico breve y su pregunta concreta.</li><li>Imágenes, idealmente en DICOM, e informes de radiología.</li><li>Informe de patología, si existe.</li><li>Sus datos de contacto para la respuesta.</li></ul>
<div class="caja"><p>Pídale al paciente su autorización para compartir sus datos de salud conmigo. El formulario para colegas incluye esa constancia.</p></div>
<h2>Cómo le respondo</h2>
<p><span class="pendiente">[CONFIRMAR CON EL DOCTOR: INFORME ESCRITO, LLAMADA O AMBOS, Y POR QUÉ CANAL]</span> Si el paciente necesita una valoración presencial, mi equipo lo coordina y le mantengo al tanto de la conducta. Para casos urgentes, llame al consultorio: {D['telefono']}.</p>
<h2>El paciente vuelve a usted</h2>
<p>Mi trabajo es resolver la parte de ortopedia oncológica. El control general, el manejo de otras enfermedades y el seguimiento que no sea de mi especialidad se mantienen con el médico que refiere, y le envío la información necesaria para continuar.</p>
<div class="botones" style="margin:32px 0">{cta(r,'colega','Enviar un caso')}<a class="btn btn-neutro" href="{rel(r,'perfil/')}">Ver mi perfil y publicaciones</a></div>
</div></div></section>""")

# ---------------------------------------------------------------- Fuera de Quito
r = "fuera-de-quito/"
pagina(ruta=r, prioridad="0.7", titulo="Si vives fuera de Quito o en el exterior",
       descripcion="Cómo consultar con el Dr. Felipe Criollo Palacios desde provincia o el exterior: qué enviar antes, cómo se coordina la visita y dónde atiende en Quito.",
       jsonld=[migas_ld(r, [("", "Inicio")], "Si vives fuera de Quito")],
       cuerpo=cabeza(r, [("", "Inicio")], "Pacientes de provincia y del exterior", "Si vives fuera de Quito",
                     "Viajar por un problema de salud cuesta tiempo, dinero y cansancio. Por eso el primer paso se hace a distancia: el doctor revisa tu caso antes de que viajes.") + f"""
<section class="seccion"><div class="contenedor">
<ol class="pasos">
<li><strong>Envía tu caso antes</strong><span>Por la ficha médica inteligente o la segunda opinión, con tus estudios.</span></li>
<li><strong>El doctor decide contigo</strong><span>Si basta una teleconsulta, si necesitas estudios adicionales en tu ciudad o si conviene venir.</span></li>
<li><strong>La visita, bien preparada</strong><span>Si vienes, su equipo coordina la cita y, en lo posible, los estudios del mismo viaje.</span></li>
<li><strong>Seguimiento a distancia</strong><span>Los controles que lo permitan se hacen por teleconsulta, con tu médico local.</span></li>
</ol>
<div class="prosa" style="margin-top:48px">
<h2>Qué esperar el día de la cita</h2>
<p>Trae tus estudios originales (discos de imagen, informes y láminas de patología si te las entregaron), la lista de tus medicamentos y, si puedes, un acompañante.</p>
<h2>Consultorio</h2>
<p>{D['direccion_citimed']}. Las cirugías se realizan en el Hospital Metropolitano, Av. Mariana de Jesús y Nicolás Arteta, a pocas cuadras del consultorio. <a href="{rel(r,'donde-atiendo/')}">Mapas y horarios</a>.</p>
<h2>Desde el exterior</h2>
<p>Todo el proceso inicial es en línea. La videollamada se coordina según tu zona horaria y el pago puede hacerse con tarjeta internacional. <span class="pendiente">[CONFIRMAR CON EL DOCTOR SI OFRECE APOYO PARA ALOJAMIENTO O TRASLADOS]</span></p>
<div class="botones" style="margin:28px 0">{cta(r)}<a class="btn btn-neutro" href="{rel(r,'segunda-opinion/')}">Pedir una segunda opinión</a></div>
</div>
</div></section>""")

# ---------------------------------------------------------------- Dónde atiendo
r = "donde-atiendo/"
tel = f'<a href="tel:{D["telefono_enlace"]}">{D["telefono"]}</a>' if D["telefono_enlace"] else D["telefono"]
mapa = lambda q, titulo: (f'<div class="mapa mapa-sustituto" data-mapa="{q}" data-titulo="{titulo}"><p>El mapa se carga desde Google Maps.<br>'
                          f'<button class="btn btn-linea" type="button" style="margin-top:12px">Mostrar el mapa</button><br><a href="https://www.google.com/maps/search/?api=1&query={q}" rel="noopener">Abrir en Google Maps</a></p></div>')
pagina(ruta=r, prioridad="0.8", titulo="Consultorio: Citimed y Hospital Metropolitano, Quito",
       descripcion="Consulta privada en el Centro Médico Citimed, piso 6, consultorio 628, y cirugías en el Hospital Metropolitano de Quito. Cómo llegar.",
       jsonld=[MEDICO_LD, migas_ld(r, [("", "Inicio")], "Consultorio")], scripts=("assets/mapa.js",),
       cuerpo=cabeza(r, [("", "Inicio")], "", "Consultorio") + f"""
<section class="seccion"><div class="contenedor">
<div class="rejilla">
<article class="tarjeta destacada"><p class="eti">Consulta privada</p><h3>Centro Médico Citimed</h3>
<p>Piso 6, consultorio 628<br>Av. Mariana de Jesús y Nuño de Valderrama, Quito</p>
<p>Horario: {D['horario_citimed']}</p>{f'<p>Teléfono: {tel}</p>' if D['telefono'] else ''}{f'<p><a href="{D["whatsapp_enlace"]}" rel="noopener">Escribir por WhatsApp</a></p>' if D["whatsapp_enlace"] else ""}
{mapa('Citimed+Mariana+de+Jesus+Quito', 'Mapa de Citimed')}</article>
<article class="tarjeta"><p class="eti">Cirugías y casos complejos</p><h3>Hospital Metropolitano</h3>
<p>Av. Mariana de Jesús y Nicolás Arteta, Quito</p>
<p>Horario: {D['horario_metropolitano']}</p>
{mapa('Hospital+Metropolitano+Quito', 'Mapa del Hospital Metropolitano')}</article>
</div>
<div class="dos" style="margin-top:56px">
<div class="texto"><h2>Antes de venir</h2><p class="entrada">Si cuentas tu caso en la ficha médica inteligente, el doctor llega a la cita conociendo tu historia y tus estudios, y no repites todo desde cero.</p><div class="botones" style="margin-top:24px">{cta(r)}</div></div>
<div class="media">{img(r,'felipe-consultorio','El Dr. Felipe Criollo Palacios en su consultorio de Citimed','10/9')}</div>
</div>
</div></section>""")

# ---------------------------------------------------------------- Cuándo consultar sin esperar
r = "cuando-consultar/"
t = "Cuándo consultar sin esperar"
d = "Señales que no deben esperar: dolor óseo que despierta de noche, un bulto que crece, una fractura sin golpe que la explique, y cuándo acudir directamente a emergencias."
pagina(ruta=r, prioridad="0.7", titulo=t, descripcion=d,
       jsonld=[ld_pagina_medica(r, t, d, "Señales de alarma musculoesqueléticas"), migas_ld(r, [("", "Inicio")], t)],
       cuerpo=cabeza(r, [("", "Inicio")], "Señales de alarma", t, "Algunas molestias pueden esperar a una cita programada. Otras no.") + f"""
<section class="seccion"><div class="contenedor"><div class="prosa">
<div class="alarma-caja"><p><strong>Acuda hoy a emergencias o llame al 911 si:</strong></p><ul style="margin:10px 0 0"><li>Hay una deformidad visible después de un golpe o el hueso asoma por la piel.</li><li>Pierde la sensibilidad o la fuerza de un brazo o una pierna.</li><li>La extremidad está fría, pálida o morada.</li><li>Tiene fiebre y una herida quirúrgica enrojecida o que supura.</li><li>Tiene dolor de espalda con debilidad de las piernas o dificultad para orinar, sobre todo si tiene un diagnóstico de cáncer.</li><li>Una pierna está hinchada, caliente y dolorosa después de una cirugía o una inmovilización.</li></ul></div>
<h2>Pida una valoración pronto, en los próximos días, si:</h2>
<ul><li>Tiene un dolor en un hueso que dura más de unas semanas, que no se explica por un golpe y que lo despierta en la noche o no cede en reposo.</li><li>Nota un bulto que crece, sobre todo si mide más de 5 cm o está en la profundidad del músculo.</li><li>Se fracturó con un golpe menor o sin golpe.</li><li>Un niño o un adolescente cojea o se queja de dolor en un hueso sin causa clara.</li><li>Tiene un diagnóstico de cáncer y aparece dolor en un hueso que carga peso.</li></ul>
<p>En estos casos puede contar su caso en la ficha médica inteligente. La guía inteligente está programada para reconocer las señales de alarma y, si las detecta, le indicará acudir a emergencias en lugar de esperar.</p>
<div class="botones" style="margin:28px 0">{cta(r)}</div>
{revisado()}
</div></div></section>""")

# ---------------------------------------------------------------- Casos y publicaciones
r = "casos-y-publicaciones/"
pagina(ruta=r, prioridad="0.6", titulo="Casos y publicaciones",
       descripcion="Casos de cirugía de salvamento de extremidad y reconstrucción, y publicaciones del Dr. Felipe Criollo Palacios en ortopedia oncológica.",
       jsonld=[migas_ld(r, [("", "Inicio")], "Casos y publicaciones")],
       cuerpo=cabeza(r, [("", "Inicio")], "", "Casos y publicaciones", "Cirugía de salvamento de extremidad y reconstrucción en tumores óseos. Los casos se publican con el consentimiento escrito de cada paciente y sin datos que permitan identificarlo.") + f"""
<section class="seccion"><div class="contenedor">
<div class="rejilla chica">
<article class="tarjeta"><span class="eti">Caso clínico</span><strong>Reconstrucción de húmero proximal con peroné vascularizado</strong><p><span class="pendiente">[RESUMEN E IMÁGENES, CON CONSENTIMIENTO]</span></p></article>
<article class="tarjeta"><span class="eti">Caso clínico</span><strong>Resección de hombro con técnica de Tikhoff-Linberg modificada</strong><p><span class="pendiente">[RESUMEN E IMÁGENES, CON CONSENTIMIENTO]</span></p></article>
<article class="tarjeta"><span class="eti">Caso clínico</span><strong>Condrosarcoma del segundo metacarpiano</strong><p><span class="pendiente">[RESUMEN E IMÁGENES, CON CONSENTIMIENTO]</span></p></article>
<article class="tarjeta"><span class="eti" style="color:var(--gris)">Publicación · 2015</span><strong>Biopsia percutánea en ortopedia oncológica. Serie de casos</strong><p>Revista Colombiana de Ortopedia y Traumatología. 152 pacientes. <a href="{rel(r,'biopsia/')}">Por qué importa</a></p></article>
<article class="tarjeta"><span class="eti" style="color:var(--gris)">Artículo</span><strong>Sobre las fracturas patológicas</strong><p>Qué son y cuándo sospechar un tumor detrás de una fractura. <a href="{rel(r,'especialidades/fractura-patologica/')}">Leer el resumen</a></p></article>
</div>
<p class="nota" style="margin-top:32px">Cada publicación lleva la fecha de su última revisión. Lo que deja de estar vigente se retira.</p>
</div></section>""")

# ---------------------------------------------------------------- Preguntas frecuentes
r = "preguntas-frecuentes/"
FAQ = [
    ("¿La ficha médica inteligente reemplaza a la cita?", "No. Prepara la cita: el doctor llega a ella conociendo su caso y sus estudios, y usted no repite la historia desde cero."),
    ("¿La guía inteligente me da un diagnóstico?", "No. La guía solo hace preguntas y ordena sus respuestas para el doctor. No diagnostica, no receta y no reemplaza la valoración médica. Quien revisa su caso y decide el siguiente paso es el doctor."),
    ("¿Cuánto cuesta la ficha médica inteligente?", precio("precio_consulta", "{}. Se paga en línea al enviar el caso y se descuenta del valor de su consulta.", "El consultorio te informa el valor antes de que usted pague. Ese valor se descuenta de su consulta.")),
    ("¿Cuándo me responden?", "El equipo del doctor te contacta cuando tu caso esté revisado. El tiempo depende del número de casos y de la complejidad del suyo. Si tiene una señal de alarma, no espere la respuesta: acuda a emergencias."),
    ("¿Quién ve mis datos y mis estudios?", "Solo el doctor y su equipo, para valorar su caso, conforme a la Ley Orgánica de Protección de Datos Personales. Los detalles están en el aviso de privacidad."),
    ("¿Qué archivos puedo subir?", "Radiografías, resonancias, tomografías, informes y biopsias, en PDF o imagen (JPG, PNG o HEIC). Si tiene un disco de imágenes en formato DICOM, envíe el enlace de descarga del centro de imagen."),
    ("Vivo fuera de Quito, ¿puedo consultar?", "Sí. Envíe sus estudios por la ficha médica inteligente y el doctor le dirá si conviene una teleconsulta o viajar para una cita presencial."),
    ("¿Atiende por seguro médico?", "[CONFIRMAR CON EL DOCTOR LOS SEGUROS CON LOS QUE TRABAJA]"),
    ("¿Cómo obtengo mi factura?", "Al pagar, el sistema le pide su nombre, cédula o RUC y correo. La factura electrónica la emite el consultorio con esos datos."),
]
pagina(ruta=r, prioridad="0.6", titulo="Preguntas frecuentes",
       descripcion="Respuestas sobre la ficha médica inteligente, la segunda opinión, los costos, la privacidad de sus datos y cómo consultar desde fuera de Quito.",
       jsonld=[{"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ if not a.startswith("[")]},
               migas_ld(r, [("", "Inicio")], "Preguntas frecuentes")],
       cuerpo=cabeza(r, [("", "Inicio")], "", "Preguntas frecuentes") +
       '<section class="seccion"><div class="contenedor estrecho">' + "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in FAQ if not (D.get("publicado") and a.startswith("["))) +
       f'<div class="botones" style="margin-top:32px">{cta(r)}</div></div></section>')

# ---------------------------------------------------------------- Ficha médica inteligente (la aplicación)
r = "consulta-express/"
pagina(ruta=r, prioridad="0.9", titulo="Ficha médica inteligente",
       descripcion="Cuenta tu caso, sube tus estudios y el Dr. Felipe Criollo Palacios lo revisa antes de la cita. Ficha médica inteligente que ordena tu historia; no diagnostica.",
       jsonld=[migas_ld(r, [("", "Inicio")], "Ficha médica inteligente")], scripts=("assets/consulta.js",),
       cuerpo=f"""
<section class="cabeza-pagina"><div class="contenedor">
<nav class="migas" aria-label="Ruta"><a href="{rel(r,'')}">Inicio</a></nav>
<p class="antetitulo">Ficha médica inteligente</p><h1>Cuenta tu caso antes de la cita</h1>
<p class="entrada">La ficha médica inteligente te hace las preguntas de una primera consulta, programadas para orientarte y recoger tu información de manera más eficaz. Respondes con tus palabras y subes tus estudios. El doctor revisa tu caso personalmente.</p>
</div></section>
<section class="seccion" style="padding-top:40px"><div class="contenedor">
<div id="ce" class="ce" aria-live="polite">
<noscript><p>La ficha médica inteligente necesita JavaScript activado en tu navegador.</p></noscript>
</div>
<script type="application/json" id="ce-contacto">{{"telefono": "{D['telefono']}", "tel": "{D['telefono_enlace']}", "whatsapp": "{D['whatsapp_enlace']}", "precio_consulta": "{D['precio_consulta']}", "precio_segunda": "{D['precio_segunda']}"}}</script>
<p class="nota" style="margin-top:24px;max-width:760px">La guía inteligente no diagnostica ni receta. Si describes una señal de alarma, te pedirá acudir a emergencias. Tus datos se tratan conforme al <a href="{rel(r,'privacidad/')}">aviso de privacidad</a>.</p>
</div></section>
<link rel="stylesheet" href="{rel(r,'assets/consulta.css')}">""")

# ---------------------------------------------------------------- Textos legales (borradores para el abogado)
BORRADOR = ('<div class="caja borrador"><p><strong>Borrador para revisión legal.</strong> Este texto lo preparó el equipo del sitio como punto de partida. '
            'Antes de publicar, el abogado del doctor debe revisarlo y aprobarlo. Este aviso desaparece cuando el texto quede aprobado.</p></div>')

r = "privacidad/"
pagina(ruta=r, legal=True, prioridad="0.3", titulo="Aviso de privacidad y tratamiento de datos personales",
       descripcion="Cómo el Dr. Felipe Criollo Palacios trata los datos personales y de salud que recibe a través de este sitio, conforme a la Ley Orgánica de Protección de Datos Personales del Ecuador.",
       cuerpo=cabeza(r, [("", "Inicio")], "", "Aviso de privacidad") + f"""
<section class="seccion"><div class="contenedor"><div class="prosa">
<div class="caja"><p><strong>Hoy este sitio no recoge datos personales.</strong> No tiene formularios activos ni cookies publicitarias o de analítica. La ficha médica inteligente en línea todavía no está en funcionamiento; lo que sigue describe cómo se tratarán los datos cuando se active, y se actualizará antes de esa fecha.</p></div>
<h2>1. Quién es el responsable</h2>
<p>El responsable del tratamiento de tus datos es {D['nombre_completo']}, médico cirujano ortopedista oncólogo, con domicilio en {D['direccion_citimed']}. Para cualquier consulta sobre tus datos puedes presentar {CORREO_O_SITIO}.</p>
<h2>2. Qué datos tratamos</h2>
<ul><li><strong>Datos de identificación y contacto</strong>: nombre, cédula o pasaporte, fecha de nacimiento, correo, teléfono y ciudad.</li><li><strong>Datos de salud</strong>: el motivo de consulta, lo que cuentas en la ficha médica inteligente, los estudios, informes e imágenes que subes y el resumen de tu caso. La Ley Orgánica de Protección de Datos Personales los considera <strong>datos sensibles</strong>.</li><li><strong>Datos de facturación y pago</strong>: nombre o razón social, cédula o RUC, dirección y la constancia del pago. No recibimos ni guardamos el número completo de tu tarjeta: el pago lo procesa directamente la plataforma de pagos.</li><li><strong>Datos técnicos mínimos</strong>: para evitar abusos del formulario, el sistema cuenta las solicitudes por conexión usando un código derivado de la dirección IP, que no permite identificarte y se borra a diario. El sitio no usa cookies publicitarias. [CONFIRMAR SI SE ACTIVA ANALÍTICA Y CUÁL]</li></ul>
<h2>3. Para qué los usamos</h2>
<ul><li>Valorar tu caso, prepararte la cita, la teleconsulta o la segunda opinión, y contactarte con la propuesta de siguiente paso.</li><li>Emitir la factura electrónica del servicio que pagas.</li><li>Si un médico te refirió, y solo si lo autorizas, enviarle a ese médico el informe de tu caso.</li><li>Cumplir obligaciones legales, como las tributarias y las de la historia clínica.</li></ul>
<p>No usamos tus datos de salud para publicidad ni los vendemos. No tomamos decisiones sobre ti de forma automatizada: la guía inteligente es un sistema automatizado que solo ordena la información; la valoración la hace el doctor.</p>
<h2>4. Base legal</h2>
<p>Tratamos tus datos de salud con tu <strong>consentimiento explícito</strong>, que otorgas al marcar la casilla de autorización antes de enviar tu caso, y para la prestación del servicio de salud que solicitas. Los datos de facturación se tratan para cumplir obligaciones legales.</p>
<h2>5. Con quién los compartimos</h2>
<p>Tus datos solo los ven el doctor y el personal de su consultorio que necesita verlos para atenderte, con deber de confidencialidad. Para que el sitio funcione, intervienen proveedores tecnológicos que actúan como encargados del tratamiento, solo bajo instrucciones del doctor: alojamiento del sitio, el servicio automatizado que formula las preguntas de la guía, el formulario donde se guardan los casos y las plataformas de pago. Algunos de estos proveedores están fuera del Ecuador, por lo que tus datos pueden transferirse a otros países con garantías adecuadas de protección.</p>
<p>El proveedor de ese servicio procesa el texto de la conversación para formular la siguiente pregunta y no lo usa para entrenar sus modelos. [CONFIRMAR CONDICIONES CONTRACTUALES VIGENTES]</p>
<h2>6. Cuánto tiempo los conservamos</h2>
<p>Los datos de tu caso se conservan mientras sean necesarios para atenderte. Si tu caso pasa a formar parte de tu historia clínica, se conserva el tiempo que exige la normativa sanitaria. Los datos de facturación se conservan el tiempo que exige la normativa tributaria.</p>
<h2>7. Tus derechos</h2>
<p>Puedes ejercer en cualquier momento tus derechos de acceso, rectificación y actualización, eliminación, oposición, portabilidad, y suspensión del tratamiento, así como revocar tu consentimiento, con {CORREO_O_SITIO}, junto con una copia de tu documento de identidad. Te responderemos en el plazo que fija la ley. Si consideras que tus derechos no fueron atendidos, puedes acudir a la Superintendencia de Protección de Datos Personales.</p>
<h2>8. Seguridad</h2>
<p>Las comunicaciones del sitio viajan cifradas. Los casos se guardan en un espacio de acceso restringido al doctor y su equipo. Te pedimos no enviar por el sitio contraseñas ni datos completos de tarjetas.</p>
<h2>9. Menores de edad</h2>
<p>Si el paciente es menor de edad, la consulta debe enviarla su madre, padre o representante legal, quien otorga el consentimiento.</p>
<h2>10. Cambios</h2>
<p>Si este aviso cambia, publicaremos aquí la nueva versión con su fecha.</p>
</div></div></section>""")

r = "condiciones/"
pagina(ruta=r, legal=True, servicio=True, prioridad="0.3", titulo="Condiciones del servicio",
       descripcion="Condiciones de la ficha médica inteligente y la segunda opinión en línea del Dr. Felipe Criollo Palacios.",
       cuerpo=cabeza(r, [("", "Inicio")], "", "Condiciones del servicio") + f"""
<section class="seccion"><div class="contenedor"><div class="prosa">
{BORRADOR}
<p>Última actualización: [FECHA DE APROBACIÓN]</p>
<h2>1. Quién presta el servicio</h2>
<p>La ficha médica inteligente y la segunda opinión las presta {D['nombre_completo']}, médico cirujano ortopedista oncólogo, con consultorio en {D['direccion_citimed']}.</p>
<h2>2. Qué es la ficha médica inteligente</h2>
<p>Es una ficha previa a tu cita, que se llena en línea. Cuentas tu caso en ella, con la guía de un sistema automatizado que te hace preguntas y ordena tus respuestas, y subes tus estudios. El doctor revisa la información y su equipo te contacta para proponerte el siguiente paso: una cita presencial, una teleconsulta, estudios adicionales o la derivación a otro especialista.</p>
<h2>3. Qué no es</h2>
<ul><li>No es una atención de urgencia ni de emergencia. Ante una señal de alarma, acude a emergencias o llama al 911.</li><li>La guía inteligente no diagnostica, no receta y no da indicaciones de tratamiento. Sus mensajes son preguntas para recoger información.</li><li>La ficha médica inteligente no reemplaza la valoración médica presencial cuando esta es necesaria.</li></ul>
<h2>4. Qué es la segunda opinión</h2>
<p>Es la revisión por el doctor de un diagnóstico o una propuesta de tratamiento previa, con tus estudios. Incluye un informe escrito y una videollamada para explicarlo. La opinión se basa en la información y los estudios enviados; si son incompletos, el doctor puede pedir información adicional o indicar que se requiere una valoración presencial.</p>
<h2>5. Precio y pago</h2>
<ul><li>Ficha médica inteligente: {D['precio_consulta']}.</li><li>Segunda opinión: {D['precio_segunda']}.</li><li>Los precios incluyen IVA cuando corresponde. El pago se hace en línea con las plataformas disponibles en el sitio, que pueden cobrar sus propias comisiones al paciente según sus condiciones.</li><li>El consultorio emite la factura electrónica con los datos que indiques.</li></ul>
<h2>6. Plazos</h2>
<p>El equipo del doctor te contacta cuando el caso está revisado. No se garantiza un plazo de respuesta, que depende del volumen de casos y de la complejidad de cada uno.</p>
<h2>7. Devoluciones</h2>
<p>[POLÍTICA A DEFINIR CON EL DOCTOR Y SU ABOGADO. Por ejemplo: si el doctor determina que el caso no corresponde a su especialidad antes de revisarlo a fondo, se devuelve el valor pagado.]</p>
<h2>8. Responsabilidad del paciente</h2>
<p>Te comprometes a dar información veraz y completa, a enviar estudios que te pertenecen o que estás autorizado a compartir y a no usar el servicio para fines distintos de tu atención.</p>
<h2>9. Datos personales</h2>
<p>El tratamiento de tus datos se rige por el <a href="{rel(r,'privacidad/')}">aviso de privacidad</a>.</p>
<h2>10. Ley aplicable</h2>
<p>Estas condiciones se rigen por las leyes de la República del Ecuador.</p>
</div></div></section>""")

r = "consentimiento/"
pagina(ruta=r, legal=True, servicio=True, prioridad="0.3", titulo="Consentimiento para el tratamiento de datos de salud",
       descripcion="Texto del consentimiento que el paciente otorga en la ficha médica inteligente y la segunda opinión del Dr. Felipe Criollo Palacios.",
       cuerpo=cabeza(r, [("", "Inicio")], "", "Consentimiento para el tratamiento de datos de salud") + f"""
<section class="seccion"><div class="contenedor"><div class="prosa">
{BORRADOR}
<p>Este es el texto completo de la autorización que otorgas al marcar la casilla antes de enviar tu caso.</p>
<div class="caja"><p>Autorizo de forma libre, específica, informada e inequívoca a {D['nombre_completo']} a tratar mis datos personales y los datos de salud que entrego en este formulario, incluidos los estudios, informes e imágenes que adjunto, con la finalidad de valorar mi caso, preparar mi atención y contactarme con la propuesta de siguiente paso, conforme al aviso de privacidad, que declaro haber leído.</p>
<p>Entiendo que la guía inteligente es un sistema automatizado que solo ordena mi información y no emite diagnósticos, y que mis datos serán procesados por proveedores tecnológicos que pueden estar fuera del Ecuador, con garantías adecuadas.</p>
<p>Sé que puedo revocar esta autorización y ejercer mis derechos de acceso, rectificación, eliminación, oposición, portabilidad y suspensión con {CORREO_O_SITIO}.</p></div>
<h2>Si un médico te refiere</h2>
<div class="caja"><p>Autorizo, además, que el informe de mi caso se envíe al médico que me refirió. [CASILLA OPCIONAL]</p></div>
<h2>Si envía el caso un médico o un familiar</h2>
<div class="caja"><p>Declaro que cuento con la autorización del paciente, o que soy su representante legal, para compartir sus datos de salud con el doctor con esta finalidad.</p></div>
</div></div></section>""")

r = "accesibilidad/"
pagina(ruta=r, prioridad="0.2", titulo="Declaración de accesibilidad",
       descripcion="Compromiso de accesibilidad del sitio del Dr. Felipe Criollo Palacios con la norma WCAG 2.2, nivel AA.",
       cuerpo=cabeza(r, [("", "Inicio")], "", "Declaración de accesibilidad") + f"""
<section class="seccion"><div class="contenedor"><div class="prosa">
<p>Queremos que todas las personas puedan usar este sitio, incluidas las que tienen alguna discapacidad visual, auditiva, motriz o cognitiva, y las personas mayores.</p>
<h2>Norma de referencia</h2>
<p>El sitio se construyó siguiendo las Pautas de Accesibilidad para el Contenido Web (WCAG) 2.2, nivel AA, del W3C. Entre otras medidas:</p>
<ul><li>Contraste suficiente entre el texto y el fondo.</li><li>Textos alternativos en las imágenes.</li><li>Un enlace «Saltar al contenido» al inicio de cada página.</li><li>Navegación completa con teclado y foco visible.</li><li>Botones y enlaces de al menos 44 píxeles para tocarlos con facilidad.</li><li>Respeto de la preferencia de movimiento reducido del dispositivo.</li><li>Mapas que solo se cargan si lo pides.</li></ul>
<h2>Limitaciones conocidas</h2>
<p>Los documentos que suben los pacientes y algunos artículos científicos enlazados pertenecen a terceros y pueden no ser accesibles.</p>
<h2>Cómo avisarnos</h2>
<p>Si encuentras una barrera, cuéntanoslo en el consultorio del doctor. Te ayudaremos por otro medio y corregiremos el problema.</p>
<p>Fecha de esta declaración: [FECHA DE PUBLICACIÓN]</p>
</div></div></section>""")

# ---------------------------------------------------------------- 404
r = ""
pagina(ruta="", archivo="404.html", sin_indice=True, titulo="Página no encontrada", descripcion="La página que buscas no existe.",
       cuerpo=f"""<section class="seccion"><div class="contenedor estrecho"><h1>No encontramos esta página</h1>
<p class="entrada">Puede que la dirección haya cambiado. Estas son las páginas más consultadas:</p>
<ul style="margin-top:20px;line-height:2"><li><a href="/">Inicio</a></li><li><a href="/consulta-express/">Ficha médica inteligente</a></li><li><a href="/segunda-opinion/">Segunda opinión</a></li><li><a href="/#oncologia">Especialidades</a></li><li><a href="/donde-atiendo/">Consultorio</a></li></ul></div></section>""")
