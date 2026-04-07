"""
Vercel FastAPI entrypoint when the project Root Directory is ``src``.

If Vercel is configured with **Root Directory → src**, files at the repo root
(like ``../server.py``) are not part of the deployment, so discovery must find
``server.py`` here instead.

See: https://vercel.com/docs/frameworks/backend/fastapi
"""

from __future__ import annotations

import sys
from pathlib import Path

_src = Path(__file__).resolve().parent
_src_str = str(_src)
if _src_str not in sys.path:
    sys.path.insert(0, _src_str)

from service.service import app  # noqa: E402

__all__ = ["app"]
