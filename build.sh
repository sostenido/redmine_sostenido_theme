#!/usr/bin/env bash
# Genera la carpeta del tema lista para copiar a <redmine>/themes/
#   ./build.sh <variante>        p. ej.  ./build.sh demo
# Resultado: dist/<CARPETA>/{stylesheets/application.css, javascripts/theme.js}
#
# Todo el CSS se concatena en UN solo application.css. El único @import es el
# del núcleo de Redmine (src/00-import.css). Motivo: con Propshaft, los
# @import relativos entre archivos del propio tema pueden dar 404.
set -euo pipefail
cd "$(dirname "$0")"

variante="${1:-}"
if [[ -z "$variante" || ! -f "variants/$variante.conf" || ! -f "variants/$variante.js" ]]; then
  echo "uso: ./build.sh <variante>"
  echo "variantes disponibles:"
  for f in variants/*.conf; do echo "  - $(basename "$f" .conf)"; done
  exit 1
fi

# Leer la configuración sin ejecutarla
# LOGO= y LOGO_CABECERA_OSCURA= son opcionales: rutas a imágenes dentro de
# variants/, que se incrustan en theme.js
valor() { { grep -E "^$1=" "variants/$variante.conf" || true; } | head -1 | cut -d= -f2- | tr -d "\"' "; }
carpeta="$(valor CARPETA)"
incluir_marca="$(valor INCLUIR_MARCA)"
logo_archivo="$(valor LOGO)"
logo_oscuro="$(valor LOGO_CABECERA_OSCURA)"
[[ "$carpeta" =~ ^[a-z0-9_-]+$ ]] || { echo "CARPETA inválida en variants/$variante.conf"; exit 1; }

salida="dist/$carpeta"
rm -rf "$salida"
mkdir -p "$salida/stylesheets" "$salida/javascripts"

# CSS: 00-import primero, después el resto en orden numérico
cat src/[0-9][0-9]-*.css > "$salida/stylesheets/application.css"

# Incrusta una imagen de variants/ como data URI en una variable JS
incrustar() {
  local rel="$1" variable="$2" ruta tipo
  [[ -z "$rel" ]] && return 0
  ruta="variants/$rel"
  [[ -f "$ruta" ]] || { echo "No existe el logo $ruta" >&2; exit 1; }
  case "${ruta,,}" in
    *.png) tipo=image/png ;; *.jpg|*.jpeg) tipo=image/jpeg ;;
    *.svg) tipo=image/svg+xml ;; *.webp) tipo=image/webp ;;
    *) echo "Formato de logo no soportado: $ruta (usar png, jpg, svg o webp)" >&2; exit 1 ;;
  esac
  echo "/* Logo del cliente, incrustado por build.sh desde $rel */"
  echo "var $variable = 'data:$tipo;base64,$(base64 -w0 "$ruta")';"
}

# JS: configuración de la variante + logo (si corresponde) + theme.js
{
  echo "/* GENERADO por build.sh — variante: $variante. Editar src/ y variants/, no este archivo. */"
  cat "variants/$variante.js"
  [[ "$incluir_marca" == "si" ]] && cat src/marca-sostenido.js
  incrustar "$logo_archivo" SOSTENIDO_LOGO_ARCHIVO
  incrustar "$logo_oscuro" SOSTENIDO_LOGO_ARCHIVO_OSCURO
  cat src/theme.js
} > "$salida/javascripts/theme.js"

echo "Tema generado en $salida  (variante: $variante)"
echo "Instalar: copiar $salida a <redmine>/themes/ , precompilar assets y elegir el tema en"
echo "Administración → Configuración → Visualización."
