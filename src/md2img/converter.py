"""Markdown → HTML → PDF → PNG 转换核心。

管线（已验证方案）：
    markdown 库 → HTML 模板/CSS → weasyprint → PDF → pypdfium2 渲染拼接 PNG
"""
from __future__ import annotations

import os
import tempfile
from pathlib import Path

import markdown
from weasyprint import HTML

TEMPLATE_DIR = Path(__file__).parent / "templates"

# 尺寸 → CSS @page size（长图用 auto 高度，其余用固定宽高比例）
SIZES: dict[str, str] = {
    "long": "764px auto",
    "1:1": "1080px 1080px",
    "3:4": "810px 1080px",
    "9:16": "1080px 1920px",
}

TEMPLATES: set[str] = {"daily", "card", "poster", "minimal"}

# PDF 渲染缩放：PDF 1pt = CSS 0.75px，scale=2.0 时输出约为 CSS 尺寸的 1.5 倍
RENDER_SCALE = 2.0

MARKDOWN_EXTENSIONS = ["tables", "fenced_code", "nl2br"]

BASE_CSS = """\
@page {{ size: {page_size}; margin: 0; }}
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; padding: 0; }}
img {{ max-width: 100%; height: auto; }}
table {{ border-collapse: collapse; width: 100%; table-layout: fixed; word-break: break-all; overflow-wrap: break-word; }}
pre {{ white-space: pre-wrap; word-break: break-all; overflow-wrap: anywhere; }}
code {{ font-family: "WenQuanYi Zen Hei Mono", "DejaVu Sans Mono", "Liberation Mono", monospace; }}
a {{ word-break: break-all; }}
"""

HTML_SKELETON = """\
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<style>{base_css}</style>
<style>{template_css}</style>
</head>
<body>
<main class="md2img-content">
{content}
</main>
</body>
</html>
"""


def load_template_css(name: str) -> str:
    """读取模板 CSS 文件内容。"""
    if name not in TEMPLATES:
        raise ValueError(f"未知模板: {name!r}（可选: {', '.join(sorted(TEMPLATES))}）")
    return (TEMPLATE_DIR / f"{name}.css").read_text(encoding="utf-8")


def markdown_to_html(text: str, template: str = "daily", size: str = "long") -> str:
    """Markdown 文本 → 完整 HTML 文档（含模板 CSS 与尺寸 @page）。"""
    if size not in SIZES:
        raise ValueError(f"未知尺寸: {size!r}（可选: {', '.join(sorted(SIZES))}）")
    body = markdown.markdown(text, extensions=MARKDOWN_EXTENSIONS)
    return HTML_SKELETON.format(
        base_css=BASE_CSS.format(page_size=SIZES[size]),
        template_css=load_template_css(template),
        content=body,
    )


def pdf_to_png(pdf_path: str, output_path: str, scale: float = RENDER_SCALE, size: str = "long") -> tuple[int, int, int]:
    """PDF 各页渲染为 PNG，多页纵向拼接成长图。返回 (页数, 宽, 高)。"""
    import pypdfium2 as pdfium
    from PIL import Image

    pdf = pdfium.PdfDocument(pdf_path)
    pages = [page.render(scale=scale).to_pil().convert("RGB") for page in pdf]
    if not pages:
        raise RuntimeError("PDF 无页面")
    if len(pages) == 1:
        pages[0].save(output_path)
    else:
        width = max(p.width for p in pages)
        total_height = sum(p.height for p in pages)
        canvas = Image.new("RGB", (width, total_height), "white")
        y = 0
        for page in pages:
            canvas.paste(page, (0, y))
            y += page.height
        # 仅 long 模式：裁剪底部空白（内容像素探测）；固定尺寸模式保持原样
        bg = (255, 255, 255)
        h = canvas.height
        if size == "long":
            threshold = max(2, int(width * 0.003))
            def row_has_content(yy):
                row = list(canvas.crop((0, yy, width, yy + 1)).getdata())
                cnt = sum(1 for p in row if p != bg)
                return cnt >= threshold
            # 从底部向上 1px 步长，找最后一行内容（长图高度有限，直接精确扫）
            last_content = -1
            yy = h - 1
            while yy > 0:
                if row_has_content(yy):
                    last_content = yy
                    break
                yy -= 1
            if last_content == -1:
                last_content = 0
            # 底部留 60px 边距（防贴边误判截断）
            bottom = min(last_content + 60, h)
            canvas = canvas.crop((0, 0, width, bottom))
        canvas.save(output_path)
    return len(pages), pages[0].width, sum(p.height for p in pages)


def convert_text(
    text: str,
    template: str = "daily",
    size: str = "long",
    output: str | Path | None = None,
) -> dict:
    """Markdown 文本 → PNG 图片。返回生成信息（页数/宽/高）。"""
    if output is None:
        raise ValueError("必须提供 output 路径")
    html = markdown_to_html(text, template=template, size=size)
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    fd, pdf_path = tempfile.mkstemp(suffix=".pdf")
    os.close(fd)
    try:
        HTML(string=html).write_pdf(pdf_path)
        pages, width, height = pdf_to_png(pdf_path, str(output), size=size)
    finally:
        try:
            os.unlink(pdf_path)
        except OSError:
            pass
    return {"pages": pages, "width": width, "height": height, "output": str(output)}


def default_output_name(source: str, template: str, size: str) -> str:
    """默认输出名：<输入名>_<模板>_<尺寸>.png。"""
    stem = Path(source).name
    for suffix in Path(source).suffixes:
        stem = stem.removesuffix(suffix)
    return f"{stem}_{template}_{size}.png"


def convert_markdown(
    source: str | Path,
    template: str = "daily",
    size: str = "long",
    output: str | Path | None = None,
) -> dict:
    """Markdown 文件 → PNG 图片。返回生成信息（页数/宽/高）。"""
    text = Path(source).read_text(encoding="utf-8")
    if output is None:
        output = default_output_name(str(source), template, size)
    return convert_text(text, template=template, size=size, output=output)
