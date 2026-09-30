#!/usr/bin/env python3
"""Genera carteles A3 (200 dpi) según la normativa Cedric Milles."""

from __future__ import annotations

import math
import os
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
OUT = Path(__file__).resolve().parent

PETROL = (9, 45, 74)  # #092D4A
PRIMARY = (49, 95, 141)  # #315F8D
ACCENT = (74, 139, 199)  # #4A8BC7
GRAY = (83, 97, 111)  # #53616F
WHITE = (255, 255, 255)
RULE = (220, 228, 236)

W, H = 2339, 3307  # A3 @ 200 dpi
MARGIN = 180

INTER_REG = "/usr/share/fonts/truetype/macos/Inter-Regular.ttf"
INTER_MED = "/usr/share/fonts/truetype/macos/Inter-Medium.ttf"
INTER_SEMI = "/usr/share/fonts/truetype/macos/Inter-SemiBold.ttf"


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def ensure_isotipo() -> Image.Image:
    path = ASSETS / "isotipo.png"
    if path.exists():
        return Image.open(path).convert("RGBA")

    src = ASSETS / "logo-cedric-milles.png"
    im = Image.open(src).convert("RGBA")
    pixels = list(im.getdata())
    cleaned = []
    for r, g, b, a in pixels:
        if r > 248 and g > 248 and b > 248:
            cleaned.append((255, 255, 255, 0))
        else:
            cleaned.append((r, g, b, 255))
    im.putdata(cleaned)
    cropped = im.crop(im.getbbox())
    icon = cropped.crop((0, 0, cropped.width, 369))
    icon = icon.crop(icon.getbbox())
    ASSETS.mkdir(parents=True, exist_ok=True)
    icon.save(path)
    return icon


def center_text(draw: ImageDraw.ImageDraw, text: str, fnt, y: int, fill, canvas_w: int = W) -> int:
    bbox = draw.textbbox((0, 0), text, font=fnt)
    tw = bbox[2] - bbox[0]
    draw.text(((canvas_w - tw) // 2, y), text, font=fnt, fill=fill)
    return bbox[3] - bbox[1]


def wrap_lines(draw: ImageDraw.ImageDraw, text: str, fnt, max_w: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    cur = ""
    for word in words:
        test = (cur + " " + word).strip()
        bb = draw.textbbox((0, 0), test, font=fnt)
        if bb[2] - bb[0] <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def lighten_icon(icon: Image.Image) -> Image.Image:
    out = icon.copy()
    pix = out.load()
    for y in range(out.height):
        for x in range(out.width):
            r, g, b, a = pix[x, y]
            if a < 10:
                continue
            if r < 80 and b > r:
                pix[x, y] = (200, 220, 235, a)
            elif b > r and g < 160:
                pix[x, y] = (ACCENT[0], ACCENT[1], ACCENT[2], a)
    return out


def cartel_institucional(icon: Image.Image) -> Image.Image:
    img = Image.new("RGB", (W, H), WHITE)
    draw = ImageDraw.Draw(img)

    for y in range(0, 700):
        t = y / 700
        r = int(242 + (255 - 242) * t)
        g = int(247 + (255 - 247) * t)
        b = int(251 + (255 - 251) * t)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    # Una sola línea direccional muy sutil (metáfora de brújula)
    draw.line([(W // 2 - 10, 560), (W // 2 + 210, 470)], fill=(210, 224, 236), width=1)

    logo_w = 200
    logo_h = int(icon.height * (logo_w / icon.width))
    icon_r = icon.resize((logo_w, logo_h), Image.Resampling.LANCZOS)
    img.paste(icon_r, ((W - logo_w) // 2, 260), icon_r)

    y = 260 + logo_h + 40
    center_text(draw, "Cedric Milles", font(INTER_SEMI, 52), y, PETROL)
    center_text(
        draw,
        "Psicología  ·  Orientación  ·  Rendimiento",
        font(INTER_REG, 22),
        y + 70,
        PRIMARY,
    )

    draw.line([(MARGIN + 160, 700), (W - MARGIN - 160, 700)], fill=RULE, width=1)

    y = 780
    for line in (
        "Psicología para comprender.",
        "Orientación para decidir.",
        "Rendimiento para avanzar.",
    ):
        center_text(draw, line, font(INTER_MED, 54), y, PETROL)
        y += 72

    y += 36
    sub = (
        "Acompañamiento psicológico y orientación aplicada al "
        "desarrollo personal, académico, profesional y deportivo."
    )
    for line in wrap_lines(draw, sub, font(INTER_REG, 28), W - 2 * MARGIN - 80):
        center_text(draw, line, font(INTER_REG, 28), y, GRAY)
        y += 42

    y = 1240
    pillars = [
        ("COMPRENDER", "Qué ocurre y dónde estás."),
        ("DECIDIR", "Qué quieres y hacia dónde dirigirte."),
        ("AVANZAR", "Construir herramientas para llegar hasta allí."),
    ]
    block_left = MARGIN + 80
    block_right = W - MARGIN - 80
    accents = [ACCENT, PRIMARY, PETROL]
    for i, (word, desc) in enumerate(pillars):
        draw.rectangle([block_left, y + 8, block_left + 4, y + 78], fill=accents[i])
        draw.text((block_left + 36, y), word, font=font(INTER_SEMI, 72), fill=PETROL)
        draw.text((block_left + 36, y + 90), desc, font=font(INTER_REG, 26), fill=GRAY)
        y += 180
        if i < 2:
            draw.line([(block_left + 36, y - 30), (block_right, y - 30)], fill=(230, 235, 240), width=1)

    y = 1920
    center_text(draw, "Áreas de trabajo", font(INTER_MED, 24), y, PRIMARY)
    areas = [
        "Desarrollo personal",
        "Orientación y objetivos",
        "Gestión emocional",
        "Rendimiento deportivo",
        "Rendimiento académico",
        "Toma de decisiones",
    ]
    col_w = (W - 2 * MARGIN) // 2
    y += 70
    for i, area in enumerate(areas):
        col = i % 2
        row = i // 2
        ax = MARGIN + 100 + col * col_w
        ay = y + row * 48
        draw.ellipse([ax, ay + 10, ax + 8, ay + 18], fill=ACCENT)
        draw.text((ax + 24, ay), area, font=font(INTER_REG, 22), fill=GRAY)

    y = 2300
    cta = "Descubre cómo puedo ayudarte  →"
    cta_f = font(INTER_MED, 28)
    bb = draw.textbbox((0, 0), cta, font=cta_f)
    tw = bb[2] - bb[0]
    tx = (W - tw) // 2
    draw.text((tx, y), cta, font=cta_f, fill=PETROL)
    draw.line([(tx, y + 48), (tx + tw, y + 48)], fill=ACCENT, width=2)

    y = 2500
    center_text(
        draw,
        "“Entender dónde estás. Elegir hacia dónde ir. Avanzar.”",
        font(INTER_MED, 30),
        y,
        PRIMARY,
    )

    y = H - 220
    draw.line([(MARGIN, y), (W - MARGIN, y)], fill=RULE, width=1)
    center_text(draw, "COMPRENDER  ·  DECIDIR  ·  AVANZAR", font(INTER_SEMI, 22), y + 50, PETROL)
    center_text(draw, "cedricmilles.com", font(INTER_REG, 20), y + 100, GRAY)
    return img


def cartel_bienestar(icon: Image.Image) -> Image.Image:
    img = Image.new("RGB", (W, H), WHITE)
    draw = ImageDraw.Draw(img)

    for y in range(0, 1100):
        t = y / 1100
        r = int(236 + (255 - 236) * t)
        g = int(243 + (255 - 243) * t)
        b = int(248 + (255 - 248) * t)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    random.seed(7)
    for i in range(28):
        x = 220 + i * 28 + random.uniform(-10, 10)
        y0 = 980 + random.uniform(-90, 90) * (1 - i / 35)
        ang = random.uniform(-1.2, 1.2) * (1 - i / 32)
        length = 50 + i * 3
        x2 = x + math.cos(ang) * length
        y2 = y0 + math.sin(ang) * length
        if i > 18:
            color = ACCENT
            width = 2
        else:
            c = int(210 - i * 3)
            color = (c, c + 5, c + 10)
            width = 1
        draw.line([(x, y0), (x2, y2)], fill=color, width=width)
    draw.line([(980, 1000), (W - MARGIN - 40, 860)], fill=PETROL, width=2)

    logo_w = 90
    logo_h = int(icon.height * (logo_w / icon.width))
    icon_r = icon.resize((logo_w, logo_h), Image.Resampling.LANCZOS)
    img.paste(icon_r, (MARGIN, MARGIN - 20), icon_r)
    draw.text((MARGIN + logo_w + 28, MARGIN + 18), "CEDRIC MILLES", font=font(INTER_SEMI, 28), fill=PETROL)
    draw.text(
        (MARGIN + logo_w + 28, MARGIN + 58),
        "Psicología · Orientación · Rendimiento",
        font=font(INTER_REG, 18),
        fill=PRIMARY,
    )

    y = 1180
    for line, fnt in (
        ("No necesitas tenerlo todo claro", font(INTER_MED, 78)),
        ("para empezar a avanzar.", font(INTER_SEMI, 78)),
    ):
        for wrapped in wrap_lines(draw, line, fnt, W - 2 * MARGIN - 40):
            center_text(draw, wrapped, fnt, y, PETROL)
            y += 96
        y += 8

    y += 40
    sub = (
        "Psicología, orientación y herramientas prácticas para comprender "
        "dónde estás, definir lo que quieres y construir tu propio camino."
    )
    for line in wrap_lines(draw, sub, font(INTER_REG, 30), W - 2 * MARGIN - 100):
        center_text(draw, line, font(INTER_REG, 30), y, GRAY)
        y += 44

    y += 70
    tags = (
        "Autoconocimiento  ·  Objetivos  ·  Toma de decisiones  ·  "
        "Gestión emocional  ·  Desarrollo personal"
    )
    center_text(draw, tags, font(INTER_REG, 20), y, PRIMARY)

    y = 2680
    cta = "Empieza a encontrar tu dirección  →"
    cta_f = font(INTER_MED, 32)
    bb = draw.textbbox((0, 0), cta, font=cta_f)
    tw = bb[2] - bb[0]
    tx = (W - tw) // 2
    draw.text((tx, y), cta, font=cta_f, fill=PETROL)
    draw.line([(tx, y + 52), (tx + tw, y + 52)], fill=ACCENT, width=2)

    y = H - 180
    draw.line([(MARGIN, y), (W - MARGIN, y)], fill=RULE, width=1)
    center_text(
        draw,
        "“Entender dónde estás. Elegir hacia dónde ir. Avanzar.”",
        font(INTER_MED, 24),
        y + 40,
        PRIMARY,
    )
    center_text(draw, "cedricmilles.com", font(INTER_REG, 20), y + 88, GRAY)
    return img


def cartel_claridad(icon: Image.Image) -> Image.Image:
    img = Image.new("RGB", (W, H), PETROL)
    draw = ImageDraw.Draw(img)

    for r in range(900, 0, -4):
        t = r / 900
        shade = (
            int(9 + (49 - 9) * (1 - t) * 0.35),
            int(45 + (95 - 45) * (1 - t) * 0.35),
            int(74 + (141 - 74) * (1 - t) * 0.4),
        )
        draw.ellipse([W // 2 - r, 1100 - r * 0.7, W // 2 + r, 1100 + r * 0.7], outline=shade)

    random.seed(11)
    for _ in range(40):
        ang = random.uniform(0, 2 * math.pi)
        length = random.uniform(80, 420)
        dist = random.uniform(60, 380)
        x1 = W // 2 + math.cos(ang) * dist
        y1 = 1100 + math.sin(ang) * dist * 0.7
        a2 = ang + random.uniform(-0.4, 0.4)
        x2 = x1 + math.cos(a2) * length
        y2 = y1 + math.sin(a2) * length
        c = random.randint(30, 55)
        draw.line([(x1, y1), (x2, y2)], fill=(c + 10, c + 25, c + 40), width=1)

    draw.line([(W // 2 - 30, 1180), (W // 2 + 280, 900)], fill=ACCENT, width=3)

    light = lighten_icon(icon)
    logo_w = 160
    logo_h = int(light.height * (logo_w / light.width))
    ir = light.resize((logo_w, logo_h), Image.Resampling.LANCZOS)
    img.paste(ir, ((W - logo_w) // 2, 280), ir)
    center_text(draw, "CEDRIC MILLES", font(INTER_SEMI, 26), 520, (180, 200, 220))

    center_text(draw, "Baja el ruido.", font(INTER_SEMI, 86), 1450, WHITE)
    center_text(draw, "Recupera perspectiva.", font(INTER_MED, 86), 1550, ACCENT)

    y = 1750
    body = (
        "Cuando la presión, las preocupaciones o el estrés ocupan "
        "demasiado espacio, parar y comprender lo que ocurre "
        "puede ayudarte a recuperar dirección."
    )
    for line in wrap_lines(draw, body, font(INTER_REG, 28), W - 2 * MARGIN - 60):
        center_text(draw, line, font(INTER_REG, 28), y, (180, 195, 210))
        y += 44

    center_text(
        draw,
        "Estrés  ·  Presión  ·  Gestión emocional  ·  Equilibrio",
        font(INTER_REG, 22),
        2100,
        PRIMARY,
    )

    y = 2550
    cta = "Reserva una sesión  →"
    cta_f = font(INTER_MED, 32)
    bb = draw.textbbox((0, 0), cta, font=cta_f)
    tw = bb[2] - bb[0]
    tx = (W - tw) // 2
    draw.text((tx, y), cta, font=cta_f, fill=WHITE)
    draw.line([(tx, y + 52), (tx + tw, y + 52)], fill=ACCENT, width=2)

    center_text(
        draw,
        "Psicología · Orientación · Rendimiento",
        font(INTER_REG, 20),
        H - 160,
        (140, 165, 190),
    )
    center_text(draw, "cedricmilles.com", font(INTER_REG, 18), H - 120, (120, 145, 170))
    return img


def main() -> None:
    icon = ensure_isotipo()
    OUT.mkdir(parents=True, exist_ok=True)

    pieces = [
        ("cartel-institucional-cedric-milles.png", cartel_institucional(icon)),
        ("cartel-bienestar-cedric-milles.png", cartel_bienestar(icon)),
        ("cartel-claridad-cedric-milles.png", cartel_claridad(icon)),
    ]
    for name, image in pieces:
        path = OUT / name
        image.save(path, "PNG", dpi=(200, 200))
        print(f"saved {path} ({image.size[0]}x{image.size[1]})")


if __name__ == "__main__":
    main()
