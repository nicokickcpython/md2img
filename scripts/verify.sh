#!/usr/bin/env bash
# md2img 完整验证：pytest（16 组合 + 中文 + 无截断）+ CLI 实际生成 4×4=16 张 PNG
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
PY="${PYTHON:-$ROOT/.venv/bin/python}"
[ -x "$PY" ] || PY="${PYTHON:-python3}"

echo "==> 1/2 运行 pytest（4 模板 × 4 尺寸 = 16 组合 + 中文 + 无截断像素验证）"
PYTHONPATH="$ROOT/src" "$PY" -m pytest tests/ -v

echo "==> 2/2 CLI 实际生成 4×4=16 张 PNG"
OUT="$(mktemp -d)"
i=0
for t in daily card poster minimal; do
  for s in long 1:1 3:4 9:16; do
    i=$((i + 1))
    PYTHONPATH="$ROOT/src" "$PY" -m md2img scripts/sample.md -t "$t" -s "$s" -o "$OUT/${t}_${s}.png"
  done
done

PYTHONPATH="$ROOT/src" "$PY" - "$OUT" <<'PY'
import sys
from pathlib import Path
from PIL import Image

out_dir = Path(sys.argv[1])
files = sorted(out_dir.glob("*.png"))
assert len(files) == 16, f"期望 16 张 PNG，实际 {len(files)}"
expected_ratio = {"1:1": 1.0, "3:4": 0.75, "9:16": 0.5625}
for f in files:
    img = Image.open(f)
    img.load()
    w, h = img.size
    assert w > 100 and h > 100, f"{f.name}: 尺寸异常 {w}x{h}"
    for size, ratio in expected_ratio.items():
        if f.name.endswith(f"_{size}.png"):
            pages = round(h * ratio / w)
            page_ratio = (w / h) * pages
            assert abs(page_ratio - ratio) < 0.02, (
                f"{f.name}: 单页比例 {page_ratio:.4f} != {ratio} (页数={pages})"
            )
    print(f"  ✓ {f.name}: {w}x{h}")
print(f"✅ 4 模板 × 4 尺寸 = 16 组合全部生成成功，比例正确")
PY
rm -rf "$OUT"
echo "✅ verify.sh 完成"
