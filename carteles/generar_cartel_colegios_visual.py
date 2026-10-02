#!/usr/bin/env python3
"""Carteles escolares con diseño propio (ilustración, sin plantilla foto+cream)."""

from __future__ import annotations

import math
import os
from pathlib import Path

import qrcode
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
OUT = Path(__file__).resolve().parent

W, H = 2480, 3508
PETROL = (9, 45, 74)
NAVY = (6, 43, 85)
PRIMARY = (49, 95, 141)
ACCENT = (74, 139, 199)
SKY = (232, 242, 251)
MIST = (245, 249, 252)
GRAY = (83, 97, 111)
WHITE = (255, 255, 255)
WARM = (255, 244, 230)

SERVICIOS_URL = "https://cedricmilles.com/es/servicios/"

INTER_REG = "/usr/share/fonts/truetype/macos/Inter-Regular.ttf"
INTER_MED = "/usr/share/fonts/truetype/macos/Inter-Medium.ttf"
INTER_SEMI = "/usr/share/fonts/truetype/macos/Inter-SemiBold.ttf"
INTER_BOLD = "/usr/share/fonts/truetype/macos/Inter-Bold.ttf"


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def draw_compass(draw: ImageDraw.ImageDraw, cx: int, cy: int, r: int) -> None:
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=PRIMARY, width=6)
    # gaps top/bottom
    draw.chord([cx - 22, cy - r - 8, cx + 22, cy - r + 28], 0, 180, fill=SKY)
    draw.chord([cx - 22, cy + r - 28, cx + 22, cy + r + 8], 180, 360, fill=SKY)
    draw.polygon(
        [(cx - 38, cy + 42), (cx, cy - 58), (cx + 38, cy + 42), (cx, cy + 12)],
        fill=ACCENT,
    )
    draw.polygon([(cx - 38, cy + 42), (cx, cy + 12), (cx + 38, cy + 42), (cx, cy + 72)], fill=PETROL)
    draw.ellipse([cx - 10, cy + 2, cx + 10, cy + 22], fill=WHITE)


def draw_path_scene(draw: ImageDraw.ImageDraw, y_base: int) -> None:
    """Camino visual de líneas caóticas a una dirección clara."""
    import random

    random.seed(19)
    for i in range(30):
        x = 180 + i * 38
        y0 = y_base + random.randint(-50, 50)
        ang = random.uniform(-1.1, 1.1) * (1 - i / 34)
        ln = 35 + i * 2
        x2 = x + math.cos(ang) * ln
        y2 = y0 + math.sin(ang) * ln
        col = ACCENT if i > 20 else (200 + i, 210 + i, 220 + i)
        draw.line([(x, y0), (x2, y2)], fill=col, width=3 if i > 20 else 2)

    draw.line([(1180, y_base + 10), (W - 160, y_base - 120)], fill=PETROL, width=8)
    draw.polygon(
        [(W - 160, y_base - 120), (W - 110, y_base - 135), (W - 125, y_base - 95)],
        fill=PETROL,
    )


def draw_school_icon(draw: ImageDraw.ImageDraw, x: int, y: int, scale: float = 1.0) -> None:
    s = scale
    w, h = int(120 * s), int(90 * s)
    draw.rectangle([x, y + int(30 * s), x + w, y + h], fill=WHITE, outline=PETROL, width=int(4 * s))
    draw.polygon(
        [(x, y + int(30 * s)), (x + w // 2, y), (x + w, y + int(30 * s))],
        fill=PRIMARY,
    )
    draw.rectangle(
        [x + w // 2 - int(14 * s), y + int(55 * s), x + w // 2 + int(14 * s), y + h],
        fill=ACCENT,
    )


def draw_home_icon(draw: ImageDraw.ImageDraw, x: int, y: int, scale: float = 1.0) -> None:
    s = scale
    draw.polygon(
        [
            (x + int(50 * s), y),
            (x, y + int(45 * s)),
            (x + int(100 * s), y + int(45 * s)),
        ],
        fill=ACCENT,
    )
    draw.rectangle(
        [x + int(18 * s), y + int(45 * s), x + int(82 * s), y + int(95 * s)],
        fill=WHITE,
        outline=PETROL,
        width=int(3 * s),
    )


def make_qr(size: int = 300) -> Image.Image:
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=2)
    qr.add_data(SERVICIOS_URL)
    qr.make(fit=True)
    img = qr.make_image(fill_color="rgb(9,45,74)", back_color="white").convert("RGB")
    return img.resize((size, size), Image.Resampling.NEAREST)


def poster_colegios_mapa() -> Image.Image:
    """Diseño 1: mapa/brújula — lectura desde lejos en pasillos."""
    img = Image.new("RGB", (W, H), MIST)
    draw = ImageDraw.Draw(img)

    # Banda superior petróleo (no cream)
    draw.rectangle([0, 0, W, 420], fill=PETROL)
    icon = Image.open(ASSETS / "isotipo.png").convert("RGBA")
    lw = 100
    lh = int(icon.height * (lw / icon.width))
    ir = icon.resize((lw, lh), Image.Resampling.LANCZOS)
    # light icon on dark
    light = ir.copy()
    px = light.load()
    for yy in range(light.height):
        for xx in range(light.width):
            r, g, b, a = px[xx, yy]
            if a < 10:
                continue
            if r < 100:
                px[xx, yy] = (220, 235, 248, a)
            else:
                px[xx, yy] = (ACCENT[0], ACCENT[1], ACCENT[2], a)
    img.paste(light, (140, 95), light)

    draw.text((270, 115), "CEDRIC MILLES", font=font(INTER_SEMI, 44), fill=WHITE)
    draw.text((270, 175), "Psicología · Orientación · Rendimiento", font=font(INTER_REG, 22), fill=(180, 210, 235))
    draw.text((140, 300), "CARTEL PARA COLEGIOS  ·  FAMILIAS Y ALUMNADO", font=font(INTER_SEMI, 24), fill=ACCENT)

    # Zona niños — tipografía grande
    y = 520
    draw.text((140, y), "¿Hacia dónde quieres avanzar?", font=font(INTER_BOLD, 72), fill=PETROL)
    y += 100
    draw.text((140, y), "No hace falta tenerlo todo claro para empezar.", font=font(INTER_MED, 40), fill=PRIMARY)

    # Tres pasos en círculos grandes (staggered, no columnas blancas)
    steps = [
        (420, "1", "COMPRENDER", "¿Qué siento?", ACCENT),
        (980, "2", "DECIDIR", "¿Qué hago?", PRIMARY),
        (1540, "3", "AVANZAR", "¡Lo intento!", PETROL),
    ]
    cy = 920
    diam = 340
    for cx, num, word, q, col in steps:
        draw.ellipse([cx, cy, cx + diam, cy + diam], fill=col)
        draw.text((cx + 130, cy + 55), num, font=font(INTER_BOLD, 88), fill=WHITE)
        draw.text((cx + 48, cy + 165), word, font=font(INTER_SEMI, 30), fill=WHITE)
        bb = draw.textbbox((0, 0), q, font=font(INTER_REG, 28))
        draw.text((cx + (diam - (bb[2] - bb[0])) // 2, cy + 220), q, font=font(INTER_REG, 28), fill=WHITE)

    draw_path_scene(draw, 1320)

    # Iconos casa / colegio / tú
    draw_home_icon(draw, 220, 1480, 1.3)
    draw.text((200, 1600), "Casa", font=font(INTER_SEMI, 28), fill=PETROL)
    draw_school_icon(draw, 1080, 1450, 1.4)
    draw.text((1095, 1600), "Colegio", font=font(INTER_SEMI, 28), fill=PETROL)
    draw.ellipse([1860, 1490, 1980, 1610], outline=PRIMARY, width=5)
    draw.ellipse([1895, 1510, 1945, 1560], fill=ACCENT)
    draw.line([(1920, 1560), (1920, 1595)], fill=PETROL, width=5)
    draw.text((1885, 1620), "Tú", font=font(INTER_SEMI, 28), fill=PETROL)

    # Banda familias
    draw.rounded_rectangle([120, 1720, W - 120, 1980], radius=32, fill=WARM, outline=PRIMARY, width=3)
    draw.text((180, 1770), "Para familias y equipos educativos", font=font(INTER_SEMI, 36), fill=PETROL)
    tips = [
        "Tutorías y orientación con familias",
        "Convivencia y gestión emocional",
        "Motivación, estudio y cambios de etapa",
    ]
    ty = 1840
    for t in tips:
        draw.ellipse([180, ty + 8, 200, ty + 28], fill=ACCENT)
        draw.text((220, ty), t, font=font(INTER_REG, 28), fill=GRAY)
        ty += 48

    # Pie con QR — layout horizontal distinto
    draw.rectangle([0, H - 520, W, H], fill=SKY)
    draw.rectangle([0, H - 520, W, H - 516], fill=PRIMARY)

    qr = make_qr(320)
    qx, qy = 160, H - 470
    draw.rounded_rectangle([qx - 20, qy - 20, qx + 340, qy + 340], radius=20, fill=WHITE, outline=PETROL, width=4)
    img.paste(qr, (qx, qy))

    draw.text((520, H - 450), "Escanea y descubre cómo puedo ayudar", font=font(INTER_SEMI, 40), fill=PETROL)
    draw.text((520, H - 380), "cedricmilles.com/es/servicios/", font=font(INTER_MED, 30), fill=PRIMARY)
    draw.text(
        (520, H - 320),
        "Acompañamiento psicológico en el entorno escolar",
        font=font(INTER_REG, 26),
        fill=GRAY,
    )

    draw.text((520, H - 220), "cedricluc.milles@gmail.com  ·  @Cedric_milles", font=font(INTER_REG, 24), fill=GRAY)

    # Isotipo watermark large faint
    draw_compass(draw, W - 380, H - 260, 120)

    return img


def poster_colegios_panel() -> Image.Image:
    """Diseño 2: tres paneles verticales a toda altura (sin foto)."""
    img = Image.new("RGB", (W, H), WHITE)
    draw = ImageDraw.Draw(img)

    pw = W // 3
    colors = [ACCENT, PRIMARY, PETROL]
    titles = ["COMPRENDER", "DECIDIR", "AVANZAR"]
    subs = [
        "Qué ocurre\ny cómo te sientes",
        "Qué quieres\ny qué paso das",
        "Practicar\ny seguir",
    ]
    kids = [
        "Nombra la emoción",
        "Elige solo una cosa",
        "Pide ayuda si la necesitas",
    ]
    adults = [
        "Escucha antes de aconsejar",
        "Un acuerdo pequeño por semana",
        "Casa y colegio alineados",
    ]

    header_h = 200
    for i in range(3):
        x0 = i * pw
        draw.rectangle([x0, header_h, x0 + pw, H - 480], fill=colors[i])
        # panel number
        draw.text((x0 + 48, header_h + 80), str(i + 1), font=font(INTER_BOLD, 100), fill=WHITE)
        tw = draw.textbbox((0, 0), titles[i], font=font(INTER_BOLD, 52))[2]
        draw.text((x0 + (pw - tw) // 2, header_h + 240), titles[i], font=font(INTER_BOLD, 52), fill=WHITE)
        y = header_h + 380
        for line in subs[i].split("\n"):
            lw = draw.textbbox((0, 0), line, font=font(INTER_MED, 34))[2]
            draw.text((x0 + (pw - lw) // 2, y), line, font=font(INTER_MED, 34), fill=WHITE)
            y += 46

        sep = header_h + 580
        draw.line([(x0 + 60, sep), (x0 + pw - 60, sep)], fill=WHITE, width=2)
        draw.text((x0 + 56, sep + 40), "Niños y niñas", font=font(INTER_SEMI, 24), fill=WHITE)
        draw.text((x0 + 56, sep + 90), kids[i], font=font(INTER_REG, 26), fill=WHITE)
        draw.text((x0 + 56, sep + 200), "Familias", font=font(INTER_SEMI, 24), fill=WHITE)
        draw.text((x0 + 56, sep + 250), adults[i], font=font(INTER_REG, 26), fill=WHITE)

    draw.rectangle([0, 0, W, header_h], fill=WHITE)
    draw.line([(0, header_h), (W, header_h)], fill=PRIMARY, width=4)
    icon = Image.open(ASSETS / "isotipo.png").convert("RGBA")
    ir = icon.resize((90, int(90 * icon.height / icon.width)), Image.Resampling.LANCZOS)
    img.paste(ir, (80, 55), ir)
    draw.text((200, 70), "Cedric Milles", font=font(INTER_SEMI, 42), fill=PETROL)
    draw.text((200, 125), "Tu brújula en el colegio", font=font(INTER_REG, 26), fill=PRIMARY)

    # Footer
    draw.rectangle([0, H - 480, W, H], fill=PETROL)
    headline = "Entender dónde estás · Elegir hacia dónde ir · Avanzar"
    hw = draw.textbbox((0, 0), headline, font=font(INTER_SEMI, 38))[2]
    draw.text(((W - hw) // 2, H - 440), headline, font=font(INTER_SEMI, 38), fill=WHITE)

    qr = make_qr(280)
    img.paste(qr, (140, H - 400))
    draw.rectangle([130, H - 410, 430, H - 110], outline=WHITE, width=3)

    draw.text(
        (480, H - 380),
        "Servicios para colegios y familias",
        font=font(INTER_SEMI, 36),
        fill=WHITE,
    )
    draw.text((480, H - 310), "cedricmilles.com/es/servicios/", font=font(INTER_MED, 28), fill=ACCENT)
    draw.text(
        (480, H - 250),
        "Psicología · Orientación · Rendimiento",
        font=font(INTER_REG, 24),
        fill=(200, 220, 235),
    )
    draw.text(
        (480, H - 180),
        "cedricluc.milles@gmail.com  ·  @Cedric_milles",
        font=font(INTER_REG, 22),
        fill=(180, 200, 220),
    )

    return img


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    posters = [
        ("cartel-colegios-mapa-qr.png", poster_colegios_mapa()),
        ("cartel-colegios-paneles-qr.png", poster_colegios_panel()),
    ]
    for name, im in posters:
        path = OUT / name
        im.save(path, "PNG", dpi=(300, 300))
        jpg = OUT / name.replace(".png", ".jpg")
        im.save(jpg, "JPEG", quality=92, dpi=(300, 300))
        print(f"saved {path} ({os.path.getsize(path)} bytes)")


if __name__ == "__main__":
    main()
