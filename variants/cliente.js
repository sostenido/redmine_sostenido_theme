/* Plantilla de variante: configuración que lee theme.js.
   Copiar como variants/<nombre>.js junto con su .conf. */
window.SOSTENIDO_TEMA = {
  nombre: 'Mi organización',    // texto alternativo del logo
  paleta: 'sostenido',          // paleta por defecto: sostenido | grafito | papel
  modo: 'auto',                 // modo por defecto: auto | claro | oscuro
  logo: null,                   // null | 'sostenido' | 'archivo' (LOGO= del .conf) | '<svg>…</svg>'
  logoFondo: false,             // true = el logo va sobre una placa clara
  lema: '',                     // texto opcional debajo del logo
  enlace: '/',                  // a dónde lleva el logo
  credito: true,                // "Realizado y mantenido por SOSTENIDO" en el pie
  elegirPaleta: true            // el usuario elige paleta en su menú (el modo siempre)
};
