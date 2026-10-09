#!/usr/bin/env python3
"""Cartel general: niños, adolescentes y familias (sin enfoque colegio) + QR servicios."""

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


def make_qr(size: int = 320) -> Image.Image:
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=2)
    qr.add_data(SERVICIOS_URL)
    qr.make(fit=True)
    img = qr.make_image(fill_color="rgb(9,45,74)", back_color="white").convert("RGB")
    return img.resize((size, size), Image.Resampling.NEAREST)


def draw_path(draw: ImageDraw.ImageDraw, y_base: int) -> None:
    import random

    random.seed(23)
    for i in range(28):
        x = 180 + i * 40
        y0 = y_base + random.randint(-45, 45)
        ang = random.uniform(-1.0, 1.0) * (1 - i / 32)
        ln = 38 + i * 2
        col = ACCENT if i > 18 else (200 + i, 210 + i, 220 + i)
        draw.line(
            [(x, y0), (x + math.cos(ang) * ln, y0 + math.sin(ang) * ln)],
            fill=col,
            width=3 if i > 18 else 2,
        )
    draw.line([(1150, y_base + 5), (W - 150, y_base - 110)], fill=PETROL, width=8)


def main() -> None:
    img = Image.new("RGB", (W, H), MIST)
    draw = ImageDraw.Draw(img)

    draw.rectangle([0, 0, W, 400], fill=PETROL)
    icon = Image.open(ASSETS / "isotipo.png").convert("RGBA")
    lw = 100
    lh = int(icon.height * (lw / icon.width))
    ir = icon.resize((lw, lh), Image.Resampling.LANCZOS)
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
    img.paste(light, (140, 90), light)

    draw.text((270, 105), "CEDRIC MILLES", font=font(INTER_SEMI, 44), fill=WHITE)
    draw.text((270, 165), "Psicología · Orientación · Rendimiento", font=font(INTER_REG, 22), fill=(180, 210, 235))
    draw.text(
        (140, 285),
        "PARA NIÑOS, ADOLESCENTES Y FAMILIAS",
        font=font(INTER_SEMI, 24),
        fill=ACCENT,
    )

    y = 500
    draw.text((140, y), "Crecer también es", font=font(INTER_BOLD, 76), fill=PETROL)
    draw.text((140, y + 92), "aprender a entenderse.", font=font(INTER_BOLD, 76), fill=PETROL)
    y += 200
    draw.text(
        (140, y),
        "Bienestar emocional, confianza y herramientas para el día a día.",
        font=font(INTER_MED, 36),
        fill=PRIMARY,
    )

    steps = [
        (420, "1", "COMPRENDER", "¿Qué siento?", ACCENT),
        (980, "2", "DECIDIR", "¿Qué elijo?", PRIMARY),
        (1540, "3", "AVANZAR", "Paso a paso", PETROL),
    ]
    cy = 880
    diam = 340
    for cx, num, word, q, col in steps:
        draw.ellipse([cx, cy, cx + diam, cy + diam], fill=col)
        draw.text((cx + 130, cy + 55), num, font=font(INTER_BOLD, 88), fill=WHITE)
        draw.text((cx + 48, cy + 165), word, font=font(INTER_SEMI, 30), fill=WHITE)
        bb = draw.textbbox((0, 0), q, font=font(INTER_REG, 28))
        draw.text((cx + (diam - (bb[2] - bb[0])) // 2, cy + 220), q, font=font(INTER_REG, 28), fill=WHITE)

    draw_path(draw, 1280)

    draw.rounded_rectangle([120, 1680, W - 120, 1940], radius=32, fill=WARM, outline=PRIMARY, width=3)
    draw.text((180, 1730), "Áreas de acompañamiento", font=font(INTER_SEMI, 36), fill=PETROL)
    areas = [
        "Emociones, autoestima y gestión emocional",
        "Relaciones, cambios y convivencia",
        "Hábitos, estudio, deporte y objetivos",
    ]
    ty = 1800
    for a in areas:
        draw.ellipse([180, ty + 8, 200, ty + 28], fill=ACCENT)
        draw.text((220, ty), a, font=font(INTER_REG, 28), fill=GRAY)
        ty += 48

    draw.rectangle([0, H - 520, W, H], fill=SKY)
    draw.rectangle([0, H - 520, W, H - 516], fill=PRIMARY)

    qr = make_qr(320)
    qx, qy = 160, H - 470
    draw.rounded_rectangle([qx - 20, qy - 20, qx + 340, qy + 340], radius=20, fill=WHITE, outline=PETROL, width=4)
    img.paste(qr, (qx, qy))

    draw.text((520, H - 450), "Escanea y descubre cómo puedo ayudarte", font=font(INTER_SEMI, 40), fill=PETROL)
    draw.text((520, H - 380), "cedricmilles.com/es/servicios/", font=font(INTER_MED, 30), fill=PRIMARY)
    draw.text(
        (520, H - 320),
        "Información y primera toma de contacto",
        font=font(INTER_REG, 26),
        fill=GRAY,
    )
    draw.text(
        (520, H - 220),
        "cedricmilles.com  ·  cedricluc.milles@gmail.com  ·  @Cedric_milles",
        font=font(INTER_REG, 24),
        fill=GRAY,
    )

    out_png = OUT / "cartel-servicios-familias-qr.png"
    out_jpg = OUT / "cartel-servicios-familias-qr.jpg"
    img.save(out_png, "PNG", dpi=(300, 300))
    img.save(out_jpg, "JPEG", quality=92, dpi=(300, 300))
    print(f"saved {out_png} ({os.path.getsize(out_png)} bytes)")


if __name__ == "__main__":
    main()
