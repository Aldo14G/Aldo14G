#!/usr/bin/env python3
"""El Caminante sobre el mar de nubes (Friedrich, dominio público) en pixel art.

Rejilla de 160x100: figura de espaldas sobre el pico, mar de niebla por bandas,
crestas lejanas, Zuckerhut, pinos y cielo pálido — con un hilo dorado mínimo.
Todo determinista.
"""
OUT = "assets/wanderer.svg"
W, H = 160, 100

CIELO = ["#e2e9ec", "#d5dfe4", "#c6d3da"]
LEJOS = "#8fa3ad"
LEJOS_OSC = "#6b7f8a"
NIEBLA = ["#eef1f2", "#dfe6ea", "#ccd6dc", "#bcc8d0"]
ROCA = "#232a24"
ROCA_CLARA = "#3a4238"
ROCA_LUZ = "#5c6050"
OCRE = "#7a6a48"
ABRIGO = "#1d2823"
ABRIGO_OSC = "#121915"
PELO = "#c9a35a"
PELO_OSC = "#9a7a3e"
PIEL = "#d9b48f"
ORO = "#d6c19a"

E = []


def R(x, y, w, h, c, o=None):
    x, y, w, h = int(x), int(y), int(w), int(h)
    if w <= 0 or h <= 0:
        return
    op = f' opacity="{o}"' if o else ""
    E.append(f'<rect x="{x*10}" y="{y*10}" width="{w*10}" height="{h*10}" fill="{c}"{op}/>')


# ---- cielo ----
for y in range(40):
    R(0, y, W, 1, CIELO[0] if y < 15 else (CIELO[1] if y < 28 else CIELO[2]))
# vetas de nube
for cx, cy, w in ((30, 10, 26), (100, 18, 34), (60, 26, 22), (130, 8, 18)):
    R(cx, cy, w, 2, "#f2f5f6", 0.8)
    R(cx + 4, cy + 2, w - 8, 1, "#f2f5f6", 0.6)
# aves
for bx, by in ((52, 14), (56, 16), (108, 22)):
    R(bx, by, 3, 1, "#4a5458")
    R(bx + 1, by - 1, 1, 1, "#4a5458")

# ---- fondo base: niebla profunda abajo ----
R(0, 70, W, 30, "#c3cfd6")
R(0, 80, W, 20, "#b2bec6")
R(0, 90, W, 10, "#a2adb5")

# ---- crestas lejanas ----
R(0, 36, 52, 8, LEJOS_OSC)  # loma izquierda en pendiente
R(0, 36, 52, 2, LEJOS)
for x in range(0, 52, 4):
    R(x, 34 + x // 10, 4, 2, LEJOS_OSC)
# Zuckerhut derecha: pico afilado con muesca
for i, w in enumerate((10, 8, 6, 5, 4, 3, 2)):
    R(117 - w // 2, 40 - i * 3, w, 3, LEJOS)
R(117 - 5, 40 - 18, 2, 3, LEJOS)
R(117 + 3, 40 - 18, 2, 3, LEJOS)
R(113, 24, 8, 2, "#a9bcc5")
# cordillera derecha baja
R(96, 38, 64, 6, LEJOS_OSC)
R(96, 38, 64, 1, LEJOS)

# ---- mar de niebla: bandas anchas suaves + motas ----
R(0, 42, W, 28, NIEBLA[0])
import math
bandas = [(44, 6, NIEBLA[1]), (51, 5, NIEBLA[0]), (57, 5, NIEBLA[2]), (63, 5, NIEBLA[1]), (68, 2, NIEBLA[3])]
for y, h, c in bandas:
    for x in range(0, W, 8):
        ola = int(math.sin((x + y * 5) / 14) + 1)
        R(x, y + ola, 8, h - ola, c, 0.9)
for i in range(60):  # motas deterministas
    mx = (i * 37 + 11) % 156 + 2
    my = 44 + (i * 23) % 22
    R(mx, my, 2, 1, NIEBLA[3], 0.5)
# hilo dorado: corriente de datos en la niebla
E.append('<path d="M0 620 H120 V640 H260 V620 H420" fill="none" stroke="#d6c19a" stroke-width="5" opacity="0.55"/>')
E.append('<rect x="250" y="610" width="18" height="18" fill="#d6c19a" opacity="0.8"/>')

# ---- pináculos que emergen (izquierda): bases anchas, puntas ----
for px, ph in ((14, 14), (24, 20), (36, 12), (46, 8)):
    R(px - 1, 66 - ph, 8, ph, "#3d4442")
    R(px + 1, 66 - ph, 4, 3, "#6a7268")
    R(px, 66 - ph + 3, 2, ph - 3, "#232a26")
# cresta con abetos (derecha)
R(112, 58, 44, 12, "#4c554e")
R(112, 58, 44, 2, "#6a7268")
for tx in (120, 128, 138, 146):
    R(tx, 56, 2, 4, "#2c332c")  # tronco
    R(tx - 2, 52, 6, 2, "#2c332c")
    R(tx - 1, 50, 4, 2, "#2c332c")
    R(tx, 48, 2, 2, "#2c332c")

# ---- pico principal: cima estrecha que se ensancha al bajar ----
for y in range(66, 100):
    d = y - 66
    R(58 - d // 2, y, 44 + d * 2, 1, ROCA)
R(56, 66, 48, 2, ROCA_CLARA)  # filo superior iluminado
# peñascos laterales
for y in range(78, 100):
    R(8 + (y - 78) // 4, y, 32 - (y - 78) // 2, 1, "#2b322b")
    R(120 + (y - 78) // 4, y, 32 - (y - 78) // 2, 1, "#2b322b")
R(8, 78, 34, 2, "#4a5244")
R(120, 78, 34, 2, "#4a5244")
# facetas de luz izquierda + ocres
for fx, fy, fw, fh in ((50, 74, 6, 8), (60, 80, 5, 10), (72, 76, 4, 6), (96, 78, 6, 8)):
    R(fx, fy, fw, fh, ROCA_LUZ, 0.8)
R(56, 84, 4, 3, OCRE, 0.8)
R(88, 88, 5, 3, OCRE, 0.7)
R(100, 76, 3, 6, "#161c17")  # grietas
R(66, 86, 2, 10, "#161c17")

# ---- el caminante (de espaldas, x centro 82, pies y=68) ----
X, YB = 82, 68
# piernas y botas, paso abierto
R(X - 5, YB - 10, 3, 10, ABRIGO)
R(X + 2, YB - 11, 3, 11, ABRIGO)
R(X - 6, YB - 1, 5, 1, "#0e130f")
R(X + 1, YB - 1, 5, 1, "#0e130f")
# levita: hombros anchos, faldones al viento (derecha)
for i in range(14):
    w = 12 - (i // 4)
    R(X - 6, YB - 25 + i, w + (3 if i > 9 else 0), 1, ABRIGO)
R(X - 6, YB - 24, 2, 12, ABRIGO_OSC)  # pliegue sombra izq
R(X + 4, YB - 22, 1, 9, "#0e130f")  # pliegue central
R(X + 6, YB - 14, 3, 3, ABRIGO)  # faldón al viento
# cuello + camisa
R(X - 1, YB - 26, 3, 1, "#e8e4d8")
# cabeza y pelo al viento
R(X - 2, YB - 31, 5, 4, PELO)
R(X - 2, YB - 31, 5, 1, "#e0bd72")
R(X + 3, YB - 30, 2, 1, PELO)  # mechones al viento
R(X + 4, YB - 28, 1, 1, PELO)
R(X - 2, YB - 28, 1, 3, PELO_OSC)
# brazo derecho + bastón
R(X + 6, YB - 24, 2, 9, ABRIGO)
R(X + 6, YB - 15, 2, 2, PIEL)  # mano
R(X + 6, YB - 15, 1, 17, "#6b4a34")  # bastón hasta la roca
E.append('<rect x="873" y="688" width="16" height="16" fill="#d6c19a" opacity="0.95"/>')

svg = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 1000" shape-rendering="crispEdges" role="img">'
    "<title>El caminante sobre el mar de nubes recreado en pixel art</title>"
    + "".join(E) + "</svg>"
)
with open("/Users/aldog/dev/Aldo14G/" + OUT, "w") as f:
    f.write(svg)
print(f"ok {OUT} ({len(E)} elementos)")
