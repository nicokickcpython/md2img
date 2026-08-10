# md2img

[![GitHub release](https://img.shields.io/github/v/release/nicokickcpython/md2img?style=for-the-badge&logo=github&color=black)](https://github.com/nicokickcpython/md2img/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)

**一条命令把 Markdown 转成多模板、多尺寸的精美 PNG 图片**（长图/卡片/海报）。开源小工具，本地运行，无需联网。

填补生态空白：现有工具（如 doocs/md 等）只做"md → 微信富文本复制"，不做"md → 图片文件输出"。md2img 直接输出 PNG 图片文件，方便分享到社交平台、插入文档、定时生成日报。

> ✨ **正在为"md → 图片"这个被忽略的尾巴做一件事**：输入原始 Markdown，输出可直接分享的精美图片。

## 技术方案

已验证跑通管线：

```
markdown 库 → HTML + 模板 CSS → weasyprint → PDF → pypdfium2 渲染拼接 → PNG
```

- 中文字体：文泉驿正黑（WenQuanYi Zen Hei），中文渲染正常
- 多页内容自动分页，纵向拼接成长图，右侧/底部不截断
- 表格对齐（左/中/右）、脚注、任务列表、嵌套引用等 GFM 语法完整支持

## 安装

依赖 Python 3.9+ 与系统库（pango 等，weasyprint 需要）。

```bash
python3 -m venv .venv
.venv/bin/pip install -e .
```

## 用法

```bash
md2img input.md -t daily -s long -o output.png
```

参数说明：

| 参数 | 可选值 | 默认 | 说明 |
| ---- | ------ | ---- | ---- |
| `input.md` | 文件路径 | 必填 | 输入 Markdown 文件 |
| `-t, --template` | `daily` / `card` / `poster` / `minimal` | `daily` | 视觉模板 |
| `-s, --size` | `long` / `1:1` / `3:4` / `9:16` | `long` | 输出尺寸比例 |
| `-o, --output` | 文件路径 | `<输入名>_<模板>_<尺寸>.png` | 输出 PNG 路径 |

也可以作为 Python 库调用：

```python
import md2img

md2img.convert_text("# 你好，世界", template="card", size="1:1", output="out.png")
md2img.convert_markdown("input.md", template="poster", size="3:4", output="out.png")
```

## 模板

| 模板 | 风格 | 适合场景 |
| ---- | ---- | -------- |
| `daily` | 红白配色、报头式标题 | 资讯日报、简报 |
| `card` | 浅色底 + 白色圆角卡片 | 社交平台分享 |
| `poster` | 白框 + 深色渐变面板、大标题 | 活动海报、宣传图 |
| `minimal` | 纯白、黑白灰、留白充分 | 正式文档、长文阅读 |

## 尺寸

| 尺寸 | CSS @page size | 说明 |
| ---- | -------------- | ---- |
| `long` | `764px auto` | 长图，高度自适应内容，多页自动拼接 |
| `1:1` | `1080px 1080px` | 方形卡片 |
| `3:4` | `810px 1080px` | 竖版卡片 |
| `9:16` | `1080px 1920px` | 手机竖屏长图 |

固定尺寸下内容超出一页时自动分页，每页保持指定比例，纵向拼接，内容不截断。

## 示例

```bash
md2img scripts/sample.md -t daily -s long -o daily_long.png
md2img scripts/sample.md -t card -s 1:1 -o card_1x1.png
md2img scripts/sample.md -t poster -s 3:4 -o poster_3x4.png
md2img scripts/sample.md -t minimal -s 9:16 -o minimal_9x16.png
```

## 验证

```bash
./scripts/verify.sh
```

脚本会：

1. 运行 pytest：4 模板 × 4 尺寸 = 16 组合生成、中文渲染、右侧/底部无截断（像素验证）、固定尺寸比例正确
2. 用 CLI 实际生成 16 张 PNG 并逐一校验尺寸与比例

## 项目结构

```
├── src/md2img/
│   ├── __init__.py
│   ├── cli.py            # 命令行入口
│   ├── converter.py      # md → html → pdf → png 转换核心
│   └── templates/        # 4 套独立 CSS 模板
│       ├── daily.css
│       ├── card.css
│       ├── poster.css
│       └── minimal.css
├── tests/test_md2img.py  # pytest 测试
├── scripts/verify.sh     # 一键验证
├── scripts/sample.md     # 示例输入
├── pyproject.toml
└── LICENSE
```

## 许可

[MIT](LICENSE)
