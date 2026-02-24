# POD Design Generator

A Python CLI tool that generates print-on-demand designs for Redbubble. Zero cost — uses only Pillow and free Google Fonts to produce upload-ready PNG images with metadata.

## Features

- **Text designs** — quotes and slogans with auto-sized typography
- **Pattern designs** — geometric, circles, triangles, grid, and tessellation patterns (seeded for reproducibility)
- **Niche templates** — 14 themed categories with 700 pre-written phrases
- **3 layouts** — centered, stacked multi-line, and arced/curved text
- **3 product targets** — t-shirt (2875x3900), sticker (2800x2800), poster (3840x3840)
- **Metadata generation** — title, description, and up to 15 tags per design
- **Batch mode** — generate hundreds of designs from a single JSON config

## Quick Start

```bash
# Install dependency
pip install Pillow

# Download fonts (one-time)
python3 setup_fonts.py

# Generate a text design
python3 generate.py text "DREAM BIG" --font anton --colors white-on-black --products tshirt,sticker,poster

# Generate all 700 template designs
python3 generate_all.py
```

## CLI Usage

### Text Design

```bash
python3 generate.py text "HUSTLE HARDER" --font bebas --colors gold-on-black --layout stacked --products tshirt,sticker
```

Options:
- `--font` / `-f` — Font name: `anton`, `bebas`, `russo`, `pacifico`, `caveat`, `shadows`, `patrick`
- `--colors` / `-c` — Color shortcut: `white-on-black`, `neon-on-dark`, `gold-on-black`, `pink-on-dark`, `cyan-on-dark`, `red-on-black`, `sunset`
- `--palette` — Color palette: `warm`, `cool`, `neon`, `pastel`, `earth`
- `--layout` / `-l` — Layout: `centered`, `stacked`, `arced`
- `--products` / `-p` — Comma-separated: `tshirt`, `sticker`, `poster`
- `--no-shadow` — Disable drop shadow
- `--filename` — Custom output filename

### Pattern Design

```bash
python3 generate.py pattern --style geometric --palette neon --seed 42 --products poster
```

Options:
- `--style` / `-s` — Style: `geometric`, `circles`, `triangles`, `grid`, `tessellation`
- `--palette` — Color palette: `warm`, `cool`, `neon`, `pastel`, `earth`
- `--seed` — Random seed for reproducible output

### Niche Template Design

```bash
python3 generate.py niche --theme funny --text "Hold on let me overthink this" --products tshirt
```

Options:
- `--theme` / `-t` — Theme name (see available themes below)
- `--text` — Custom text (omit for random phrase from theme)

### Batch Generation

```bash
python3 generate.py batch --config batch_examples/batch_example.json
```

### Generate All Templates

```bash
python3 generate_all.py
```

Generates every phrase from every template across all 3 products (~2,100 images).

## Available Themes

| Theme | Phrases | Font | Colors |
|-------|---------|------|--------|
| `motivational` | 50 | Anton | White on black |
| `funny` | 50 | Patrick Hand | Neon on dark |
| `profession` | 50 | Bebas Neue | Gold on black |
| `hobby` | 50 | Pacifico | Pink on dark |
| `gaming` | 50 | Russo One | Neon on dark |
| `fitness` | 50 | Anton | Red on black |
| `mom` | 50 | Pacifico | Pink on dark |
| `dad` | 50 | Bebas Neue | Gold on black |
| `pets` | 50 | Patrick Hand | Gold on black |
| `coffee` | 50 | Caveat | Gold on black |
| `introvert` | 50 | Shadows Into Light | Cyan on dark |
| `sarcasm` | 51 | Bebas Neue | Red on black |
| `seasonal` | 50 | Pacifico | Gold on black |
| `drinking` | 50 | Patrick Hand | Gold on black |

## Product Specs

| Product | Dimensions | Format |
|---------|-----------|--------|
| T-Shirt | 2875 x 3900 | RGBA (transparent) |
| Sticker | 2800 x 2800 | RGBA (transparent) |
| Poster | 3840 x 3840 | RGB (solid background) |

## Fonts

7 free Google Fonts downloaded via `setup_fonts.py`:

- **Bold**: Russo One, Anton, Bebas Neue
- **Script**: Pacifico, Caveat, Shadows Into Light
- **Clean**: Patrick Hand

All fonts are OFL-licensed for free commercial use.

## Project Structure

```
pod-design-generator/
├── generate.py              # CLI entry point
├── generate_all.py          # Bulk generate all templates
├── setup_fonts.py           # Downloads Google Fonts
├── requirements.txt         # Pillow
├── src/
│   ├── config.py            # Product specs & constants
│   ├── canvas.py            # Canvas creation & saving
│   ├── fonts.py             # Font loading & caching
│   ├── colors.py            # Palettes & color parsing
│   ├── metadata.py          # Title/tags/description
│   ├── batch.py             # Batch JSON processing
│   ├── generators/
│   │   ├── base.py          # Abstract base generator
│   │   ├── text_design.py   # Text/quote designs
│   │   ├── pattern_design.py # Geometric patterns
│   │   └── niche_design.py  # Themed templates
│   ├── layouts/
│   │   ├── centered.py      # Auto-sized centered text
│   │   ├── stacked.py       # Multi-line stacked
│   │   └── arced.py         # Curved text along arc
│   └── effects/
│       ├── shadow.py        # Drop shadow
│       ├── gradient.py      # Linear/radial gradients
│       └── shapes.py        # Shape primitives
├── fonts/                   # Downloaded .ttf files (gitignored)
├── templates/               # Niche theme JSON configs
├── batch_examples/          # Example batch configs
└── output/                  # Generated designs (gitignored)
```

## Adding Custom Templates

Create a JSON file in `templates/`:

```json
{
  "category": "your-niche",
  "description": "Description of the theme",
  "style": {
    "font": "anton",
    "colors": "white-on-black",
    "layout": "stacked",
    "shadow": true
  },
  "phrases": [
    "YOUR TEXT\nHERE",
    "ANOTHER\nPHRASE"
  ],
  "tags": ["tag1", "tag2", "tag3"]
}
```

Then generate with:

```bash
python3 generate.py niche --theme your-niche --products tshirt,sticker,poster
```

## License

Fonts are licensed under the [SIL Open Font License](https://scripts.sil.org/OFL). Code is free to use.
