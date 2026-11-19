# Tema Sostenido para Redmine 7

Tema para Redmine 7 orientado a la simplicidad: cabecera con el logo, botón **Nueva petición** siempre visible, botones y campos más grandes,
modo claro y oscuro, y tres paletas.

- **Paletas:** cada una con versión clara y oscura, bien distintas entre sí para
  que cada usuario elija la que le resulte más cómoda:
  - claro: `sostenido` frío y luminoso (índigo) · `grafito` gris medio ·
    `papel` cálido, amarillento.
  - oscuro: `sostenido` el más oscuro · `grafito` gris oscuro intermedio ·
    `papel` el gris más claro y cálido.
  Los colores se definen en `herramientas/tokens.py`, que genera
  `src/10-tokens.css` y verifica el contraste (WCAG AA) antes de escribirlo.
- **Modos:** `auto` (sigue al sistema), `claro`, `oscuro`. Cada usuario lo
  cambia desde su menú (avatar); se recuerda en su navegador.
- **Tipografía:** Noto Sans, la de Redmine.

## Estructura

```
src/
  00-import.css        único @import: el CSS del núcleo de Redmine
  10-tokens.css        paletas y modos — GENERADO por herramientas/tokens.py
  20-redmine.css       conecta las variables de Redmine 7 (--oc-*, --color-*) con los tokens
  25-superficies.css   fondos blancos fijos del núcleo → superficie del tema
  26-oscuro.css        ajustes del oscuro que no se resuelven con variables (íconos de la barra de descripción)
  30-layout.css        barra superior, cabecera con marca, menú, pie
  40-componentes.css   campos, botones, mensajes, listas
  45-desplegables.css  "Saltar a un proyecto" y menús "…": lista limpia con títulos de grupo
  50-movimiento.css    transiciones
  55-jqueryui.css      diálogos, calendario y tooltips de jQuery UI (p. ej. "Editar petición" de Agile)
  60-plugins.css       DMSF (carpetas de sistema) y Agile de RedmineUP (tablero y tarjetas) (respeta "reducir movimiento" del sistema)
  marca-sostenido.js   logo (marca registrada, ver NOTICE.md)
  theme.js             aplica paleta/modo, inserta marca, crédito y selector
variants/
  <nombre>.conf        CARPETA (nombre del tema en Redmine) e INCLUIR_MARCA
  <nombre>.js          configuración: paleta, logo, lema, crédito
build.sh               genera dist/<CARPETA>/ listo para themes/
preview/               vista previa simulada (no es parte del tema)
```

## Variantes incluidas

| Variante  | Para qué sirve |
|-----------|----------------|
| `demo`    | muestra las tres paletas; el usuario elige modo y paleta en su menú |
| `cliente` | plantilla comentada para crear una variante nueva |

Las variantes de cada instalación real se mantienen en un repositorio privado
(ver `variants/LEEME.md`).

El crédito del pie es "Realizado y mantenido por" + logo de SOSTENIDO.
Las opciones de apariencia (modo claro / oscuro / automático y, si la variante
lo permite, paleta) aparecen al final del menú del usuario (avatar, arriba a la
derecha) y se recuerdan en su navegador. Los usuarios anónimos ven el modo de
su sistema.

### Logo de un cliente

1. Copiar la imagen a `variants/logos/<cliente>.png` (sirve png, jpg, svg o webp;
   mejor SVG, o PNG de al menos 60 px de alto para pantallas de alta densidad).
2. En `variants/<cliente>.conf` agregar `LOGO=logos/<cliente>.png`.
3. En `variants/<cliente>.js` poner `logo: 'archivo'`. Si la imagen tiene fondo
   blanco o colores que no contrastan con la cabecera, `logoFondo: true` la
   muestra sobre una placa clara. Con la paleta `papel` (cabecera blanca) no hace falta.
   Si el cliente tiene una versión con letras claras, agregar en el `.conf`
   `LOGO_CABECERA_OSCURA=logos/<cliente>-oscuro.png`: el tema muestra esa en
   las cabeceras oscuras (todas las paletas salvo `papel` en claro) y la normal
   en la cabecera blanca. Con las dos versiones no hace falta `logoFondo`.
4. `./build.sh <cliente>`: el logo queda incrustado en `theme.js`, no hay que
   copiar imágenes aparte.

Las variantes y logos de cada instalación están en `.gitignore`: no se
publican en el repositorio público.

## Uso

```bash
./build.sh demo                      # o el nombre de tu variante
cp -r dist/<CARPETA> <redmine>/themes/
cd <redmine> && bundle exec rails assets:precompile RAILS_ENV=production
# Administración → Configuración → Visualización → Tema
```

En Docker, copiar la carpeta y precompilar **al construir la imagen**, no al
arrancar el contenedor. Un bind mount del directorio de temas tapa lo que se
precompiló en la imagen: sirve para desarrollo, no para producción.

### Por qué un solo archivo CSS

Con Propshaft (Redmine 6 y 7), un `@import` relativo entre archivos del propio
tema puede devolver 404 por el digest de contenido. Por eso `build.sh`
concatena todo en un único `application.css`, y el único `@import` es el del
núcleo de Redmine, que es la forma estándar que usan los temas para Redmine 7.

## Licencia

GPL v2 o posterior (ver `LICENSE`). El nombre y el logo SOSTENIDO no están
cubiertos por la GPL (ver `NOTICE.md`).
