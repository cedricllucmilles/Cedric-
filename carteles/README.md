# Carteles Cedric Milles

Carteles publicitarios alineados con `Material Corporativo` (concepto de brújula, paleta oficial y tono editorial).

## Archivos

| Archivo | Enfoque | Mensaje |
|---|---|---|
| `cartel-institucional-cedric-milles.png` | Corporativo / editorial | Psicología para comprender · Orientación para decidir · Rendimiento para avanzar |
| `cartel-bienestar-cedric-milles.png` | Bienestar y crecimiento | No necesitas tenerlo todo claro para empezar a avanzar |
| `cartel-claridad-cedric-milles.png` | Ansiedad, estrés y sobrecarga | Baja el ruido. Recupera perspectiva |
| `cartel-escolar-familias-ninos.png` | Colegios · familias | Crecéis juntos: comprender, decidir y avanzar |
| `cartel-escolar-ninos.png` | Colegios · infancia | No hace falta tenerlo todo claro para empezar a avanzar |
| `cartel-colegios-mapa-qr.png` | Colegios · ilustrado | Mapa/brújula + QR servicios (recomendado) |
| `cartel-colegios-paneles-qr.png` | Colegios · paneles | Tres columnas niños/familias + QR |
| `cartel-colegios-servicios-qr.png` | (legacy) | Plantilla tipo foto+cream — sustituida por mapa/paneles |
| `cartel-orientacion-familias.png` | Familias · foto | Crecer también es aprender a entenderse |

## Especificaciones

- Formato: A3 vertical (297 × 420 mm) a 200 dpi → 2339 × 3307 px
- Paleta: `#092D4A` · `#315F8D` · `#4A8BC7` · `#53616F` · `#FFFFFF`
- Tipografía: Inter (Medium / Semibold / Regular)
- Vista previa: abre `index.html` en el navegador (también sirve para imprimir)

## Regenerar

```bash
python3 carteles/generar_carteles.py
python3 carteles/generar_cartel_colegios_qr.py
python3 carteles/generar_cartel_orientacion_familias.py
python3 carteles/generar_cartel_colegios_visual.py
```

Requisito QR: `pip install qrcode[pil]`

Fotografías del cartel cream/foto: `assets/foto-colegios-original-cedric.jpg` y
`assets/foto-familias-original-cedric.jpg` (generadas para el proyecto, no recortes
de la referencia externa).
