"""命令行入口：md2img input.md -t <模板> -s <尺寸> -o output.png"""
from __future__ import annotations

import argparse
import sys

from . import __version__
from .converter import SIZES, TEMPLATES, convert_markdown, default_output_name


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="md2img",
        description="Markdown 转多模板多尺寸 PNG 图片（开源小工具）",
    )
    parser.add_argument("input", metavar="input.md", help="输入 Markdown 文件路径")
    parser.add_argument(
        "-t", "--template",
        choices=sorted(TEMPLATES),
        default="daily",
        help="模板（默认 daily）",
    )
    parser.add_argument(
        "-s", "--size",
        choices=sorted(SIZES),
        default="long",
        help="尺寸（默认 long，长图自动高度）",
    )
    parser.add_argument(
        "-o", "--output",
        help="输出 PNG 路径（默认 <输入名>_<模板>_<尺寸>.png）",
    )
    parser.add_argument(
        "--version", action="version", version=f"md2img {__version__}"
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    output = args.output or default_output_name(args.input, args.template, args.size)
    try:
        info = convert_markdown(
            args.input, template=args.template, size=args.size, output=output
        )
    except FileNotFoundError:
        print(f"错误: 找不到输入文件 {args.input}", file=sys.stderr)
        return 1
    print(
        f"✅ 已生成 {output} "
        f"(模板={args.template} 尺寸={args.size} "
        f"页数={info['pages']} {info['width']}x{info['height']})"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
