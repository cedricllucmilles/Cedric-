#!/usr/bin/env python3
"""Cartel A3 para colegios (estilo foto + QR servicios)."""

from __future__ import annotations

import os
from pathlib import Path

import qrcode
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
OUT = Path(__file__).resolve().parent

SERVICIOS_URL = "https://cedricmilles.com/es/servicios/"
W, H = 2480, 3508
CREAM = (249, 239, 222)
NAVY = (6, 43, 85)
PRIMARY = (49, 95, 141)
ACCENT = (74, 139, 199)
GRAY = (90, 100, 112)
GRAY2 = (115, 125, 138)
WHITE = (255, 255, 255)
CARD = (255, 252, 248)

INTER_REG = "/usr/share/fonts/truetype/macos/Inter-Regular.ttf"
INTER_MED = "/usr/share/fonts/truetype/macos/Inter-Medium.ttf"
INTER_SEMI = "/usr/share/fonts/truetype/macos/Inter-SemiBold.ttf"
INTER_BOLD = "/usr/share/fonts/truetype/macos/Inter-Bold.ttf"


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def make_qr(url: str, size: int = 340) -> Image.Image:
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=12, border=2)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="rgb(6,43,85)", back_color="white").convert("RGB")
    return img.resize((size, size), Image.Resampling.NEAREST)


def main() -> None:
    qr_size = 340
    qr_img = make_qr(SERVICIOS_URL, qr_size)
    qr_img.save(ASSETS / "qr-cedric-servicios.png")

    icon = Image.open(ASSETS / "isotipo.png").convert("RGBA")
    photo_path = ASSETS / "foto-colegios-original-cedric.jpg"
    photo = Image.open(photo_path).convert("RGB")

    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)
    m = 140

    for y in range(0, 1320):
        t = y / 1320
        draw.line([(0, y), (W, y)], fill=(int(251 - 2 * t), int(242 - 3 * t), int(225 - 3 * t)))

    logo_w = 122
    logo_h = int(icon.height * (logo_w / icon.width))
    icon_r = icon.resize((logo_w, logo_h), Image.Resampling.LANCZOS)
    ly = 105
    img.paste(icon_r, (m, ly), icon_r)
    draw.text((m + logo_w + 30, ly + 12), "Cedric Milles", font=font(INTER_SEMI, 52), fill=NAVY)
    draw.text(
        (m + logo_w + 30, ly + 78),
        "Psicología · Orientación · Rendimiento",
        font=font(INTER_REG, 25),
        fill=PRIMARY,
    )

    badge = "PARA COLEGIOS"
    bf = font(INTER_SEMI, 22)
    bbb = draw.textbbox((0, 0), badge, font=bf)
    bw, bh = bbb[2] - bbb[0] + 48, bbb[3] - bbb[1] + 28
    bx = W - m - bw
    by = ly + 18
    draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=14, fill=ACCENT)
    draw.text((bx + 24, by + 12), badge, font=bf, fill=WHITE)

    cat = "ACOMPAÑAMIENTO PSICOLÓGICO EN CENTROS EDUCATIVOS"
    y = 300
    draw.text((m, y), cat, font=font(INTER_SEMI, 27), fill=NAVY)
    bb = draw.textbbox((m, y), cat, font=font(INTER_SEMI, 27))
    draw.line([(m, bb[3] + 12), (bb[2], bb[3] + 12)], fill=NAVY, width=3)

    y = 395
    for line in ["En el colegio también", "se aprende a entenderse."]:
        draw.text((m, y), line, font=font(INTER_BOLD, 84), fill=NAVY)
        y += 98
    y += 12
    for line in [
        "Apoyo para alumnado, familias y equipos docentes:",
        "bienestar emocional, orientación y hábitos de estudio.",
    ]:
        draw.text((m, y), line, font=font(INTER_REG, 34), fill=GRAY)
        y += 48

    y += 10
    for row in (
        ["Tutorías con familias", "Gestión emocional", "Motivación y organización"],
        ["Convivencia en el aula", "Orientación en cambios de etapa"],
    ):
        x = m
        for d in row:
            t = f"·  {d}"
            draw.text((x, y), t, font=font(INTER_MED, 23), fill=PRIMARY)
            x = draw.textbbox((x, y), t, font=font(INTER_MED, 23))[2] + 32
        y += 38

    footer_h = 560
    photo_top = 1180
    photo_bottom = H - footer_h
    photo_h = photo_bottom - photo_top
    pw, ph = photo.size
    scale = max(W / pw, photo_h / ph)
    nw, nh = int(pw * scale), int(ph * scale)
    photo_r = photo.resize((nw, nh), Image.Resampling.LANCZOS)
    left = (nw - W) // 2
    top = max(0, (nh - photo_h) // 2)
    photo_c = photo_r.crop((left, top, left + W, top + photo_h))
    photo_c = ImageEnhance.Color(photo_c).enhance(1.06)
    photo_c = ImageEnhance.Contrast(photo_c).enhance(1.04)
    img.paste(photo_c, (0, photo_top))
    for i in range(110):
        a = 1 - (i / 110)
        yy = photo_top + i
        row = img.crop((0, yy, W, yy + 1))
        img.paste(Image.blend(row, Image.new("RGB", (W, 1), CREAM), a * 0.58), (0, yy))

    draw = ImageDraw.Draw(img)
    card_x, card_y, card_w, card_h = 110, 930, W - 220, 320
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle(
        [card_x + 10, card_y + 16, card_x + card_w + 10, card_y + card_h + 16],
        radius=26,
        fill=(0, 0, 0, 42),
    )
    img = Image.alpha_composite(img.convert("RGBA"), shadow.filter(ImageFilter.GaussianBlur(16))).convert("RGB")
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle(
        [card_x, card_y, card_x + card_w, card_y + card_h],
        radius=26,
        fill=CARD,
        outline=(225, 215, 205),
        width=2,
    )

    cols = [
        ("BIENESTAR EMOCIONAL", "Autoestima, emociones\ny convivencia en el aula.", "Ansiedad · Conflicto · Autoestima"),
        ("FAMILIAS Y TUTORÍAS", "Acompañamiento a madres,\npadres y reuniones escolares.", "Comunicación · Límites · Cambios"),
        ("RENDIMIENTO Y HÁBITOS", "Motivación, organización\ny objetivos alcanzables.", "Estudio · Deporte · Decisiones"),
    ]
    col_w = card_w // 3
    for i, (title, body, tags) in enumerate(cols):
        cx = card_x + i * col_w
        if i > 0:
            draw.line([(cx, card_y + 48), (cx, card_y + card_h - 48)], fill=(212, 202, 190), width=2)
        tw = draw.textbbox((0, 0), title, font=font(INTER_SEMI, 25))[2]
        draw.text((cx + (col_w - tw) // 2, card_y + 52), title, font=font(INTER_SEMI, 25), fill=NAVY)
        by = card_y + 108
        for line in body.split("\n"):
            lw = draw.textbbox((0, 0), line, font=font(INTER_REG, 24))[2]
            draw.text((cx + (col_w - lw) // 2, by), line, font=font(INTER_REG, 24), fill=GRAY)
            by += 34
        tw = draw.textbbox((0, 0), tags, font=font(INTER_REG, 18))[2]
        draw.text((cx + (col_w - tw) // 2, card_y + card_h - 58), tags, font=font(INTER_REG, 18), fill=GRAY2)

    framework = "COMPRENDER  ·  DECIDIR  ·  AVANZAR"
    ff = font(INTER_SEMI, 28)
    fw = draw.textbbox((0, 0), framework, font=ff)[2]
    draw.rectangle([0, photo_bottom - 88, W, photo_bottom], fill=NAVY)
    draw.text(((W - fw) // 2, photo_bottom - 68), framework, font=ff, fill=WHITE)

    footer_y = H - footer_h
    draw.rectangle([0, footer_y, W, H], fill=NAVY)
    qr_pad = 24
    qr_x = m + 20
    qr_y = footer_y + 95
    draw.rounded_rectangle(
        [qr_x - qr_pad, qr_y - qr_pad, qr_x + qr_size + qr_pad, qr_y + qr_size + qr_pad],
        radius=16,
        fill=WHITE,
    )
    img.paste(qr_img, (qr_x, qr_y))
    ql = qr_x + qr_size + qr_pad + 36
    draw.text((ql, footer_y + 110), "Escanea para ver servicios", font=font(INTER_SEMI, 36), fill=WHITE)
    draw.text((ql, footer_y + 168), "cedricmilles.com/es/servicios/", font=font(INTER_MED, 28), fill=(180, 210, 235))
    draw.text(
        (ql, footer_y + 220),
        "Psicología · orientación · rendimiento para el entorno escolar.",
        font=font(INTER_REG, 24),
        fill=(190, 210, 225),
    )

    cta_x = W - m - 680
    cta_y = footer_y + 108
    for i, line in enumerate(["Un espacio para escuchar,", "comprender y avanzar."]):
        draw.text((cta_x, cta_y + i * 52), line, font=font(INTER_SEMI, 40), fill=WHITE)

    info = "Información y primera toma de contacto"
    iw = draw.textbbox((0, 0), info, font=font(INTER_REG, 24))[2]
    line_y = footer_y + 390
    draw.text(((W - iw) // 2, line_y - 42), info, font=font(INTER_REG, 24), fill=(190, 210, 225))
    draw.line([(m, line_y), (W - m, line_y)], fill=(80, 110, 145), width=2)
    contact = "cedricmilles.com   ·   cedricluc.milles@gmail.com   ·   @Cedric_milles"
    cw = draw.textbbox((0, 0), contact, font=font(INTER_MED, 24))[2]
    draw.text(((W - cw) // 2, line_y + 28), contact, font=font(INTER_MED, 24), fill=WHITE)

    out_png = OUT / "cartel-colegios-servicios-qr.png"
    out_jpg = OUT / "cartel-colegios-servicios-qr.jpg"
    img.save(out_png, "PNG", dpi=(300, 300))
    img.save(out_jpg, "JPEG", quality=93, dpi=(300, 300))
    print(f"saved {out_png} ({os.path.getsize(out_png)} bytes)")


if __name__ == "__main__":
    main()
