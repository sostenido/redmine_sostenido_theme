#!/usr/bin/env python3
"""
Genera src/10-tokens.css a partir de las paletas definidas acá.

  python3 herramientas/tokens.py

Cada paleta tiene una versión clara y una oscura, con su propia rampa de
grises. La idea es que las tres se distingan a simple vista y cada usuario
elija la que le resulte más cómoda:

  claro:   sostenido = frío y luminoso · grafito = gris medio · papel = cálido, amarillento
  oscuro:  sostenido = el más oscuro   · grafito = gris oscuro intermedio · papel = gris más claro y cálido

Antes de escribir el archivo verifica el contraste (WCAG AA, 4.5:1) de los
pares de texto importantes y aborta si alguno no llega.
"""
from pathlib import Path
import sys

# ---------------------------------------------------------------------------
# Paletas. Claves:
#   topbar / topbar_text            barra superior
#   header / header_text / header_muted / header_divider   cabecera
#   menu_bg / menu_text / menu_hover                        menú del proyecto
#   bg / surface / surface2 / blanco                        fondos (página, contenido, lateral, campos)
#   border / border_strong
#   text / text_muted / link / link_hover
#   primary / primary_hover / primary_text                  botón principal y "Nueva petición"
#   marker / focus                                          marcador de pestaña y foco
#   g0..g9                                                  rampa que reemplaza los grises de Redmine
# ---------------------------------------------------------------------------
P = {
  ("sostenido", "claro"): dict(
    topbar="#1B2550", topbar_text="#DDE1F3",
    header="#23306B", header_text="#FFFFFF", header_muted="#AEB6DD", header_divider="rgba(255,255,255,.16)",
    menu_bg="#EEF0F9", menu_text="#16181D", menu_hover="#DDE1F3",
    bg="#F5F6FA", surface="#FFFFFF", surface2="#F0F2F8", blanco="#FFFFFF",
    border="#D9DCE6", border_strong="#9AA0B4",
    text="#16181D", text_muted="#5B6075", link="#33448F", link_hover="#1B2550",
    primary="#23306B", primary_hover="#33448F", primary_text="#FFFFFF",
    marker="#EF9F27", focus="#33448F",
    g=["#F8F9FC", "#F0F2F8", "#E6E9F1", "#D9DCE6", "#C5C9D6", "#9AA0B4", "#7A8095", "#5B6075", "#33374A", "#16181D"],
  ),
  ("grafito", "claro"): dict(
    topbar="#22252A", topbar_text="#C9CDD3",
    header="#3A3F47", header_text="#F4F5F6", header_muted="#B9BEC6", header_divider="rgba(255,255,255,.12)",
    menu_bg="#D9DCE0", menu_text="#1E2125", menu_hover="#C9CDD3",
    bg="#E4E6E9", surface="#F4F5F6", surface2="#ECEDEF", blanco="#F4F5F6",
    border="#C9CDD3", border_strong="#8D939C",
    text="#1E2125", text_muted="#4E545C", link="#2F3F86", link_hover="#1E2125",
    primary="#3A3F47", primary_hover="#50565F", primary_text="#FFFFFF",
    marker="#EF9F27", focus="#2F3F86",
    g=["#F4F5F6", "#ECEDEF", "#E4E6E9", "#D9DCE0", "#C9CDD3", "#A9AEB6", "#8D939C", "#545A63", "#33373D", "#1E2125"],
  ),
  ("papel", "claro"): dict(
    topbar="#3D3426", topbar_text="#EDE3CC",
    header="#F3EAD3", header_text="#23306B", header_muted="#6B5D45", header_divider="#DCCFAE",
    menu_bg="#EBE0C4", menu_text="#3D3426", menu_hover="#E2D5B4",
    bg="#F1E8D2", surface="#FBF6EA", surface2="#F5EDDA", blanco="#FBF6EA",
    border="#DCCFAE", border_strong="#A8987A",
    text="#2B2418", text_muted="#5E5139", link="#2F3F86", link_hover="#1B2550",
    primary="#23306B", primary_hover="#33448F", primary_text="#FFFFFF",
    marker="#C77C0E", focus="#2F3F86",
    g=["#FBF6EA", "#F5EDDA", "#EFE5CC", "#E6DABB", "#DCCFAE", "#BFB092", "#A8987A", "#6B5D45", "#463C2B", "#2B2418"],
  ),
  ("sostenido", "oscuro"): dict(
    topbar="#0A0C14", topbar_text="#C9CEE8",
    header="#141A33", header_text="#F2F1EC", header_muted="#9AA5DA", header_divider="rgba(255,255,255,.10)",
    menu_bg="#0F1117", menu_text="#D0D3DC", menu_hover="#1A1E2A",
    bg="#0B0D12", surface="#13161C", surface2="#0F1117", blanco="#13161C",
    border="#242833", border_strong="#3A3F4D",
    text="#ECEDF1", text_muted="#A3A8B8", link="#8E9BDB", link_hover="#C9CEE8",
    primary="#4E62B8", primary_hover="#6B7DCB", primary_text="#FFFFFF",
    marker="#EF9F27", focus="#EF9F27",
    g=["#0F1117", "#13161C", "#1A1E26", "#242833", "#3A3F4D", "#575D6E", "#7A8095", "#A3A8B8", "#D0D3DC", "#ECEDF1"],
  ),
  ("grafito", "oscuro"): dict(
    topbar="#16181B", topbar_text="#B8BCC3",
    header="#24272C", header_text="#F1F2F3", header_muted="#A3A8B0", header_divider="rgba(255,255,255,.10)",
    menu_bg="#2A2D32", menu_text="#D4D7DC", menu_hover="#34383E",
    bg="#1F2125", surface="#2A2D32", surface2="#25282C", blanco="#2A2D32",
    border="#3A3E45", border_strong="#555A62",
    text="#EEF0F2", text_muted="#B0B5BD", link="#9AA6E0", link_hover="#D0D5F0",
    primary="#EF9F27", primary_hover="#F5B655", primary_text="#16181D",
    marker="#EF9F27", focus="#EF9F27",
    g=["#25282C", "#2A2D32", "#31353A", "#3A3E45", "#4A4F57", "#666B74", "#8A9099", "#B0B5BD", "#D4D7DC", "#EEF0F2"],
  ),
  ("papel", "oscuro"): dict(
    topbar="#2A2620", topbar_text="#E6DCC6",
    header="#3E3A33", header_text="#F3EBD9", header_muted="#CFC4AC", header_divider="rgba(255,255,255,.12)",
    menu_bg="#46423A", menu_text="#E6DCC6", menu_hover="#504B42",
    bg="#36332D", surface="#423E37", surface2="#3B3832", blanco="#423E37",
    border="#57524A", border_strong="#756E62",
    text="#F3EBD9", text_muted="#D3C9B2", link="#B4BDEA", link_hover="#DDE1F3",
    primary="#9AA6E0", primary_hover="#B4BDEA", primary_text="#141C40",
    marker="#F0B04A", focus="#F0B04A",
    g=["#3B3832", "#423E37", "#4A463E", "#57524A", "#675F55", "#81796C", "#A0978A", "#CFC4AC", "#E6DCC6", "#F3EBD9"],
  ),
}

# Pares que tienen que llegar a 4.5:1 (texto sobre fondo)
PARES = [
    ("header_text", "header"), ("header_muted", "header"), ("topbar_text", "topbar"),
    ("menu_text", "menu_bg"), ("primary_text", "primary"),
    ("text", "bg"), ("text", "surface"), ("text_muted", "surface"), ("text_muted", "surface2"),
    ("link", "surface"), ("link", "surface2"), ("g7", "surface"),
]


def lum(h):
    h = h.lstrip("#")
    r, g, b = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def contraste(a, b):
    a, b = lum(a), lum(b)
    return (max(a, b) + .05) / (min(a, b) + .05)


def valor(p, k):
    return p["g"][int(k[1])] if k[0] == "g" and k[1:].isdigit() else p[k]


def rgb(h):
    h = h.lstrip("#")
    return ", ".join(str(int(h[i:i + 2], 16)) for i in (0, 2, 4))


def bloque(p, sangria):
    s = sangria
    L = [
        f"{s}--s-topbar:{p['topbar']}; --s-topbar-text:{p['topbar_text']};",
        f"{s}--s-header:{p['header']}; --s-header-text:{p['header_text']};",
        f"{s}--s-header-muted:{p['header_muted']}; --s-header-divider:{p['header_divider']};",
        f"{s}--s-menu-bg:{p['menu_bg']}; --s-menu-text:{p['menu_text']}; --s-menu-hover:{p['menu_hover']};",
        f"{s}--s-bg:{p['bg']}; --s-surface:{p['surface']}; --s-surface-2:{p['surface2']}; --s-blanco:{p['blanco']};",
        f"{s}--s-border:{p['border']}; --s-border-strong:{p['border_strong']};",
        f"{s}--s-text:{p['text']}; --s-text-muted:{p['text_muted']};",
        f"{s}--s-link:{p['link']}; --s-link-hover:{p['link_hover']};",
        f"{s}--s-primary:{p['primary']}; --s-primary-hover:{p['primary_hover']}; --s-primary-text:{p['primary_text']};",
        f"{s}--s-marker:{p['marker']}; --s-focus:{p['focus']};",
        f"{s}" + " ".join(f"--s-g{i}:{c};" for i, c in enumerate(p["g"][:5])),
        f"{s}" + " ".join(f"--s-g{i}:{c};" for i, c in enumerate(p["g"][5:], 5)),
        f"{s}--s-g9-rgb:{rgb(p['g'][9])};",
    ]
    return "\n".join(L)


def bloque_oscuro_comun(p, sangria):
    """Ajustes de Redmine que dependen de la rampa de cada paleta oscura."""
    s = sangria
    return "\n".join([
        f"{s}--oc-indigo-0:{p['g'][0]}; --oc-indigo-1:{p['g'][2]}; --oc-indigo-2:{p['g'][3]};",
        f"{s}--oc-blue-0:{p['g'][2]};",
    ])


OSCURO_GENERAL = """  color-scheme:dark;
  --s-accent-ink:#EF9F27;
  --s-ok:#4ADE80; --s-error:#F87171; --s-amber-100:#2A2113;
  --s-sombra:0 1px 2px rgba(0,0,0,.4); --s-sombra-lg:0 4px 12px rgba(0,0,0,.5);
  /* Colores de Open Color que Redmine usa como texto: se aclaran */
  --oc-blue-9:#9AA6E0; --oc-blue-7:#7C8AD1; --oc-blue-5:#7C8AD1;
  --oc-indigo-9:#AEB6DD; --oc-indigo-5:#7C8AD1;
  --oc-red-9:#F87171; --oc-red-8:#F87171; --oc-red-3:#7F1D1D; --oc-red-1:#2C1517;
  --oc-green-9:#4ADE80; --oc-green-8:#4ADE80; --oc-green-7:#4ADE80;
  --oc-green-3:#14532D; --oc-green-2:#16301F; --oc-green-1:#132619;
  --oc-yellow-9:#FACC15; --oc-yellow-3:#5C4813; --oc-yellow-1:#2A2113; --oc-yellow-0:#231C10;
  --oc-pink-9:#F472B6; --oc-grape-9:#D8B4FE; --oc-grape-7:#C084FC; --oc-orange-9:#FDBA74;"""

CABECERA = """/* ============================================================
   10 · TOKENS — ARCHIVO GENERADO por herramientas/tokens.py
   Para cambiar colores, editar las paletas en ese script y volver a
   correrlo: verifica el contraste antes de escribir este archivo.

   Paletas: sostenido (por defecto) · grafito · papel
   Modos:   claro · oscuro · auto (sigue al sistema)
     claro:   sostenido = frío y luminoso · grafito = gris medio · papel = cálido
     oscuro:  sostenido = el más oscuro · grafito = intermedio · papel = el más claro

   theme.js pone en <html>: data-paleta="..." y data-modo="..."
   Sin JavaScript se usa "sostenido" y el modo del sistema.
   ============================================================ */

/* ---------- Constantes de marca y forma (no cambian) ---------- */
:root{
  --s-indigo-900:#141C40; --s-indigo-800:#1B2550; --s-indigo-700:#23306B;
  --s-indigo-500:#33448F; --s-indigo-400:#4E62B8; --s-indigo-300:#7C8AD1;
  --s-indigo-100:#DDE1F3; --s-indigo-50:#EEF0F9;
  --s-amber-500:#EF9F27; --s-amber-800:#8A5209; --s-amber-100:#FDEBCE;
  --s-accent:#EF9F27; --s-accent-ink:#8A5209;
  --s-ok:#1F7A4D; --s-error:#B3261E;
  --s-radio:6px; --s-radio-lg:10px;
  --s-sombra:0 1px 2px rgba(22,24,29,.06), 0 1px 3px rgba(22,24,29,.10);
  --s-sombra-lg:0 4px 12px rgba(22,24,29,.12);
  --s-dur:160ms; --s-ease:cubic-bezier(.16,1,.3,1);
  --s-control-h:36px;
}
"""


def sel_claro(nombre):
    if nombre == "sostenido":
        return ':root, html[data-paleta="sostenido"]'
    return f'html[data-paleta="{nombre}"]'


def sel_oscuro(nombre, auto):
    base = 'html:not([data-modo="claro"]):not([data-modo="oscuro"])' if auto else 'html[data-modo="oscuro"]'
    if nombre == "sostenido":
        return base + ':is([data-paleta="sostenido"],:not([data-paleta]))'
    return base + f'[data-paleta="{nombre}"]'


def main():
    # 1. Contraste
    fallas = []
    print("Contraste (mínimo 4.5):")
    for (nombre, modo), p in P.items():
        fila = []
        for a, b in PARES:
            c = contraste(valor(p, a), valor(p, b))
            fila.append(f"{a}/{b} {c:.1f}")
            if c < 4.5:
                fallas.append(f"{nombre} {modo}: {a} sobre {b} = {c:.2f}")
        print(f"  {nombre:9} {modo:6} " + " · ".join(fila))
    if fallas:
        print("\nNO SE ESCRIBIÓ EL ARCHIVO. Contraste insuficiente:\n  " + "\n  ".join(fallas))
        sys.exit(1)

    # 2. CSS
    out = [CABECERA]
    out.append("/* ============================ MODO CLARO ============================ */")
    for nombre in ("sostenido", "grafito", "papel"):
        out.append(f"{sel_claro(nombre)}{{\n{bloque(P[(nombre, 'claro')], '  ')}\n}}")

    out.append("""
/* ============================ MODO OSCURO ===========================
   Activo con data-modo="oscuro", o con "auto" (o sin atributo) cuando el
   sistema está en oscuro. Los bloques se repiten porque CSS no permite
   unir @media y atributo en un mismo selector. */""")
    out.append(f'html[data-modo="oscuro"]{{\n{OSCURO_GENERAL}\n}}')
    for nombre in ("sostenido", "grafito", "papel"):
        p = P[(nombre, "oscuro")]
        out.append(f"{sel_oscuro(nombre, False)}{{\n{bloque(p, '  ')}\n{bloque_oscuro_comun(p, '  ')}\n}}")

    interno = [f'  html:not([data-modo="claro"]):not([data-modo="oscuro"]){{\n'
               + OSCURO_GENERAL.replace("\n  ", "\n    ").replace("  color-scheme", "    color-scheme", 1) + "\n  }"]
    for nombre in ("sostenido", "grafito", "papel"):
        p = P[(nombre, "oscuro")]
        interno.append(f"  {sel_oscuro(nombre, True)}{{\n{bloque(p, '    ')}\n{bloque_oscuro_comun(p, '    ')}\n  }}")
    out.append("@media (prefers-color-scheme:dark){\n" + "\n".join(interno) + "\n}")

    destino = Path(__file__).resolve().parent.parent / "src" / "10-tokens.css"
    destino.write_text("\n\n".join(out) + "\n", encoding="utf-8")
    print(f"\nEscrito {destino}")


if __name__ == "__main__":
    main()
