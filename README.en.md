# md2img

[![GitHub release](https://img.shields.io/github/v/release/nicokickcpython/md2img?style=for-the-badge&logo=github&color=black)](https://github.com/nicokickcpython/md2img/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)

**One command to turn Markdown into beautiful multi-template, multi-size PNG images** (long image / card / poster). An open-source lightweight tool that runs locally with no network needed.

Filling the ecosystem gap: existing tools (e.g. doocs/md) only do "md → WeChat rich-text copy", not "md → image file output". md2img directly outputs PNG image files — perfect for sharing to social platforms, embedding in documents, or generating daily reports on schedule.

> ✨ **Doing one thing for the neglected tail of "md → image"**: feed raw Markdown in, get a shareable image out.

## Pipeline

Verified end-to-end:

```
markdown lib → HTML + template CSS → weasyprint → PDF → pypdfium2 render & stitch → PNG
```

- CJK font: WenQuanYi Zen Hei — Chinese renders correctly
- Multi-page content auto-paginates, stitched vertically into a long image; no right/bottom clipping
- Full GFM support: table alignment (left/center/right), footnotes, task lists, nested blockquotes

## Install

Requires Python 3.9+ and system libs (pango, etc. — needed by weasyprint).

```bash
python3 -m venv .venv
.venv/bin/pip install -e .
```

## Usage

```bash
md2img input.md -t daily -s long -o output.png
```

| Option | Values | Default | Description |
| ---- | ------ | ---- | ---- |
| `input.md` | file path | required | Input Markdown file |
| `-t, --template` | `daily` / `card` / `poster` / `minimal` | `daily` | Visual template |
| `-s, --size` | `long` / `1:1` / `3:4` / `9:16` | `long` | Output aspect ratio |
| `-o, --output` | file path | `<input>_<template>_<size>.png` | Output PNG path |

Or use it as a Python library:

```python
import md2img

md2img.convert_text("# Hello world", template="card", size="1:1", output="out.png")
md2img.convert_markdown("input.md", template="poster", size="3:4", output="out.png")
```

## Templates

| Template | Style | Use case |
| ---- | ---- | -------- |
| `daily` | red/white, newspaper-style heading | daily reports, briefings |
| `card` | light background + white rounded cards | social media sharing |
| `poster` | white frame + dark gradient panel, big title | event posters, promo images |
| `minimal` | pure white, black/gray, generous whitespace | formal docs, long-form reading |

## Sizes

| Size | CSS @page size | Description |
| ---- | -------------- | ---- |
| `long` | `764px auto` | Long image, height auto-fits content, multi-page stitched |
| `1:1` | `1080px 1080px` | Square card |
| `3:4` | `810px 1080px` | Portrait card |
| `9:16` | `1080px 1920px` | Mobile portrait long image |

For fixed sizes, content overflowing one page auto-paginates; each page keeps the ratio and is stitched vertically — no clipping.

## Examples

```bash
md2img scripts/sample.md -t daily -s long -o daily_long.png
md2img scripts/sample.md -t card -s 1:1 -o card_1x1.png
md2img scripts/sample.md -t poster -s 3:4 -o poster_3x4.png
md2img scripts/sample.md -t minimal -s 9:16 -o minimal_9x16.png
```

## Verify

```bash
./scripts/verify.sh
```

The script:

1. Runs pytest: 4 templates × 4 sizes = 16 combos, CJK rendering, no right/bottom clipping (pixel-verified), fixed-size ratio correctness
2. Actually generates 16 PNGs via CLI and checks dimensions/ratios

## Structure

```
├── src/md2img/
│   ├── __init__.py
│   ├── cli.py            # CLI entry
│   ├── converter.py      # md → html → pdf → png core
│   └── templates/        # 4 independent CSS templates
│       ├── daily.css
│       ├── card.css
│       ├── poster.css
│       └── minimal.css
├── tests/test_md2img.py  # pytest tests
├── scripts/verify.sh     # one-shot verification
├── scripts/sample.md     # sample input
├── pyproject.toml
└── LICENSE
```

## License

[MIT](LICENSE)
