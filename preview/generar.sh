#!/usr/bin/env bash
# Genera preview/index.html (un solo archivo) con la variante demo.
set -euo pipefail
cd "$(dirname "$0")/.."
{
  echo '<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">'
  echo '<meta name="viewport" content="width=device-width, initial-scale=1">'
  echo '<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Noto+Sans:ital,wght@0,400;0,600;0,700;1,400&display=swap" rel="stylesheet">'
  echo '<title>Tema Sostenido para Redmine 7 — vista previa</title><style>'
  cat preview/base-simulada.css
  for f in src/[0-9][0-9]-*.css; do [[ "$f" == src/00-import.css ]] || cat "$f"; done
  echo '</style><script>'
  cat variants/demo.js src/marca-sostenido.js src/theme.js
  echo '</script></head>'
  cat preview/cuerpo.html
  echo '</html>'
} > preview/index.html
echo "preview/index.html generado"
