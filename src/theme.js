/*
 * Tema Sostenido para Redmine 7 — theme.js
 * Copyright (C) 2026 Martín Roberto Tolava — SOSTENIDO
 * Licencia: GPL v2 o posterior (ver LICENSE). El logo no está cubierto
 * por la GPL (ver NOTICE.md).
 *
 * Redmine carga este archivo en el <head>. Hace tres cosas:
 *   1. Aplica paleta y modo (claro/oscuro/auto) antes de pintar,
 *      para que no haya parpadeo.
 *   2. Inserta la marca (logo, y lema si la variante lo define) en la cabecera y, si la
 *      variante lo pide, el crédito "Realizado y mantenido por" en el pie.
 *   3. Agrega "Apariencia" al menú desplegable del usuario: modo
 *      (claro / oscuro / automático) y, si la variante lo permite, paleta.
 *
 * La configuración la define la variante (variants/<nombre>.js) en
 * window.SOSTENIDO_TEMA, concatenada antes de este archivo por build.sh.
 */
(function () {
  'use strict';

  var C = window.SOSTENIDO_TEMA || {};
  var PALETAS = { sostenido: 'Sostenido', grafito: 'Grafito', papel: 'Papel' };
  // Paleta de marca de la organización (PALETA_MARCA= en el .conf): va primera
  if (C.paletaMarca) {
    PALETAS = { marca: C.paletaMarca, sostenido: 'Sostenido', grafito: 'Grafito', papel: 'Papel' };
  }
  var MODOS = ['auto', 'claro', 'oscuro'];
  var html = document.documentElement;
  var LOGO = (typeof SOSTENIDO_LOGO === 'string') ? SOSTENIDO_LOGO : null;

  /* localStorage puede no estar disponible (modo privado, políticas):
     el tema funciona igual, solo no recuerda la elección */
  function leer(clave) {
    try { return window.localStorage.getItem('sostenido.' + clave); } catch (e) { return null; }
  }
  function guardar(clave, valor) {
    try { window.localStorage.setItem('sostenido.' + clave, valor); } catch (e) { /* sin memoria */ }
  }

  /* ---------- 1. Paleta y modo, antes de pintar ---------- */
  var paleta = PALETAS[C.paleta] ? C.paleta : 'sostenido';
  if (C.elegirPaleta && PALETAS[leer('paleta')]) { paleta = leer('paleta'); }

  var modo = leer('modo');
  if (MODOS.indexOf(modo) < 0) { modo = MODOS.indexOf(C.modo) >= 0 ? C.modo : 'auto'; }

  html.setAttribute('data-paleta', paleta);
  html.setAttribute('data-modo', modo);

  /* ---------- Íconos de los modos ---------- */
  var ICONO = {
    claro: '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>',
    oscuro: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5z"/></svg>',
    auto: '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="8"/><path d="M12 4a8 8 0 0 1 0 16z" class="s-relleno"/></svg>'
  };
  var ETIQUETA_MODO = { claro: 'Claro', oscuro: 'Oscuro', auto: 'Automático' };

  /* ---------- 2. Marca y crédito ---------- */
  function insertarMarca() {
    var header = document.getElementById('header');
    if (!header || header.querySelector('.s-marca')) { return; }

    // C.logo puede ser: 'sostenido' (logo de la marca), 'archivo' (imagen
    // indicada en LOGO= del .conf, incrustada por build.sh) o un <svg> propio
    var archivo = (typeof SOSTENIDO_LOGO_ARCHIVO === 'string') ? SOSTENIDO_LOGO_ARCHIVO : null;
    var logo = C.logo === 'sostenido' ? LOGO : C.logo;
    if (C.logo === 'archivo') { logo = archivo; }
    if (!logo) { return; }

    var marca = document.createElement(C.enlace ? 'a' : 'div');
    marca.className = 's-marca' + (C.logoFondo ? ' s-marca--fondo' : '');
    if (C.enlace) { marca.href = C.enlace; }
    marca.setAttribute('aria-label', C.nombre || 'Inicio');
    if (C.logoAlto) { marca.style.setProperty('--s-logo-alto', C.logoAlto + 'px'); }  // alto del logo en la cabecera
    if (C.logo === 'archivo') {
      // Con dos versiones, el CSS muestra la que corresponde según la cabecera
      // sea clara u oscura (ver .s-logo--cabecera-* en 30-layout.css)
      var oscuro = (typeof SOSTENIDO_LOGO_ARCHIVO_OSCURO === 'string') ? SOSTENIDO_LOGO_ARCHIVO_OSCURO : null;
      var img = document.createElement('img');
      img.src = logo;
      img.alt = C.nombre || '';
      if (oscuro) {
        img.className = 's-logo--cabecera-clara';
        var img2 = document.createElement('img');
        img2.src = oscuro;
        img2.alt = C.nombre || '';
        img2.className = 's-logo--cabecera-oscura';
        marca.appendChild(img2);
      }
      marca.appendChild(img);
    } else {
      marca.innerHTML = logo;                            // SVG definido en la variante (no viene del usuario)
    }

    if (C.lema) {
      var lema = document.createElement('span');
      lema.className = 's-marca__lema';
      lema.textContent = C.lema;
      marca.appendChild(lema);
    }
    var titulo = header.querySelector('h1');
    header.insertBefore(marca, titulo || header.firstChild);
  }

  function insertarCredito() {
    if (!C.credito || !LOGO) { return; }
    var pie = document.getElementById('footer');
    if (!pie || pie.querySelector('.s-credito')) { return; }

    var credito = document.createElement('span');
    credito.className = 's-credito';
    credito.appendChild(document.createTextNode('Realizado y mantenido por'));

    var enlace = document.createElement('a');
    enlace.href = 'https://sostenido.com.ar';
    enlace.target = '_blank';
    enlace.rel = 'noopener';
    enlace.setAttribute('aria-label', 'SOSTENIDO');
    enlace.innerHTML = LOGO;
    credito.appendChild(enlace);

    pie.appendChild(credito);
  }

  /* ---------- 3. Apariencia en el menú del usuario ----------
     Se agrega al final del desplegable del avatar (#account .dropdown-content).
     Redmine no cierra ese desplegable con clics dentro de él, así que el
     usuario puede probar opciones y ver el cambio en el momento.
     Usuarios anónimos no tienen desplegable: ven el modo del sistema. */
  function grupo(titulo, opciones, actual, alElegir) {
    var caja = document.createElement('div');
    caja.className = 's-apariencia__grupo';
    caja.setAttribute('role', 'group');
    caja.setAttribute('aria-label', titulo);

    var rotulo = document.createElement('span');
    rotulo.className = 's-apariencia__rotulo';
    rotulo.textContent = titulo;
    caja.appendChild(rotulo);

    var fila = document.createElement('div');
    fila.className = 's-apariencia__opciones';
    var botones = [];
    opciones.forEach(function (op) {
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 's-apariencia__opcion';
      b.setAttribute('data-valor', op.valor);
      b.setAttribute('aria-pressed', op.valor === actual ? 'true' : 'false');
      b.title = op.texto;
      b.innerHTML = op.icono;                      // íconos y muestras propios del tema
      var texto = document.createElement('span');
      texto.textContent = op.texto;
      b.appendChild(texto);
      b.addEventListener('click', function (ev) {
        ev.preventDefault();
        botones.forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
        alElegir(op.valor);
      });
      botones.push(b);
      fila.appendChild(b);
    });
    caja.appendChild(fila);
    return caja;
  }

  function insertarApariencia() {
    var menu = document.querySelector('#account .dropdown-content');
    if (!menu || menu.querySelector('.s-apariencia')) { return; }

    var seccion = document.createElement('div');
    seccion.className = 's-apariencia';

    seccion.appendChild(grupo('Modo', MODOS.map(function (m) {
      return { valor: m, texto: ETIQUETA_MODO[m], icono: ICONO[m] };
    }), modo, function (valor) {
      modo = valor;
      html.setAttribute('data-modo', modo);
      guardar('modo', modo);
    }));

    if (C.elegirPaleta) {
      seccion.appendChild(grupo('Colores', Object.keys(PALETAS).map(function (p) {
        return { valor: p, texto: PALETAS[p],
                 icono: '<span class="s-muestra s-muestra--' + p + '" aria-hidden="true"></span>' };
      }), paleta, function (valor) {
        paleta = valor;
        html.setAttribute('data-paleta', paleta);
        guardar('paleta', paleta);
      }));
    }

    var divisor = document.createElement('div');
    divisor.className = 'dropdown-divider';
    menu.appendChild(divisor);
    menu.appendChild(seccion);
  }

  function iniciar() {
    insertarMarca();
    insertarCredito();
    insertarApariencia();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', iniciar);
  } else {
    iniciar();
  }
})();
