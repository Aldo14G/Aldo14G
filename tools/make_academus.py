#!/usr/bin/env python3
"""Recreación pixel-art de La Escuela de Atenas (Rafael, dominio público).

Genera assets/academus.svg sobre una rejilla de 160x100 píxeles: bóvedas
artesonadas, arcos en retirada, estatuas en nichos, la multitud de filósofos,
Platón y Aristóteles al centro, escalinata y suelo de mármol — con overlay
posthumanista (circuitos dorados + medallón borromeo). Todo determinista.
"""
import html

W, H = 160, 100
OUT = "assets/academus.svg"

# Paleta: tonos del fresco + acentos del perfil
CIELO = ["#c3d5df", "#b3c9d5", "#a4bdca"]
PIEDRA_CLARA = "#dcc9a2"
PIEDRA = "#c3ab7d"
PIEDRA_OSC = "#97805a"
SOMBRA = "#4a4238"
NICHO = "#37312b"
SUELO_CLARO = "#e0d2b0"
SUELO_OSC = "#7d5f3f"
LINEA_SUELO = "#57432f"
PIEL = "#dfb28c"
PIEL_OSC = "#b3875f"
TUNICA = ["#9e3a2b", "#1f5f86", "#c08a2e", "#6a4a78", "#20605a", "#7a7434", "#d8cba9", "#6b4a34"]
ORO = "#d6c19a"
NUDO = ["#d98b6f", "#d6c19a", "#a8c9ae"]

E = []  # elementos svg


def R(x, y, w, h, c, o=None):
    x, y, w, h = int(x), int(y), int(w), int(h)
    if w <= 0 or h <= 0:
        return
    op = f' opacity="{o}"' if o else ""
    E.append(f'<rect x="{x*10}" y="{y*10}" width="{w*10}" height="{h*10}" fill="{c}"{op}/>')


def figura(x, yb, h, tunica, pose="stand", piel=PIEL, pelo="#4a3428", barba=None, manto=None):
    """Filósofo: cabeza 3x3 con pelo/barba, túnica con pliegues, brazos con gesto."""
    osc = SOMBRA
    barba_filas = 2 if barba else 0
    # cabeza: pelo arriba, rostro, barba debajo
    R(x - 1, yb - h, 3, 1, pelo)
    R(x - 1, yb - h + 1, 3, 2, piel)
    R(x - 1, yb - h + 1, 1, 1, PIEL_OSC)
    if barba:
        R(x - 1, yb - h + 3, 3, 1, barba)
        R(x, yb - h + 4, 1, 1, barba)
    y0 = yb - h + 3 + barba_filas
    n = h - 3 - barba_filas
    for i in range(n):
        t = i / max(n - 1, 1)
        w = 5 + int(t * 3)  # hombros 5 -> base 8
        dx = x - w // 2
        R(dx, y0 + i, w, 1, tunica)
        R(dx, y0 + i, 1, 1, osc)  # pliegue sombra
        if manto and i > n // 3:  # manto diagonal (Aristóteles)
            R(dx + 1 + i // 2, y0 + i, 1, 1, manto)
        if i % 3 == 2:
            R(dx + w - 1, y0 + i, 1, 1, osc)
    # brazos y gestos
    if pose == "stand":
        R(x - 4, y0 + 1, 1, 4, tunica)
        R(x + 3, y0 + 1, 1, 4, tunica)
    elif pose == "scroll":  # pergamino en mano
        R(x - 4, y0 + 1, 1, 3, tunica)
        R(x + 1, y0 + 3, 3, 1, piel)
        R(x + 1, y0 + 2, 1, 3, "#e8dcc3")
    elif pose == "point":  # Platón: índice al cielo + Timeo bajo el brazo
        R(x + 3, y0 - 6, 1, 7, piel)
        R(x + 3, y0 - 7, 1, 1, piel)
        R(x - 4, y0 + 1, 1, 4, tunica)
        R(x - 4, y0 + 5, 3, 2, "#5a2f5e")
    elif pose == "palm":  # Aristóteles: palma a la tierra + libro
        R(x - 4, y0 + 2, 6, 1, piel)
        R(x + 1, y0 + 1, 3, 2, "#3d2f28")
        R(x + 1, y0 + 1, 3, 1, "#e8dcc3")
    # pies
    R(x - 3, yb, 6, 1, "#33291f")


def heraclito(x, yb):
    """El pensador en primer plano: bloque de mármol, codo en rodilla, puño en mejilla."""
    R(x - 4, yb - 6, 8, 6, "#ddd0ae")  # bloque
    R(x - 4, yb - 6, 8, 1, "#f4ecd8")
    R(x - 4, yb - 1, 8, 1, SOMBRA)
    R(x - 3, yb - 14, 6, 8, "#3a4a6b")  # torso inclinado
    R(x - 3, yb - 14, 2, 8, SOMBRA)
    R(x - 4, yb - 8, 7, 2, "#3a4a6b")  # piernas
    R(x - 1, yb - 18, 3, 3, PIEL)  # cabeza
    R(x - 1, yb - 18, 3, 1, "#2e2a26")  # pelo oscuro
    R(x + 1, yb - 15, 2, 2, PIEL)  # puño en mejilla
    R(x - 1, yb - 13, 2, 5, PIEL)  # brazo al codo
    R(x - 3, yb - 6, 5, 1, "#33291f")


def estatua(x, yb, c=PIEDRA_CLARA, atributo=None):
    R(x - 1, yb - 12, 2, 2, c)
    R(x - 2, yb - 10, 4, 6, c)
    R(x - 3, yb - 9, 1, 4, c)
    R(x + 2, yb - 9, 1, 4, c)
    R(x - 2, yb - 4, 1, 4, c)
    R(x + 1, yb - 4, 1, 4, c)
    R(x - 3, yb, 6, 2, PIEDRA_OSC)
    if atributo == "lira":  # Apolo
        R(x + 3, yb - 8, 1, 3, "#8f7d5a")
        R(x + 3, yb - 8, 3, 1, "#8f7d5a")
        R(x + 5, yb - 8, 1, 3, "#8f7d5a")
    elif atributo == "lanza":  # Minerva
        R(x - 4, yb - 14, 1, 12, "#8f7d5a")
        E.append(f'<circle cx="{(x - 6)*10}" cy="{(yb - 6)*10}" r="18" fill="none" stroke="#8f7d5a" stroke-width="7"/>')


def arco(cx, y_resorte, medio_ancho, y_apice, grosor, c_banda, c_caseton):
    """Banda de arco escalonada con casetones."""
    for y in range(y_apice, y_resorte + 1):
        t = (y - y_apice) / max(y_resorte - y_apice, 1)
        w = int(medio_ancho * (1 - t * t) ** 0.5)
        R(cx - w - grosor, y, grosor, 1, c_banda)
        R(cx + w, y, grosor, 1, c_banda)
        if (y - y_apice) % 3 == 0:  # casetón
            R(cx - w - grosor + 1, y, grosor - 2, 1, c_caseton)
            R(cx + w + 1, y, grosor - 2, 1, c_caseton)


# ---- cielo con bandas ----
for y in range(H):
    t = y / H
    c = CIELO[0] if t < 0.35 else (CIELO[1] if t < 0.65 else CIELO[2])
    R(0, y, W, 1, c)

# nubes en la vista central
R(70, 52, 8, 2, "#e9eef0")
R(72, 51, 4, 1, "#f4f7f8")
R(84, 56, 6, 2, "#e9eef0")

# edificio lejano
R(64, 58, 32, 20, "#d8c8a6")
R(64, 58, 32, 3, PIEDRA_OSC)
for i in range(5):
    R(68 + i * 5, 64, 2, 8, SOMBRA)

# ---- gran masa de piedra y apertura del arco ----
R(0, 0, W, 80, "#d3bd8d")
for y in range(0, 80, 4):
    R(0, y, W, 1, PIEDRA_OSC, 0.2)


def vano(cx, y_resorte, medio_ancho, y_apice, c):
    """Apertura de arco tallada en la masa (rellena de cielo)."""
    for y in range(y_apice, y_resorte + 1):
        t = (y - y_apice) / max(y_resorte - y_apice, 1)
        w = int(medio_ancho * (1 - t * t) ** 0.5)
        R(cx - w, y, w * 2, 1, c)


vano(80, 78, 66, 8, CIELO[1])

# ---- suelo de mármol en perspectiva ----
R(0, 78, W, 22, SUELO_CLARO)
for r in range(5):
    y = 80 + r * 4
    cw = 8
    off = (r % 2) * cw // 2
    for x in range(-cw, W + cw, cw):
        if ((x + off) // cw) % 2 == 0:
            R(x + off, y, cw, 4, SUELO_OSC, 0.35)
    R(0, y, W, 1, LINEA_SUELO)
# escalinata
for i in range(3):
    R(0, 70 + i * 3, W, 1, PIEDRA_OSC)
    R(0, 71 + i * 3, W, 2, PIEDRA_CLARA)

# ---- bóvedas gruesas en retirada ----
arco(80, 76, 52, 14, 10, PIEDRA_OSC, NICHO)
arco(80, 76, 36, 24, 7, PIEDRA_OSC, NICHO)
arco(80, 76, 22, 34, 5, PIEDRA_CLARA, PIEDRA_OSC)
# muros laterales con nichos + estatuas
for nx, atr in ((24, "lira"), (124, "lanza")):
    R(nx - 7, 22, 14, 34, PIEDRA_OSC)
    R(nx - 6, 24, 12, 30, NICHO)
    R(nx - 6, 24, 12, 2, SOMBRA)
    estatua(nx, 50, atributo=atr)
    R(nx - 7, 52, 14, 2, PIEDRA_CLARA)

# ---- gran arco de proscenio con casetones ----
arco(80, 100, 74, 2, 10, SOMBRA, PIEDRA_CLARA)
# jambas anchas con capitel y base
for jx in (0, 149):
    R(jx, 44, 11, 56, PIEDRA)
    R(jx - 1, 42, 13, 3, PIEDRA_CLARA)
    R(jx - 1, 94, 13, 6, PIEDRA_OSC)
    R(jx + 2, 50, 2, 44, PIEDRA_OSC, 0.6)
# enjutas con medallones grandes: brújula y libro
for mx in (16, 128):
    R(mx, 8, 16, 16, PIEDRA_OSC)
    R(mx, 8, 16, 2, PIEDRA_CLARA)
R(16, 8, 16, 16, PIEDRA_OSC)
E.append('<circle cx="240" cy="160" r="55" fill="none" stroke="#d6c19a" stroke-width="8"/>')
E.append('<path d="M240 120 L252 200 M200 160 L280 160" stroke="#d6c19a" stroke-width="8"/>')
R(130, 10, 12, 9, "#e8dcc3")
R(130, 12, 12, 1, "#3d2f28")
R(130, 15, 12, 1, "#3d2f28")
R(135, 10, 2, 9, "#6f2f20")
# balaustrada tras la multitud media
R(8, 62, 144, 2, PIEDRA_CLARA)
for bx in range(12, 150, 5):
    R(bx, 64, 2, 5, PIEDRA_OSC)
R(8, 69, 144, 1, SOMBRA)

# ---- multitud: ancianos con barba blanca, jóvenes, pergaminos ----
BLANCA = "#ddd8cc"
rib = 0
poses = ["stand", "scroll", "stand", "scroll", "stand"]
for i, fx in enumerate((22, 30, 38, 46, 54, 62, 98, 106, 114, 122, 130, 138)):
    figura(fx, 68, 12, TUNICA[rib % len(TUNICA)],
           pose=poses[i % len(poses)],
           barba=BLANCA if i % 3 == 0 else None,
           pelo="#c9c2b2" if i % 3 == 0 else "#4a3428")
    rib += 1
for i, fx in enumerate((16, 26, 36, 48, 58, 102, 112, 124, 136)):
    figura(fx, 80, 16, TUNICA[(rib + 3) % len(TUNICA)],
           pose="scroll" if i % 2 else "stand",
           barba=BLANCA if i % 4 == 0 else None)
    rib += 1
# Platón (barba blanca, índice al cielo, Timeo) y Aristóteles (manto, palma a tierra)
figura(71, 72, 22, "#9e3a2b", pose="point", barba=BLANCA, pelo="#c9c2b2")
figura(83, 72, 21, "#1f5f86", pose="palm", manto="#6b4a34", pelo="#2e2018")
# Diógenes tendido en la escalinata
R(64, 74, 2, 2, PIEL)
R(66, 74, 12, 3, "#1f5f86")
R(78, 74, 6, 2, PIEL_OSC)
R(66, 74, 2, 3, SOMBRA)
# Heráclito: el pensador en primer plano sobre su bloque
heraclito(58, 96)
# Pitágoras escribe + discípulo
figura(30, 94, 12, "#c08a2e", barba=BLANCA, pelo="#c9c2b2")
R(36, 86, 6, 5, "#3d2f28")
R(36, 86, 6, 1, "#e8dcc3")
R(38, 88, 2, 1, "#e8dcc3")
R(40, 84, 1, 3, PIEL)  # cálamo
figura(22, 92, 10, "#20605a", pose="scroll")
# Euclides inclinado + compás + discípulos
R(118, 82, 5, 12, "#6a4a78")
R(117, 80, 4, 3, PIEL)
R(114, 94, 8, 1, "#33291f")
E.append('<path d="M1140 880 L1120 960 M1140 880 L1170 950" stroke="#d6c19a" stroke-width="8"/>')
for sx in (106, 112, 128):
    R(sx - 1, 88, 2, 2, PIEL)
    R(sx - 2, 90, 4, 5, TUNICA[(sx) % len(TUNICA)])
# templete lejano sobre la colina, entre medallón y cabezas
R(75, 46, 12, 2, PIEDRA_OSC)
for cx in range(76, 86, 2):
    R(cx, 41, 1, 5, PIEDRA_CLARA)
R(74, 39, 14, 2, PIEDRA_OSC)
R(76, 36, 10, 3, "#6f2f20")
R(78, 34, 6, 2, "#6f2f20")
R(80, 33, 2, 1, ORO)
# fuga del suelo hacia el centro: rombo claro, líneas finas
E.append('<path d="M640 860 L800 820 L960 860 L800 900 Z" fill="none" stroke="#e0d2b0" stroke-width="6" opacity="0.8"/>')
for fx in (40, 60, 100, 120):
    E.append(f'<path d="M{fx*10} 1000 L800 800" stroke="#57432f" stroke-width="3" opacity="0.35"/>')

# ---- overlay posthumanista: circuitos sobre jambas y arco ----
E.append('<path d="M55 990 V880 H150 V820" fill="none" stroke="#d6c19a" stroke-width="8" opacity="0.8"/>')
E.append('<path d="M1545 990 V880 H1450 V820" fill="none" stroke="#d6c19a" stroke-width="8" opacity="0.8"/>')
for cx, cy in ((55, 990), (150, 820), (1545, 990), (1450, 820)):
    E.append(f'<rect x="{cx*10-12}" y="{cy*10-12}" width="24" height="24" fill="#d6c19a" opacity="0.9"/>')
# medallón borromeo suspendido del ápice
R(79, 8, 2, 10, ORO)
E.append('<circle cx="800" cy="250" r="70" fill="#2b2724" stroke="#d6c19a" stroke-width="9"/>')
for i, c in enumerate(NUDO):
    a = [730, 800, 870][i]
    b = [218, 218, 280][i]
    E.append(f'<circle cx="{a}" cy="{b}" r="28" fill="none" stroke="{c}" stroke-width="10"/>')

# marco
E.append('<rect x="5" y="5" width="1590" height="990" fill="none" stroke="#d6c19a" stroke-width="10"/>')

svg = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 1000" shape-rendering="crispEdges" role="img">'
    "<title>La Escuela de Atenas recreada en pixel art con circuitos posthumanos</title>"
    + "".join(E) + "</svg>"
)
with open("/Users/aldog/dev/Aldo14G/" + OUT, "w") as f:
    f.write(svg)
print(f"ok {OUT} ({len(E)} elementos)")
