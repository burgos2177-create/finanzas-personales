#!/usr/bin/env python3
"""
Generador del logo de Ferdium para "Finanzas Personales" (suite SOGRUB).
Lenguaje visual compartido con la suite: squircle con gradiente oscuro,
rejilla "blueprint" tenue del color de acento y glifo bold de acento con
"marcas grabadas" en color de fondo. Identidad propia: acento verde-teal
de ESTA app (#1fd196) y glifo de DOMINIO = una moneda ($) = finanzas.
"""
import math
import os
import cairosvg

# ── Paleta real del tema de la app (de :root en index.html) ──
ACCENT   = "#1fd196"   # --green  (acento de Finanzas Personales)
ACCENT_2 = "#12a374"   # --green2 (sombra del acento)
BG_TOP   = "#1b212d"   # gradiente squircle (consistente con la suite)
BG_BOT   = "#0d1015"
ENGRAVE  = "#0e1218"   # "marcas grabadas" = color de fondo profundo

S = 1024
CX = CY = S / 2
RX = 232               # radio del squircle

# ── Rejilla blueprint (líneas de acento al ~7%) ──
GRID_STEP = 64
grid = []
i = GRID_STEP
while i < S:
    grid.append(f'<line x1="{i}" y1="0" x2="{i}" y2="{S}"/>')
    grid.append(f'<line x1="0" y1="{i}" x2="{S}" y2="{i}"/>')
    i += GRID_STEP
grid_lines = "\n      ".join(grid)

# ── Reeding (cantos grabados de la moneda) ──
R_OUT = 300            # radio de la moneda
R_RIM = 252           # anillo interior grabado
N_TICKS = 36
ticks = []
for k in range(N_TICKS):
    a = (360 / N_TICKS) * k
    ticks.append(
        f'<rect x="-5" y="{-(R_OUT-6)}" width="10" height="30" rx="5" '
        f'transform="rotate({a:.3f})"/>'
    )
ticks_g = "\n        ".join(ticks)

# ── Glifo "$" (S de dos curvas + barra vertical), grabado en color de fondo ──
a = 78    # medio ancho de la S
def y(off):  # helper relativo al centro
    return CY + off
dollar_s = (
    f'M {CX+a:.1f} {y(-83):.1f} '
    f'C {CX+a:.1f} {y(-138):.1f} {CX-a:.1f} {y(-138):.1f} {CX-a:.1f} {y(-45):.1f} '
    f'C {CX-a:.1f} {y(15):.1f} {CX+a:.1f} {y(-15):.1f} {CX+a:.1f} {y(45):.1f} '
    f'C {CX+a:.1f} {y(138):.1f} {CX-a:.1f} {y(138):.1f} {CX-a:.1f} {y(83):.1f}'
)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {S} {S}" width="{S}" height="{S}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{BG_TOP}"/>
      <stop offset="1" stop-color="{BG_BOT}"/>
    </linearGradient>
    <radialGradient id="coin" cx="0.38" cy="0.34" r="0.85">
      <stop offset="0" stop-color="{ACCENT}"/>
      <stop offset="1" stop-color="{ACCENT_2}"/>
    </radialGradient>
    <clipPath id="sq">
      <rect x="0" y="0" width="{S}" height="{S}" rx="{RX}" ry="{RX}"/>
    </clipPath>
  </defs>

  <g clip-path="url(#sq)">
    <!-- fondo -->
    <rect x="0" y="0" width="{S}" height="{S}" fill="url(#bg)"/>
    <!-- rejilla blueprint -->
    <g stroke="{ACCENT}" stroke-width="2" opacity="0.07">
      {grid_lines}
    </g>
    <!-- viñeta sutil -->
    <rect x="0" y="0" width="{S}" height="{S}" fill="url(#bg)" opacity="0.25"/>

    <!-- ── Moneda (glifo de dominio) ── -->
    <g transform="translate({CX},{CY})">
      <circle r="{R_OUT}" fill="url(#coin)"/>
      <!-- reeding grabado en el canto -->
      <g fill="{ENGRAVE}" opacity="0.9">
        {ticks_g}
      </g>
    </g>

    <!-- anillo interior grabado -->
    <circle cx="{CX}" cy="{CY}" r="{R_RIM}" fill="none" stroke="{ENGRAVE}" stroke-width="14"/>

    <!-- símbolo $ grabado -->
    <g fill="none" stroke="{ENGRAVE}" stroke-width="50" stroke-linecap="round" stroke-linejoin="round">
      <path d="{dollar_s}"/>
    </g>
    <rect x="{CX-16}" y="{CY-178}" width="32" height="356" rx="16" fill="{ENGRAVE}"/>

    <!-- brillo superior del squircle -->
    <rect x="0" y="0" width="{S}" height="{S}" rx="{RX}" ry="{RX}"
          fill="none" stroke="#ffffff" stroke-opacity="0.06" stroke-width="2"/>
  </g>
</svg>'''

here = os.path.dirname(os.path.abspath(__file__))
svg_path = os.path.join(here, "icon.svg")
with open(svg_path, "w") as f:
    f.write(svg)
print("wrote", svg_path)

for size in (1024, 256, 64):
    out = os.path.join(here, f"icon-{size}.png")
    cairosvg.svg2png(url=svg_path, write_to=out,
                     output_width=size, output_height=size)
    print("rendered", out)
