"""
Vercel FastAPI entrypoint.

Vercel discovers a top-level ``server.py`` with an ``app`` object.
The real application lives under ``src/``; we add that directory to the path
so existing imports (``service``, ``agents``, …) keep working.

See: https://vercel.com/docs/frameworks/backend/fastapi
"""

from __future__ import annotations

import sys
from pathlib import Path

_src = Path(__file__).resolve().parent / "src"
_src_str = str(_src)
if _src_str not in sys.path:
    sys.path.insert(0, _src_str)

from service.service import app  # noqa: E402

__all__ = ["app"]
