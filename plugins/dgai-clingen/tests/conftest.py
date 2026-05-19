"""Test fixtures for dgai-clingen.

We use vcrpy in `record_mode='once'`: on first run with network access the
cassette captures real CSpec responses; thereafter pytest replays from disk
with no network needed. To refresh a cassette, delete its YAML file and
re-run the test on a machine that can reach cspec.genome.network.
"""
from __future__ import annotations

import pathlib
import sys

import pytest

# Make the MCP source importable without installing the package — the layout
# mirrors what the plugin manifest sets via PYTHONPATH at runtime.
_PLUGIN_ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_PLUGIN_ROOT / "mcp"))


@pytest.fixture(scope="module")
def vcr_config() -> dict:
    return {
        "record_mode": "once",
        "match_on": ["method", "scheme", "host", "port", "path", "query"],
        # CSpec doesn't send anything sensitive in headers, but strip the
        # User-Agent to keep cassettes stable across machines.
        "filter_headers": ["User-Agent", "Cookie", "Set-Cookie"],
        "decode_compressed_response": True,
    }


@pytest.fixture(scope="module")
def vcr_cassette_dir(request) -> str:
    return str(pathlib.Path(request.module.__file__).parent / "cassettes")
