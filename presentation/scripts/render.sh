#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
REPO_ROOT=$(CDPATH= cd -- "$SCRIPT_DIR/../.." && pwd)
PYTHON_EXE=${PYTHON_BIN:-python3}

if [ -n "${QUARTO_BIN:-}" ]; then
  QUARTO_EXE=$QUARTO_BIN
  if [ ! -x "$QUARTO_EXE" ]; then
    echo "QUARTO_NOT_FOUND: QUARTO_BIN 不是可执行文件：$QUARTO_EXE" >&2
    exit 127
  fi
elif command -v quarto >/dev/null 2>&1; then
  QUARTO_EXE=$(command -v quarto)
elif [ -x /opt/quarto/bin/quarto ]; then
  QUARTO_EXE=/opt/quarto/bin/quarto
else
  echo "QUARTO_NOT_FOUND: 请安装 Quarto，或用 QUARTO_BIN 指定可执行文件。" >&2
  exit 127
fi

export PYTHONDONTWRITEBYTECODE=1
cd "$REPO_ROOT"

echo "[1/4] 从内容规格生成 40 份课件"
"$PYTHON_EXE" presentation/scripts/generate_sessions.py

echo "[2/4] 运行课程检查器单元测试"
"$PYTHON_EXE" -m unittest presentation/scripts/test_check_course.py

echo "[3/4] 检查课次、结构、备注、链接与可访问性"
"$PYTHON_EXE" presentation/scripts/check_course.py --root "$REPO_ROOT"

echo "[4/4] 使用 $QUARTO_EXE 渲染课程"
"$QUARTO_EXE" render "$REPO_ROOT/presentation"

echo "COURSE_RENDER_OK: 输出位于 presentation/_output/。"
