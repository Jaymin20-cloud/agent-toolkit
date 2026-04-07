"""
Vercel FastAPI entrypoint under ``api/`` (alternative layout).

See: https://vercel.com/docs/frameworks/backend/fastapi
"""

from __future__ import annotations

import sys
from pathlib import Path

_root = Path(__file__).resolve().parent.parent
_src = _root / "src"
_src_str = str(_src)
if _src_str not in sys.path:
    sys.path.insert(0, _src_str)

from service.service import app  # noqa: E402

__all__ = ["app"]
