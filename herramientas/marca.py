#!/usr/bin/env python3
"""
Genera una paleta "de marca" (cuarta opción, clave "marca") a partir de los
colores de una organización, en modo claro y oscuro.

  python3 herramientas/marca.py variants/marcas/<organizacion>.json

build.sh la llama sola cuando la variante tiene PALETA_MARCA= en su .conf, y
agrega el CSS resultante al final de application.css.

Formato del JSON (solo "primario" es obligatorio):
  {
    "nombre":   "Mi organización",   texto en el menú de colores
    "primario": "#8B1E2D",           color principal de la marca (cabecera, botones)
    "acento":   "#EF9F27",           marcador de pestaña y foco (por defecto, el ámbar)
    "cabecera": "oscura",            "oscura" = cabecera del color de marca con texto blanco
                                     "clara"  = cabecera casi blanca con texto del color de marca
    "degradado": ["#A1", "#B2"]      opcional: la cabecera oscura se pinta con un degradado
  }                                  de izquierda a derecha entre esos dos colores

El resto de la paleta (fondos, bordes, enlaces, versión oscura) se deriva del
color primario. Cada color de texto se corrige solo hasta cumplir WCAG AA
(4.5:1); si aun así algún par no llega, no se genera nada.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tokens import P as BASE, PARES, contraste, valor, bloque, bloque_oscuro_comun  # noqa: E402

BLANCO, NEGRO = "#FFFFFF", "#000000"


def rgb(h):
    h = h.strip().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def hexa(t):
    return "#" + "".join(f"{max(0, min(255, round(c))):02X}" for c in t)


def mezcla(a, b, t):
    """t = cuánto de b (0 = a puro, 1 = b puro)."""
    a, b = rgb(a), rgb(b)
    return hexa(tuple(x + (y - x) * t for x, y in zip(a, b)))


def ajustar(color, fondos, hacia, minimo=4.6):
    """Aclara u oscurece 'color' hasta contrastar con todos los 'fondos'."""
    destino = BLANCO if hacia == "claro" else NEGRO
    c = color
    for i in range(41):
        if all(contraste(c, f) >= minimo for f in fondos):
            return c
        c = mezcla(color, destino, i / 40)
    return c


def paleta_clara(pri, acento, cabecera):
    p = dict(BASE[("sostenido", "claro")])          # rampa y neutros de base
    p.update(
        bg=mezcla(pri, BLANCO, .96), surface=BLANCO, surface2=mezcla(pri, BLANCO, .94), blanco=BLANCO,
        border=mezcla("#D9DCE6", pri, .10), border_strong=mezcla("#9AA0B4", pri, .10),
        menu_bg=mezcla(pri, BLANCO, .92), menu_text="#16181D", menu_hover=mezcla(pri, BLANCO, .82),
        marker=acento,
    )
    p["link"] = ajustar(pri, [p["surface"], p["surface2"]], "oscuro")
    p["link_hover"] = mezcla(p["link"], NEGRO, .35)
    p["focus"] = p["link"]
    p["text_muted"] = ajustar("#5B6075", [p["surface"], p["surface2"]], "oscuro")
    p["primary"] = ajustar(pri, [BLANCO], "oscuro")
    p["primary_hover"] = mezcla(p["primary"], NEGRO, .18)
    p["primary_text"] = BLANCO
    if cabecera == "clara":
        p.update(header=mezcla(pri, BLANCO, .97), header_divider=mezcla(pri, BLANCO, .80),
                 topbar=ajustar(pri, [BLANCO], "oscuro"), topbar_text=BLANCO)
        p["header_text"] = ajustar(pri, [p["header"]], "oscuro")
        p["header_muted"] = ajustar("#5B6075", [p["header"]], "oscuro")
        p["topbar"] = mezcla(p["topbar"], NEGRO, .25)
    else:
        p["header"] = ajustar(pri, [BLANCO], "oscuro")
        p.update(header_text=BLANCO, header_divider="rgba(255,255,255,.16)",
                 topbar=mezcla(p["header"], NEGRO, .35))
        p["header_muted"] = ajustar(mezcla(pri, BLANCO, .70), [p["header"]], "claro")
        p["topbar_text"] = ajustar(mezcla(pri, BLANCO, .85), [p["topbar"]], "claro")
    return p


def paleta_oscura(pri, acento):
    p = dict(BASE[("sostenido", "oscuro")])
    p.update(
        topbar=mezcla(pri, NEGRO, .86), header=mezcla(pri, NEGRO, .72),
        header_text="#F2F1EC", header_divider="rgba(255,255,255,.10)",
        bg=mezcla("#0B0D12", pri, .05), surface=mezcla("#13161C", pri, .06),
        surface2=mezcla("#0F1117", pri, .05),
        border=mezcla("#242833", pri, .10), border_strong=mezcla("#3A3F4D", pri, .10),
        menu_bg=mezcla("#0F1117", pri, .06), menu_text="#D0D3DC",
    )
    p["blanco"] = p["surface"]
    # Marcador y foco: el acento, aclarado si hace falta para verse sobre fondo oscuro (3:1)
    p["marker"] = p["focus"] = ajustar(acento, [p["surface"], p["menu_bg"]], "claro", 3.0)
    p["menu_hover"] = mezcla(p["menu_bg"], BLANCO, .06)
    p["header_muted"] = ajustar(mezcla(pri, BLANCO, .55), [p["header"]], "claro")
    p["topbar_text"] = ajustar(mezcla(pri, BLANCO, .80), [p["topbar"]], "claro")
    p["link"] = ajustar(mezcla(pri, BLANCO, .25), [p["surface"], p["surface2"]], "claro")
    p["link_hover"] = mezcla(p["link"], BLANCO, .5)
    p["text_muted"] = ajustar("#A3A8B8", [p["surface"], p["surface2"]], "claro")
    cand = mezcla(pri, BLANCO, .10)
    if contraste(BLANCO, cand) >= 4.6:
        p.update(primary=cand, primary_hover=mezcla(cand, BLANCO, .15), primary_text=BLANCO)
    else:
        claro = ajustar(mezcla(pri, BLANCO, .35), ["#16181D"], "claro")
        p.update(primary=claro, primary_hover=mezcla(claro, BLANCO, .2), primary_text="#16181D")
    return p


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    datos = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    pri = datos["primario"]
    acento = datos.get("acento", "#EF9F27")
    cabecera = datos.get("cabecera", "oscura")
    nombre = datos.get("nombre", "Marca")

    claro, oscuro = paleta_clara(pri, acento, cabecera), paleta_oscura(pri, acento)

    # Degradado de cabecera: el texto debe leerse sobre los dos extremos
    deg_c = deg_o = "none"
    degradado = datos.get("degradado")
    if degradado and cabecera == "oscura":
        a, b = degradado
        for extremo in (a, b):
            if contraste(BLANCO, extremo) < 4.5:
                sys.exit(f"El texto blanco no se lee sobre {extremo} del degradado (contraste {contraste(BLANCO, extremo):.2f})")
        claro["header"] = mezcla(a, b, .5)
        claro["topbar"] = mezcla(b, NEGRO, .35)
        claro["header_muted"] = ajustar(mezcla(a, BLANCO, .70), [a, b], "claro")
        claro["topbar_text"] = ajustar(mezcla(a, BLANCO, .85), [claro["topbar"]], "claro")
        oa, ob = mezcla(a, NEGRO, .62), mezcla(b, NEGRO, .62)
        oscuro["header"] = mezcla(oa, ob, .5)
        oscuro["topbar"] = mezcla(b, NEGRO, .86)
        oscuro["header_muted"] = ajustar(mezcla(a, BLANCO, .55), [oa, ob], "claro")
        deg_c = f"linear-gradient(to right, {a}, {b})"
        deg_o = f"linear-gradient(to right, {oa}, {ob})"

    fallas = [f"{modo}: {a} sobre {b} = {contraste(valor(p, a), valor(p, b)):.2f}"
              for modo, p in (("claro", claro), ("oscuro", oscuro))
              for a, b in PARES if contraste(valor(p, a), valor(p, b)) < 4.5]
    if fallas:
        sys.exit("Paleta de marca con contraste insuficiente:\n  " + "\n  ".join(fallas))

    auto = 'html:not([data-modo="claro"]):not([data-modo="oscuro"])[data-paleta="marca"]'
    fijo = 'html[data-modo="oscuro"][data-paleta="marca"]'
    muestra_c = f'linear-gradient(135deg, {claro["header"]} 0 48%, {claro["bg"]} 48% 78%, {acento} 78%)'
    muestra_o = f'linear-gradient(135deg, {oscuro["header"]} 0 48%, {oscuro["bg"]} 48% 78%, {oscuro["primary"]} 78%)'
    css = f"""
/* ============================================================
   PALETA DE MARCA: {nombre} — GENERADO por herramientas/marca.py
   primario {pri} · acento {acento} · cabecera {cabecera} · degradado {degradado or "no"}
   ============================================================ */
html[data-paleta="marca"]{{
{bloque(claro, '  ')}
  --s-header-imagen:{deg_c};
}}
{fijo}{{
{bloque(oscuro, '  ')}
  --s-header-imagen:{deg_o};
{bloque_oscuro_comun(oscuro, '  ')}
}}
@media (prefers-color-scheme:dark){{
  {auto}{{
{bloque(oscuro, '    ')}
    --s-header-imagen:{deg_o};
{bloque_oscuro_comun(oscuro, '    ')}
  }}
}}
.s-muestra--marca{{ background:{muestra_c}; }}
html[data-modo="oscuro"] .s-muestra--marca{{ background:{muestra_o}; }}
@media (prefers-color-scheme:dark){{
  html:not([data-modo="claro"]):not([data-modo="oscuro"]) .s-muestra--marca{{ background:{muestra_o}; }}
}}
"""
    sys.stdout.write(css)


if __name__ == "__main__":
    main()
