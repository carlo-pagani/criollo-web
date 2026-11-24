// Consulta express del Dr. Felipe Criollo Palacios.
// Recorrido: quién escribe y motivo → filtro de señales de alarma → relato → entrevista con el asistente (IA en el Worker;
// si no responde, preguntas fijas) → resumen que el paciente confirma → estudios → datos y consentimiento → pago y envío.
// Nada sale del navegador hasta que el paciente autoriza el tratamiento de sus datos, salvo el texto de la entrevista,
// que va al asistente sin nombre ni identificación (se avisa antes de empezar).
(function () {
  'use strict';
  var raiz = document.getElementById('ce');
  if (!raiz) return;
  var BASE = document.currentScript ? document.currentScript.src.replace(/assets\/consulta\.js.*$/, '') : '../';

  // ---------- Configuración (data/servicios.json) ----------
  // guia: dirección del asistente; api: base del Worker (precios y pagos); envio: formulario donde se guardan los casos.
  var CFG = { guia: '', api: '', envio: { url: '', campos: {} }, maxMB: 15, maxArchivos: 12 };

  var MOTIVOS = [
    { id: 'tumor', t: 'Masa, bulto o tumor', d: 'Un bulto, un dolor en el hueso o un hallazgo en un estudio' },
    { id: 'segunda', t: 'Segunda opinión', d: 'Ya tiene un diagnóstico o una propuesta de tratamiento y quiere revisarla' },
    { id: 'lesion', t: 'Lesión o fractura', d: 'Un golpe, una caída o un accidente' },
    { id: 'dolor', t: 'Dolor articular o lesión deportiva', d: 'Rodilla, hombro, cadera, mano u otra articulación' },
    { id: 'control', t: 'Control después de una cirugía', d: 'Seguimiento de una operación' },
    { id: 'colega', t: 'Soy médico y refiero a un paciente', d: 'Envío el caso de un paciente con sus estudios' }
  ];
  // Preguntas fijas: se usan cuando el asistente con IA no está disponible. VALIDACIÓN CLÍNICA PENDIENTE con el doctor.
  var COMUNES = ['¿Qué edad tiene el paciente y en qué ciudad vive?', '¿Tiene otras enfermedades, cirugías previas o alergias? ¿Qué medicamentos toma?', '¿Qué espera de esta consulta?'];
  var FIJAS = {
    tumor: ['¿En qué parte del cuerpo está y desde cuándo lo nota?', '¿Ha crecido? ¿Le duele de noche o en reposo?', '¿Ha tenido pérdida de peso, fiebre o algún antecedente de cáncer, personal o en la familia?', '¿Qué estudios le han hecho (radiografía, resonancia, tomografía, biopsia) y cuándo? Podrá subirlos en el siguiente paso.'],
    segunda: ['¿Qué diagnóstico le dieron, quién y cuándo?', '¿Qué tratamiento le propusieron y para cuándo?', '¿Le hicieron una biopsia? ¿Dónde y qué resultado dio?', '¿Qué estudios de imagen tiene y de qué fechas? Podrá subirlos en el siguiente paso.', '¿Qué duda concreta quiere resolver con la segunda opinión?'],
    lesion: ['¿Qué pasó, cómo y cuándo?', '¿Puede mover o apoyar la zona? ¿Hay hinchazón o moretón?', '¿Ya lo atendieron? ¿Qué le hicieron y qué le indicaron?', '¿Tiene radiografías u otros estudios? Podrá subirlos en el siguiente paso.'],
    dolor: ['¿Dónde le duele y desde cuándo?', '¿Qué lo empeora y qué lo alivia? ¿Le duele de noche?', '¿Practica algún deporte o hace trabajo físico?', '¿Qué tratamientos ha probado y con qué resultado?'],
    control: ['¿Qué cirugía le hicieron, cuándo y dónde?', '¿Cómo está la herida? ¿Ha tenido fiebre?', '¿Cómo van el dolor y la movilidad?', '¿Qué le preocupa o qué quiere revisar?'],
    colega: ['¿Cuál es su especialidad y en qué ciudad atiende?', 'Edad y sexo del paciente, localización y tiempo de evolución.', 'Hallazgos de imagen y, si existe, resultado o plan de biopsia.', '¿Cuál es su pregunta concreta y cómo prefiere recibir la respuesta?']
  };
  var ALARMAS = [
    'Una deformidad visible después de un golpe, o el hueso asoma por la piel',
    'Perdió la sensibilidad o la fuerza de un brazo o una pierna',
    'La extremidad está fría, pálida o morada',
    'Fiebre con una herida de cirugía enrojecida o que supura',
    'Dolor de espalda con debilidad en las piernas o dificultad para orinar',
    'Una pierna hinchada, caliente y dolorosa después de una cirugía, o falta de aire'
  ];
  var TEXTO_ALARMA = 'Por lo que describe, no espere la respuesta de esta consulta: acuda hoy a un servicio de emergencias o llame al 911.';
  var PASOS = ['Motivo', 'Su caso', 'Estudios', 'Sus datos', 'Enviar'];

  // ---------- Estado ----------
  var E = nuevo();
  var archivos = []; // los archivos no se pueden guardar en el navegador: si se recarga la página, se vuelven a elegir
  function nuevo() {
    return { pantalla: 'inicio', quien: 'paciente', motivo: '', relato: '', conv: [], pregunta: '', fija: 0, resumen: '', prioridad: '', alarma: false, sinIA: false, datos: {}, ref: 'CE-' + Math.random().toString(36).slice(2, 8).toUpperCase() };
  }
  function guardar() { try { sessionStorage.setItem('ce', JSON.stringify(E)); } catch (e) { /* sin almacenamiento: se sigue igual */ } }
  function recuperar() { try { var g = JSON.parse(sessionStorage.getItem('ce') || 'null'); if (g && g.pantalla && g.pantalla !== 'enviado') E = g; } catch (e) { /* nada */ } }
  function borrar() { try { sessionStorage.removeItem('ce'); } catch (e) { /* nada */ } }

  // ---------- Utilidades de pantalla ----------
  function el(tag, attrs, hijos) {
    var e = document.createElement(tag);
    Object.keys(attrs || {}).forEach(function (k) {
      if (k === 'texto') e.textContent = attrs[k];
      else if (k === 'on') Object.keys(attrs.on).forEach(function (ev) { e.addEventListener(ev, attrs.on[ev]); });
      else if (attrs[k] === true) e.setAttribute(k, '');
      else if (attrs[k] !== false && attrs[k] != null) e.setAttribute(k, attrs[k]);
    });
    (hijos || []).forEach(function (h) { if (h) e.appendChild(typeof h === 'string' ? document.createTextNode(h) : h); });
    return e;
  }
  function boton(texto, fn, clase) { return el('button', { type: 'button', class: clase || 'btn', texto: texto, on: { click: fn } }); }
  function ir(p) { E.pantalla = p; guardar(); pintar(); }
  function campo(id, etiqueta, tipo, extra) {
    var a = Object.assign({ id: 'ce-' + id, name: id, type: tipo || 'text', value: E.datos[id] || '' }, extra || {});
    var input = el('input', a);
    input.addEventListener('input', function () { E.datos[id] = input.value; guardar(); });
    return el('label', { class: 'ce-campo', for: 'ce-' + id }, [el('span', { texto: etiqueta }), input]);
  }
  function progreso(n) {
    return el('ol', { class: 'ce-pasos', 'aria-label': 'Progreso' }, PASOS.map(function (p, i) {
      return el('li', { class: i < n ? 'hecho' : i === n ? 'actual' : '', 'aria-current': i === n ? 'step' : null, texto: p });
    }));
  }
  function marco(n, hijos) {
    raiz.innerHTML = '';
    raiz.appendChild(progreso(n));
    var caja = el('div', { class: 'ce-caja' }, hijos);
    raiz.appendChild(caja);
    var h = caja.querySelector('h2');
    if (h) { h.setAttribute('tabindex', '-1'); h.focus({ preventScroll: true }); }
    if (raiz.getBoundingClientRect().top < 0) raiz.scrollIntoView({ block: 'start' });
  }
  function cajaAlarma() {
    return el('div', { class: 'alarma-caja', role: 'alert' }, [el('p', {}, [el('strong', { texto: 'Esto puede ser una urgencia. ' }), TEXTO_ALARMA])]);
  }

  // ---------- Pantallas ----------
  var P = {};

  P.inicio = function () {
    var quien = el('fieldset', { class: 'ce-opciones fila' }, [el('legend', { texto: '¿Quién escribe?' })].concat(
      [['paciente', 'Soy el paciente'], ['familiar', 'Soy un familiar o acompañante'], ['medico', 'Soy médico']].map(function (o) {
        var r = el('input', { type: 'radio', name: 'quien', value: o[0], checked: E.quien === o[0] });
        r.addEventListener('change', function () { E.quien = o[0]; guardar(); });
        return el('label', {}, [r, el('span', { texto: o[1] })]);
      })));
    var lista = el('div', { class: 'ce-motivos' }, MOTIVOS.map(function (m) {
      return el('button', { type: 'button', class: 'ce-motivo' + (E.motivo === m.id ? ' elegido' : ''), on: { click: function () {
        E.motivo = m.id; if (m.id === 'colega') E.quien = 'medico';
        ir(m.id === 'colega' ? 'relato' : 'alarma');
      } } }, [el('strong', { texto: m.t }), el('span', { texto: m.d })]);
    }));
    marco(0, [el('h2', { texto: '¿Por qué motivo quiere consultar?' }),
      el('p', { class: 'ce-sub', texto: 'Las preguntas están programadas para orientarle y recoger su información de manera más eficaz. La valoración la hace el doctor.' }), quien, lista]);
  };

  P.alarma = function () {
    marco(0, [el('h2', { texto: 'Antes de empezar: ¿tiene ahora alguna de estas señales?' }),
      el('ul', { class: 'ce-lista' }, ALARMAS.map(function (a) { return el('li', { texto: a }); })),
      el('div', { class: 'botones' }, [
        boton('No, ninguna', function () { E.alarma = false; ir('relato'); }),
        boton('Sí, al menos una', function () { E.alarma = true; ir('urgencia'); }, 'btn btn-linea')
      ]),
      boton('Volver', function () { ir('inicio'); }, 'ce-link')]);
  };

  P.urgencia = function () {
    marco(0, [el('h2', { texto: 'Acuda a emergencias' }), cajaAlarma(),
      el('p', { class: 'ce-sub', texto: 'La consulta express no es un servicio de urgencias y la respuesta no es inmediata. Cuando ya le hayan atendido, puede volver y enviar su caso para el seguimiento con el doctor.' }),
      el('div', { class: 'botones' }, [el('a', { class: 'btn', href: 'tel:911', texto: 'Llamar al 911' }),
        boton('Ya me atendieron; quiero enviar mi caso', function () { ir('relato'); }, 'btn btn-neutro')])]);
  };

  P.relato = function () {
    var medico = E.motivo === 'colega';
    var ta = el('textarea', { id: 'ce-relato', rows: 7, maxlength: 2500, placeholder: medico ? 'Resumen clínico del paciente…' : 'Por ejemplo: hace dos meses noté un bulto en el muslo derecho que ha ido creciendo…' });
    ta.value = E.relato;
    ta.addEventListener('input', function () { E.relato = ta.value; guardar(); });
    var aviso = el('p', { class: 'ce-error', role: 'alert' });
    marco(1, [el('h2', { texto: medico ? 'Cuénteme el caso de su paciente' : 'Cuénteme su caso con sus palabras' }),
      el('label', { class: 'ce-sub', for: 'ce-relato', texto: medico ? 'Sin el nombre ni la identificación del paciente: esos datos se piden después.' : 'Qué notó, en qué parte del cuerpo y desde cuándo. No hace falta que sea ordenado: después le haré algunas preguntas.' }),
      ta,
      el('p', { class: 'ce-nota', texto: 'Para formular las preguntas, lo que escriba aquí lo procesa un sistema automatizado. No escriba todavía su nombre, su cédula ni su teléfono: se los pediremos al final, junto con su autorización.' }),
      aviso,
      el('div', { class: 'botones' }, [boton('Continuar', function () {
        if (E.relato.trim().length < 15) { aviso.textContent = 'Escriba al menos una o dos frases para poder continuar.'; ta.focus(); return; }
        E.conv = []; E.fija = 0; E.resumen = ''; E.pregunta = ''; ir('entrevista');
      }), boton('Volver', function () { ir('inicio'); }, 'btn btn-neutro')])]);
  };

  function fijas() { return (FIJAS[E.motivo] || FIJAS.dolor).concat(E.motivo === 'colega' ? [] : COMUNES); }
  function resumenFijo() {
    return 'Así entendí su caso.\nMotivo: ' + (MOTIVOS.filter(function (m) { return m.id === E.motivo; })[0] || {}).t + '\nRelato: ' + E.relato.trim() + '\n' +
      E.conv.map(function (c) { return '· ' + c.pregunta + '\n  ' + c.respuesta; }).join('\n') + '\n¿Es correcto, o desea corregir o añadir algo?';
  }
  // Pide al asistente la siguiente pregunta. Si no hay asistente o falla, sigue con las preguntas fijas.
  function siguiente() {
    function local() {
      E.sinIA = true;
      var f = fijas();
      if (E.resumen === '' && E.fija < f.length) { E.pregunta = f[E.fija++]; } else { E.resumen = resumenFijo(); E.pregunta = ''; }
      guardar(); pintar();
    }
    if (!CFG.guia || E.sinIA) return local();
    E.pensando = true; pintar();
    var ctl = new AbortController(), t = setTimeout(function () { ctl.abort(); }, 25000);
    fetch(CFG.guia, { method: 'POST', headers: { 'Content-Type': 'application/json' }, signal: ctl.signal,
      body: JSON.stringify({ motivo: E.motivo, quien: E.quien, relato: E.relato, conversacion: E.conv }) })
      .then(function (r) { return r.ok ? r.json() : null; })
      .catch(function () { return null; })
      .then(function (o) {
        clearTimeout(t); E.pensando = false;
        if (!o || !o.mensaje || o.accion === 'seguir') return local();
        if (o.accion === 'alarma') { E.alarma = true; E.pregunta = o.mensaje; E.alarmaIA = true; }
        else if (o.accion === 'resumir') { E.resumen = o.mensaje; E.prioridad = o.prioridad || ''; E.pregunta = ''; }
        else { E.pregunta = o.mensaje; E.resumen = ''; }
        guardar(); pintar();
      });
  }

  P.entrevista = function () {
    if (!E.pregunta && !E.resumen && !E.pensando) return siguiente();
    var hilo = el('div', { class: 'ce-hilo', role: 'log', 'aria-label': 'Conversación' });
    function burbuja(texto, mia) { hilo.appendChild(el('div', { class: 'ce-bur ' + (mia ? 'pac' : 'ia') }, [mia ? null : el('b', { texto: 'Guía' }), texto])); }
    burbuja(E.relato, true);
    E.conv.forEach(function (c) { burbuja(c.pregunta, false); burbuja(c.respuesta, true); });
    var pie = el('div', { class: 'ce-pie' });
    if (E.pensando) {
      hilo.appendChild(el('div', { class: 'ce-bur ia pensando', texto: 'Un momento…' }));
    } else if (E.alarmaIA) {
      hilo.appendChild(cajaAlarma());
      pie.appendChild(el('div', { class: 'botones' }, [el('a', { class: 'btn', href: 'tel:911', texto: 'Llamar al 911' }),
        boton('Ya me atendieron; quiero continuar', function () { E.alarmaIA = false; E.conv.push({ pregunta: E.pregunta, respuesta: 'Ya recibí atención de emergencia y deseo continuar con la consulta.' }); E.pregunta = ''; guardar(); pintar(); }, 'btn btn-neutro')]));
    } else if (E.resumen) {
      burbuja(E.resumen, false);
      var corr = el('textarea', { rows: 3, maxlength: 1500, 'aria-label': 'Corrección o dato adicional', placeholder: 'Si falta algo o hay un error, escríbalo aquí…' });
      pie.appendChild(corr);
      pie.appendChild(el('div', { class: 'botones' }, [boton('Es correcto, continuar', function () { ir('estudios'); }),
        boton('Enviar corrección', function () {
          var v = corr.value.trim(); if (!v) { corr.focus(); return; }
          E.conv.push({ pregunta: E.resumen, respuesta: v }); E.resumen = ''; E.pregunta = '';
          if (E.sinIA) { E.resumen = resumenFijo(); }
          guardar(); pintar();
        }, 'btn btn-neutro')]));
    } else {
      burbuja(E.pregunta, false);
      var ta = el('textarea', { rows: 3, maxlength: 1500, 'aria-label': 'Su respuesta', placeholder: 'Escriba su respuesta…' });
      var enviar = function () {
        var v = ta.value.trim(); if (!v) { ta.focus(); return; }
        E.conv.push({ pregunta: E.pregunta, respuesta: v }); E.pregunta = ''; guardar(); pintar();
      };
      ta.addEventListener('keydown', function (e) { if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) enviar(); });
      pie.appendChild(ta);
      pie.appendChild(el('div', { class: 'botones' }, [boton('Responder', enviar),
        boton('No lo sé', function () { ta.value = 'No lo sé.'; enviar(); }, 'btn btn-neutro'),
        E.conv.length >= 3 ? boton('Ya conté todo', function () { ta.value = 'Eso es todo lo que puedo contar.'; enviar(); }, 'ce-link') : null]));
      setTimeout(function () { ta.focus({ preventScroll: true }); }, 0);
    }
    marco(1, [el('h2', { texto: 'Algunas preguntas sobre su caso' }), hilo, pie,
      el('p', { class: 'ce-nota', texto: 'La guía no diagnostica ni receta. Solo ordena su información para el doctor.' })]);
    hilo.scrollTop = hilo.scrollHeight;
  };

  function peso(b) { return b >= 1e6 ? (b / 1e6).toFixed(1) + ' MB' : Math.max(1, Math.round(b / 1e3)) + ' KB'; }
  P.estudios = function () {
    var aviso = el('p', { class: 'ce-error', role: 'alert' });
    var lista = el('ul', { class: 'ce-archivos' }, archivos.map(function (f, i) {
      return el('li', {}, [el('span', { texto: f.name }), el('span', { class: 'ce-peso', texto: peso(f.size) }),
        el('button', { type: 'button', class: 'ce-link', 'aria-label': 'Quitar ' + f.name, texto: 'Quitar', on: { click: function () { archivos.splice(i, 1); pintar(); } } })]);
    }));
    var input = el('input', { type: 'file', multiple: true, hidden: true, accept: '.pdf,.jpg,.jpeg,.png,.heic,.webp,.zip,application/pdf,image/*' });
    input.addEventListener('change', function () {
      var malos = [];
      Array.prototype.forEach.call(input.files, function (f) {
        if (archivos.length >= CFG.maxArchivos) return malos.push(f.name + ' (máximo ' + CFG.maxArchivos + ' archivos)');
        if (!f.size) return malos.push(f.name + ' (está vacío)');
        if (f.size > CFG.maxMB * 1e6) return malos.push(f.name + ' (pesa más de ' + CFG.maxMB + ' MB)');
        if (archivos.some(function (a) { return a.name === f.name && a.size === f.size; })) return;
        archivos.push(f);
      });
      pintar();
      if (malos.length) document.querySelector('.ce-error').textContent = 'No se añadieron: ' + malos.join('; ') + '.';
    });
    marco(2, [el('h2', { texto: 'Suba sus estudios' }),
      el('p', { class: 'ce-sub', texto: 'Radiografías, resonancias, tomografías, informes de radiología y de patología, en PDF o imagen. Hasta ' + CFG.maxMB + ' MB por archivo. Si tiene un disco de imágenes (DICOM), pegue el enlace de descarga del centro de imagen en el siguiente paso.' }),
      lista, el('label', { class: 'ce-agregar' }, ['+ Agregar archivos', input]), aviso,
      el('p', { class: 'ce-nota', texto: 'Sus archivos no salen de su dispositivo hasta que usted autorice y envíe el caso.' }),
      el('div', { class: 'botones' }, [boton(archivos.length ? 'Continuar' : 'Continuar sin estudios', function () { ir('datos'); }), boton('Volver', function () { ir('entrevista'); }, 'btn btn-neutro')])]);
  };

  P.datos = function () {
    var medico = E.quien === 'medico', familiar = E.quien === 'familiar';
    var aviso = el('p', { class: 'ce-error', role: 'alert' });
    function casilla(id, nodos, req) {
      var c = el('input', { type: 'checkbox', id: 'ce-' + id, checked: !!E.datos[id], required: !!req });
      c.addEventListener('change', function () { E.datos[id] = c.checked; guardar(); });
      return el('label', { class: 'ce-casilla', for: 'ce-' + id }, [c, el('span', {}, nodos)]);
    }
    var enlace = function (ruta, texto) { return el('a', { href: BASE + ruta, target: '_blank', rel: 'noopener', texto: texto }); };
    var form = el('form', { novalidate: true, class: 'ce-form' }, [
      medico ? el('p', { class: 'ce-grupo', texto: 'Sus datos' }) : null,
      medico ? campo('medico', 'Su nombre y especialidad', 'text', { required: true, autocomplete: 'name' }) : null,
      medico ? campo('medico_contacto', 'Su correo o celular para la respuesta', 'text', { required: true }) : null,
      el('p', { class: 'ce-grupo', texto: 'Datos del paciente' }),
      campo('nombre', 'Nombres y apellidos del paciente', 'text', { required: true, autocomplete: medico || familiar ? 'off' : 'name' }),
      campo('documento', 'Cédula o pasaporte', 'text', { required: !medico, inputmode: 'text', autocomplete: 'off' }),
      campo('nacimiento', 'Fecha de nacimiento', 'date', { required: !medico, autocomplete: medico || familiar ? 'off' : 'bday' }),
      campo('ciudad', 'Ciudad y país donde vive', 'text', { required: true }),
      familiar ? campo('contacto_nombre', 'Su nombre y su relación con el paciente', 'text', { required: true, autocomplete: 'name' }) : null,
      medico ? null : campo('correo', 'Correo electrónico', 'email', { required: true, autocomplete: 'email' }),
      medico ? null : campo('celular', 'Celular o WhatsApp, con código de país', 'tel', { required: true, autocomplete: 'tel' }),
      campo('enlace', 'Enlace a imágenes DICOM (opcional)', 'url', { placeholder: 'https://…' }),
      medico ? null : el('p', { class: 'ce-grupo', texto: 'Datos para la factura' }),
      medico ? null : campo('factura', 'Nombre o razón social, cédula o RUC y dirección', 'text', { placeholder: 'Si son los mismos del paciente, deje este campo vacío' }),
      el('p', { class: 'ce-grupo', texto: 'Autorización' }),
      casilla('consentimiento', medico
        ? ['Declaro que cuento con la autorización del paciente para compartir sus datos de salud con el Dr. Felipe Criollo Palacios con el fin de valorar su caso, conforme al ', enlace('privacidad/', 'aviso de privacidad'), '.']
        : [(familiar ? 'Declaro que soy el representante legal del paciente o cuento con su autorización, y autorizo' : 'Autorizo') + ' al Dr. Felipe Criollo Palacios a tratar los datos personales y de salud de este formulario, incluidos los estudios adjuntos, para valorar el caso y contactarme, conforme al ',
          enlace('privacidad/', 'aviso de privacidad'), ' y al ', enlace('consentimiento/', 'texto completo del consentimiento'), '.'], true),
      casilla('condiciones', ['Leí y acepto las ', enlace('condiciones/', 'condiciones del servicio'), '. Entiendo que la consulta express no es un servicio de urgencias y que la guía inteligente no diagnostica.'], true),
      medico ? null : casilla('informar_medico', ['Si un médico me refirió, autorizo que el doctor le envíe el informe de mi caso. (Opcional)']),
      aviso,
      el('div', { class: 'botones' }, [el('button', { type: 'submit', class: 'btn', texto: 'Revisar y enviar' }), boton('Volver', function () { ir('estudios'); }, 'btn btn-neutro')])
    ]);
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var malo = form.querySelector(':invalid');
      if (malo) { aviso.textContent = malo.type === 'checkbox' ? 'Para enviar su caso necesitamos las dos autorizaciones.' : 'Revise el campo «' + (malo.closest('label').querySelector('span').textContent) + '».'; malo.focus(); return; }
      ir('enviar');
    });
    marco(3, [el('h2', { texto: medico ? 'Datos para responderle' : 'Sus datos' }),
      el('p', { class: 'ce-sub', texto: 'Los usamos solo para identificar el caso, contactarle y emitir la factura.' }), form]);
  };

  function textoCaso() {
    var m = (MOTIVOS.filter(function (x) { return x.id === E.motivo; })[0] || {}).t;
    return ['Referencia: ' + E.ref, 'Motivo: ' + m, 'Escribe: ' + E.quien,
      'Prioridad orientativa de la guía (la confirma el doctor): ' + (E.prioridad || 'sin asignar'),
      E.alarma ? 'ATENCIÓN: el paciente marcó o describió una señal de alarma; se le indicó acudir a emergencias.' : '',
      '', 'RESUMEN CONFIRMADO POR EL PACIENTE', E.resumen, '', 'RELATO INICIAL', E.relato, '', 'CONVERSACIÓN',
      E.conv.map(function (c) { return 'P: ' + c.pregunta + '\nR: ' + c.respuesta; }).join('\n\n'),
      '', 'Guía automática: ' + (E.sinIA ? 'no disponible; se usaron las preguntas fijas' : 'sí')].filter(function (x) { return x !== ''; }).join('\n');
  }

  P.enviar = function () {
    var d = E.datos, demo = !CFG.envio.url;
    var aviso = el('p', { class: 'ce-error', role: 'alert' });
    var filas = [['Motivo', (MOTIVOS.filter(function (x) { return x.id === E.motivo; })[0] || {}).t], ['Paciente', d.nombre], ['Contacto', [d.correo, d.celular, d.medico_contacto].filter(Boolean).join(' · ')],
      ['Estudios adjuntos', archivos.length ? archivos.map(function (f) { return f.name; }).join(', ') : 'Ninguno']];
    var b = boton(demo ? 'Ver lo que recibiría el doctor' : 'Enviar mi caso', function () {
      if (demo) return ir('demo');
      b.disabled = true; b.textContent = 'Enviando…';
      enviarCaso().then(function () { borrar(); E.pantalla = 'enviado'; pintar(); })
        .catch(function () { b.disabled = false; b.textContent = 'Enviar mi caso'; aviso.textContent = 'No pudimos enviar su caso. Revise su conexión e inténtelo de nuevo; sus respuestas siguen aquí.'; });
    });
    marco(4, [el('h2', { texto: 'Revise y envíe' }),
      el('dl', { class: 'ce-resumen' }, filas.reduce(function (a, f) { return a.concat([el('dt', { texto: f[0] }), el('dd', { texto: f[1] || '—' })]); }, [])),
      el('div', { class: 'ce-bur ia', style: 'max-width:100%' }, [el('b', { texto: 'Resumen de su caso' }), E.resumen]),
      el('p', { class: 'ce-nota', texto: 'Este resumen no es un diagnóstico. El doctor revisa su caso y su equipo le contacta para proponerle el siguiente paso.' }),
      demo ? el('p', { class: 'ce-demo', texto: 'Versión de prueba: todavía no se envía ni se cobra nada.' }) : null,
      aviso, el('div', { class: 'botones' }, [b, boton('Volver', function () { ir('datos'); }, 'btn btn-neutro')])]);
  };

  // Envío al formulario donde el consultorio recibe los casos (CFG.envio). Los nombres de los campos vienen de la configuración.
  function enviarCaso() {
    var c = CFG.envio.campos || {}, d = E.datos, fd = new FormData();
    var valores = { referencia: E.ref, motivo: E.motivo, prioridad: E.prioridad, caso: textoCaso(), nombre: d.nombre, documento: d.documento, nacimiento: d.nacimiento, ciudad: d.ciudad,
      correo: d.correo, celular: d.celular, contacto: [d.contacto_nombre, d.medico, d.medico_contacto].filter(Boolean).join(' · '), enlace: d.enlace, factura: d.factura,
      consentimiento: 'Otorgado el ' + new Date().toISOString() + (d.informar_medico ? ' · autoriza informar al médico que refiere' : '') };
    Object.keys(valores).forEach(function (k) { if (c[k] && valores[k]) fd.append(c[k], valores[k]); });
    if (c.archivos) archivos.forEach(function (f) { fd.append(c.archivos, f, f.name); });
    return fetch(CFG.envio.url, { method: 'POST', body: fd, mode: CFG.envio.opaco ? 'no-cors' : 'cors' }).then(function (r) { if (!CFG.envio.opaco && !r.ok) throw new Error('envío'); });
  }

  P.demo = function () {
    var d = E.datos;
    marco(4, [el('h2', { texto: 'Esto recibiría el doctor' }),
      el('p', { class: 'ce-demo', texto: 'Versión de prueba: no se envió ni se cobró nada.' }),
      el('pre', { class: 'ce-ficha', texto: textoCaso() + '\n\nDATOS\n' + Object.keys(d).map(function (k) { return k + ': ' + d[k]; }).join('\n') +
        '\n\nARCHIVOS\n' + (archivos.length ? archivos.map(function (f) { return f.name + ' (' + peso(f.size) + ')'; }).join('\n') : 'Ninguno') }),
      el('div', { class: 'botones' }, [boton('Empezar de nuevo', function () { borrar(); E = nuevo(); archivos = []; pintar(); }), boton('Volver', function () { ir('enviar'); }, 'btn btn-neutro')])]);
  };

  P.enviado = function () {
    marco(5, [el('h2', { texto: 'Su caso llegó al doctor' }),
      el('p', { class: 'ce-sub', texto: 'El equipo del doctor revisará su caso y le escribirá para proponerle el siguiente paso: cita presencial, teleconsulta o derivación. Su referencia es ' + E.ref + '.' }),
      el('p', { class: 'ce-nota', texto: 'Si aparece una señal de alarma mientras espera, no aguarde la respuesta: acuda a emergencias.' }),
      el('div', { class: 'botones' }, [el('a', { class: 'btn btn-neutro', href: BASE, texto: 'Volver al inicio' })])]);
  };

  function pronto() {
    var c = {}; try { c = JSON.parse(document.getElementById('ce-contacto').textContent); } catch (e) { /* sin datos de contacto */ }
    raiz.innerHTML = '';
    raiz.appendChild(el('div', { class: 'ce-caja' }, [
      el('p', { class: 'rotulo', style: 'color:var(--acento)', texto: 'Muy pronto' }),
      el('h2', { texto: 'La consulta express en línea se activa en los próximos días' }),
      el('p', { class: 'ce-sub', texto: 'Estamos terminando de prepararla para que pueda contar su caso y enviar sus estudios desde aquí. Vuelva a visitarnos en unos días.' }),
      el('div', { class: 'botones' }, [
        c.whatsapp ? el('a', { class: 'btn', href: c.whatsapp, rel: 'noopener', texto: 'Escribir por WhatsApp' }) : null,
        c.tel ? el('a', { class: 'btn btn-neutro', href: 'tel:' + c.tel, texto: 'Llamar al ' + c.telefono }) : null]),
      el('p', { class: 'ce-nota', texto: 'Si tiene una señal de alarma (deformidad tras un golpe, pérdida de fuerza o de sensibilidad, fiebre con una herida que supura), no espere: acuda a emergencias o llame al 911.' })
    ]));
  }

  function pintar() { (P[E.pantalla] || P.inicio)(); }

  // ---------- Arranque ----------
  recuperar();
  var m = new URLSearchParams(location.search).get('motivo');
  if (m && E.pantalla === 'inicio' && MOTIVOS.some(function (x) { return x.id === m; })) E.motivo = m;
  fetch(BASE + 'data/servicios.json').then(function (r) { return r.ok ? r.json() : {}; }).catch(function () { return {}; }).then(function (c) {
    ['guia', 'api', 'maxMB', 'maxArchivos'].forEach(function (k) { if (c[k]) CFG[k] = c[k]; });
    if (c.envio && c.envio.url) CFG.envio = c.envio;
    if (E.pantalla === 'estudios' || E.pantalla === 'datos' || E.pantalla === 'enviar' || E.pantalla === 'demo') { /* los archivos no sobreviven a una recarga */ if (E.pantalla !== 'datos') E.pantalla = 'estudios'; }
    E.pensando = false;
    // Mientras el consultorio no tenga activo el canal donde recibe los casos, la consulta no se ofrece al público:
    // se muestra un aviso con el contacto directo. Con ?prueba=1 se puede recorrer completa (no envía ni cobra).
    if (!CFG.envio.url && new URLSearchParams(location.search).get('prueba') !== '1') return pronto();
    pintar();
  });
})();
