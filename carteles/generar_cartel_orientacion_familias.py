#!/usr/bin/env python3
"""Cartel A3 familias (estilo cream + foto original, sin usar referencias externas)."""

from __future__ import annotations

import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
OUT = Path(__file__).resolve().parent

W, H = 2480, 3508
CREAM = (249, 239, 222)
NAVY = (6, 43, 85)
PRIMARY = (49, 95, 141)
GRAY = (90, 100, 112)
WHITE = (255, 255, 255)
CARD = (255, 252, 248)

INTER_REG = "/usr/share/fonts/truetype/macos/Inter-Regular.ttf"
INTER_MED = "/usr/share/fonts/truetype/macos/Inter-Medium.ttf"
INTER_SEMI = "/usr/share/fonts/truetype/macos/Inter-SemiBold.ttf"
INTER_BOLD = "/usr/share/fonts/truetype/macos/Inter-Bold.ttf"


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def paste_cover_photo(
    canvas: Image.Image,
    photo: Image.Image,
    y0: int,
    y1: int,
    fade_from: tuple[int, int, int] = CREAM,
) -> None:
    band_h = y1 - y0
    pw, ph = photo.size
    scale = max(W / pw, band_h / ph)
    nw, nh = int(pw * scale), int(ph * scale)
    resized = photo.resize((nw, nh), Image.Resampling.LANCZOS)
    left = (nw - W) // 2
    top = max(0, (nh - band_h) // 2)
    crop = resized.crop((left, top, left + W, top + band_h))
    crop = ImageEnhance.Color(crop).enhance(1.05)
    crop = ImageEnhance.Contrast(crop).enhance(1.03)
    canvas.paste(crop, (0, y0))
    for i in range(100):
        a = 1 - (i / 100)
        y = y0 + i
        row = canvas.crop((0, y, W, y + 1))
        canvas.paste(Image.blend(row, Image.new("RGB", (W, 1), fade_from), a * 0.55), (0, y))


def main() -> None:
    icon = Image.open(ASSETS / "isotipo.png").convert("RGBA")
    photo = Image.open(ASSETS / "foto-familias-original-cedric.jpg").convert("RGB")

    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)
    m = 140

    for y in range(0, 1280):
        t = y / 1280
        draw.line([(0, y), (W, y)], fill=(int(251 - 2 * t), int(242 - 3 * t), int(225 - 3 * t)))

    logo_w = 118
    logo_h = int(icon.height * (logo_w / icon.width))
    icon_r = icon.resize((logo_w, logo_h), Image.Resampling.LANCZOS)
    ly = 110
    img.paste(icon_r, (m, ly), icon_r)
    draw.text((m + logo_w + 28, ly + 14), "Cedric Milles", font=font(INTER_SEMI, 50), fill=NAVY)
    draw.text(
        (m + logo_w + 28, ly + 76),
        "Psicología · Orientación · Rendimiento",
        font=font(INTER_REG, 24),
        fill=PRIMARY,
    )

    cat = "ORIENTACIÓN PSICOLÓGICA PARA NIÑOS, ADOLESCENTES Y FAMILIAS"
    y = 310
    draw.text((m, y), cat, font=font(INTER_SEMI, 26), fill=NAVY)
    bb = draw.textbbox((m, y), cat, font=font(INTER_SEMI, 26))
    draw.line([(m, bb[3] + 10), (bb[2], bb[3] + 10)], fill=NAVY, width=3)

    y = 410
    for line in ["Crecer también es", "aprender a entenderse."]:
        draw.text((m, y), line, font=font(INTER_BOLD, 82), fill=NAVY)
        y += 96

    y += 18
    for line in [
        "Un espacio cercano para acompañar el bienestar emocional,",
        "la confianza y los retos del día a día.",
    ]:
        draw.text((m, y), line, font=font(INTER_REG, 34), fill=GRAY)
        y += 48

    footer_h = 500
    photo_top = 1140
    photo_bottom = H - footer_h
    paste_cover_photo(img, photo, photo_top, photo_bottom)

    draw = ImageDraw.Draw(img)
    card_x, card_y, card_w, card_h = 130, 940, W - 260, 280
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle(
        [card_x + 8, card_y + 14, card_x + card_w + 8, card_y + card_h + 14],
        radius=24,
        fill=(0, 0, 0, 38),
    )
    img = Image.alpha_composite(img.convert("RGBA"), shadow.filter(ImageFilter.GaussianBlur(14))).convert("RGB")
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([card_x, card_y, card_x + card_w, card_y + card_h], radius=24, fill=CARD)

    cols = [
        ("EMOCIONES Y AUTOESTIMA", "Identificar, expresar\ny gestionar emociones."),
        ("RELACIONES Y CAMBIOS", "Familia, amistades,\netapas y convivencia."),
        ("HÁBITOS Y ESTUDIO", "Motivación, organización\ny objetivos realistas."),
    ]
    col_w = card_w // 3
    for i, (title, body) in enumerate(cols):
        cx = card_x + i * col_w
        if i > 0:
            draw.line([(cx, card_y + 40), (cx, card_y + card_h - 40)], fill=(210, 200, 190), width=2)
        tw = draw.textbbox((0, 0), title, font=font(INTER_SEMI, 26))[2]
        draw.text((cx + (col_w - tw) // 2, card_y + 56), title, font=font(INTER_SEMI, 26), fill=NAVY)
        by = card_y + 118
        for line in body.split("\n"):
            lw = draw.textbbox((0, 0), line, font=font(INTER_REG, 25))[2]
            draw.text((cx + (col_w - lw) // 2, by), line, font=font(INTER_REG, 25), fill=GRAY)
            by += 36

    footer_y = H - footer_h
    draw.rectangle([0, footer_y, W, H], fill=NAVY)

    cta = "Un espacio para escuchar, comprender y avanzar."
    cta_f = font(INTER_SEMI, 46)
    cw = draw.textbbox((0, 0), cta, font=cta_f)[2]
    draw.text(((W - cw) // 2, footer_y + 100), cta, font=cta_f, fill=WHITE)

    line_y = footer_y + 195
    draw.line([(W // 2 - 280, line_y), (W // 2 + 280, line_y)], fill=(120, 150, 180), width=2)
    info = "Información y primera toma de contacto"
    iw = draw.textbbox((0, 0), info, font=font(INTER_REG, 26))[2]
    draw.text(((W - iw) // 2, line_y + 28), info, font=font(INTER_REG, 26), fill=(190, 210, 225))

    contact = "cedricmilles.com   ·   cedricluc.milles@gmail.com   ·   @Cedric_milles"
    cw = draw.textbbox((0, 0), contact, font=font(INTER_MED, 24))[2]
    draw.text(((W - cw) // 2, footer_y + 300), contact, font=font(INTER_MED, 24), fill=WHITE)

    out_png = OUT / "cartel-orientacion-familias.png"
    out_jpg = OUT / "cartel-orientacion-familias.jpg"
    img.save(out_png, "PNG", dpi=(300, 300))
    img.save(out_jpg, "JPEG", quality=93, dpi=(300, 300))
    print(f"saved {out_png} ({os.path.getsize(out_png)} bytes)")


if __name__ == "__main__":
    main()
