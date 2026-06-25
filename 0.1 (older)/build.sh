#!/bin/bash
set -e

echo "Building RegiaScript compiler..."

NUITKA_PATCHELF_PATH=.venv/bin/patchelf python -m nuitka \
    --onefile \
    --output-filename=regiascript \
    --include-package=antlr4 \
    --include-package=src \
    --include-data-dir=src/generated=src/generated \
    --follow-imports \
    main.py

echo "Build complete: ./regiascript"
echo "Size: $(ls -lh regiascript | awk '{print $5}')"