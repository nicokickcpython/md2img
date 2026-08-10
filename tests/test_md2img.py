"""md2img 测试：4 模板 × 4 尺寸 = 16 组合生成 + 中文渲染 + 无截断像素验证。"""
from pathlib import Path

import pytest
from PIL import Image

import md2img
from md2img import convert_markdown, convert_text, markdown_to_html

FILLER = (
    "这是一段用于撑高页面、验证多页分页与拼接逻辑的占位文字。"
    "它同时包含中文、英文 mixed content 与数字 12345，用于检查换行与自动分页。"
)

SAMPLE = f"""# md2img 工具介绍

md2img 是一条命令把 **Markdown** 转成精美图片的小工具，支持多种模板与尺寸。

> 中文字体使用文泉驿正黑（WenQuanYi Zen Hei），确保中文渲染正常，不会出现乱码或截断。

## 功能特性

- 四种模板：日报 / 卡片 / 海报 / 简洁
- 四种尺寸：长图 / 1:1 / 3:4 / 9:16
- 命令行调用，支持脚本集成与 cron 定时生成

### 表格示例

| 模板 | 尺寸 | 适合场景 |
| ---- | ---- | -------- |
| daily | long | 资讯日报 |
| card | 1:1 | 社交分享 |
| poster | 3:4 | 活动海报 |
| minimal | 9:16 | 手机长图 |

## 代码示例

```python
import md2img
info = md2img.convert_text("# 你好，世界", template="daily", size="long", output="out.png")
print(info)
```

## 引用与列表

1. 第一项：安装依赖
2. 第二项：运行命令
3. 第三项：验证输出

{FILLER * 40}
"""


def _strip_clean(strip: Image.Image, threshold: int = 235) -> bool:
    r, g, b = strip.convert("RGB").split()
    return min(ch.getextrema()[0] for ch in (r, g, b)) >= threshold


def _has_no_clipping(img: Image.Image, strip: int = 10) -> bool:
    """右侧/底部边框 strip 像素均为背景色（≥235），说明内容未被截断到边缘。"""
    w, h = img.size
    right = img.crop((w - strip, 0, w, h))
    bottom = img.crop((0, h - strip, w, h))
    return _strip_clean(right) and _strip_clean(bottom)


@pytest.mark.parametrize("size", sorted(md2img.SIZES))
@pytest.mark.parametrize("template", sorted(md2img.TEMPLATES))
def test_all_combos(tmp_path, template, size):
    md = tmp_path / "input.md"
    md.write_text(SAMPLE, encoding="utf-8")
    out = tmp_path / f"{template}_{size}.png"
    info = convert_markdown(str(md), template=template, size=size, output=str(out))

    assert out.exists(), "输出 PNG 未生成"
    assert info["pages"] >= 1
    img = Image.open(out)
    img.load()
    w, h = img.size
    assert w > 100 and h > 100, f"图片尺寸异常: {w}x{h}"
    assert _has_no_clipping(img), f"{template}/{size}: 右侧或底部存在截断"

    expected = {"1:1": 1.0, "3:4": 3 / 4, "9:16": 9 / 16}.get(size)
    if expected is not None:
        # 多页纵向拼接：整图比例 = 单页比例 / 页数（每页保持指定比例）
        total = w / h
        assert abs(total * info["pages"] - expected) < 0.02, (
            f"{template}/{size}: 单页比例 {total * info['pages']:.4f} != {expected} (页数={info['pages']})"
        )


def test_chinese_renders(tmp_path):
    md = tmp_path / "chinese.md"
    md.write_text(
        "# 你好，世界！\n\n"
        "这是一段中文内容：文泉驿正黑，中文字体渲染正常。\n\n"
        "## 二级标题\n\n- 列表项一\n- 列表项二\n",
        encoding="utf-8",
    )
    out = tmp_path / "chinese.png"
    convert_markdown(str(md), template="daily", size="long", output=str(out))
    gray = Image.open(out).convert("L")
    dark = sum(gray.histogram()[:100])
    assert dark > 1500, f"深色文字像素过少: {dark}，中文可能未正常渲染"


def test_long_size_is_tall(tmp_path):
    md = tmp_path / "long.md"
    md.write_text("# 标题\n\n" + FILLER * 120, encoding="utf-8")
    out = tmp_path / "long.png"
    info = convert_markdown(str(md), template="daily", size="long", output=str(out))
    assert info["height"] > info["width"] * 3, "长图高度应明显大于宽度"
    assert _has_no_clipping(Image.open(out))


def test_cli_default_output(tmp_path, capsys, monkeypatch):
    from md2img import cli

    monkeypatch.chdir(tmp_path)
    md = tmp_path / "a.md"
    md.write_text("# Hi\n\n你好，世界。\n", encoding="utf-8")
    code = cli.main([str(md), "-t", "minimal", "-s", "1:1"])
    out = tmp_path / "a_minimal_1:1.png"
    assert code == 0
    assert out.exists()
    assert "已生成" in capsys.readouterr().out


def test_markdown_to_html_contains_css():
    html = markdown_to_html("# 标题\n", template="card", size="3:4")
    assert "810px 1080px" in html  # @page size
    assert "card" in html and "md2img-content" in html


def test_convert_text(tmp_path):
    out = tmp_path / "t.png"
    info = convert_text("# 测试\n\n内容。\n", template="poster", size="1:1", output=str(out))
    assert out.exists() and info["pages"] >= 1


def test_templates_visually_distinct(tmp_path):
    """4 套模板视觉差异明显：poster 为深色面板，daily 为白底，且两者渲染不同。"""
    from PIL import ImageChops

    def _dark_ratio(path):
        hist = Image.open(path).convert("L").histogram()
        return sum(hist[:60]) / sum(hist)

    daily = tmp_path / "daily.png"
    poster = tmp_path / "poster.png"
    convert_text(SAMPLE, template="daily", size="long", output=str(daily))
    convert_text(SAMPLE, template="poster", size="long", output=str(poster))

    ratio_daily, ratio_poster = _dark_ratio(daily), _dark_ratio(poster)
    assert ratio_daily < 0.15, f"daily 暗像素占比过高: {ratio_daily:.1%}"
    assert ratio_poster > 0.25, f"poster 深色面板未生效: {ratio_poster:.1%}"
    diff = ImageChops.difference(Image.open(daily).convert("RGB"), Image.open(poster).convert("RGB"))
    assert diff.getbbox() is not None, "daily 与 poster 渲染完全相同"
