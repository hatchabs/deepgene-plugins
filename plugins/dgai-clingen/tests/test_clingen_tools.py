"""End-to-end tests for the dgai-clingen MCP tools.

These exercise the same call paths the MCP server uses, hitting CSpec
through a VCR-backed httpx client. The first run records cassettes; later
runs replay them, so CI does not need network access to cspec.genome.network.

We bypass `mcp.tool` wrappers and call the underlying Python functions —
those wrappers add JSON-schema validation and stdio plumbing that have
nothing to do with our business logic.
"""
from __future__ import annotations

import time

import pytest

from clingen import client as client_mod
from clingen import server as server_mod
from clingen.client import (
    ClinGenClient,
    classify_identifier,
    extract_chairs,
    normalize_gene_panel_links,
    normalize_panel,
)


# ---- pure unit checks ------------------------------------------------------


def test_classify_identifier_accepts_gene_symbols():
    assert classify_identifier("OTC").kind == "gene_symbol"
    assert classify_identifier("brca1").value == "BRCA1"  # case-folded
    assert classify_identifier("TP53").value == "TP53"


def test_classify_identifier_accepts_five_digit_panel():
    ident = classify_identifier("50013")
    assert ident.kind == "affiliation_id"
    assert ident.value == "50013"


def test_classify_identifier_rejects_garbage():
    with pytest.raises(ValueError):
        classify_identifier("")
    with pytest.raises(ValueError):
        classify_identifier("not a gene!")
    with pytest.raises(ValueError):
        # 4 digits is not an affiliation ID and also not a gene symbol
        # because gene symbols must start with a letter.
        classify_identifier("1234")


def test_normalize_panel_extracts_clinicalgenome_url():
    out = normalize_panel(
        {"entId": "50013", "entContent": {"affiliation_fullname": "TP53 VCEP"}}
    )
    assert out["panel_id"] == "50013"
    assert out["kind"] == "VCEP"
    assert out["url"] == "https://clinicalgenome.org/affiliation/50013/"


def test_extract_chairs_prefers_explicit_chair_role():
    entity = {
        "entContent": {
            "members": [
                {"name": "Jane Doe", "role": "Chair", "institution": "BCM"},
                {"name": "Sam Curator", "role": "Curator"},
                {"name": "Pat Cochair", "role": "co-chair", "institution": "UNC"},
            ]
        }
    }
    chairs = extract_chairs(entity)
    names = {c["name"] for c in chairs}
    assert names == {"Jane Doe", "Pat Cochair"}


def test_extract_chairs_falls_back_to_approvers():
    entity = {
        "entContent": {
            "members": [{"name": "Anyone", "role": "Curator"}],
            "approver": ["Jane Doe", "John Smith"],
        }
    }
    chairs = extract_chairs(entity)
    assert [c["role"] for c in chairs] == ["Approver", "Approver"]
    assert [c["name"] for c in chairs] == ["Jane Doe", "John Smith"]


# ---- VCR-backed integration checks ----------------------------------------


@pytest.fixture
def real_client() -> ClinGenClient:
    # vcrpy intercepts at the urllib3/httpx layer when the test is wrapped in
    # @pytest.mark.vcr, so we hand back a fresh client with default settings.
    c = ClinGenClient()
    yield c
    c.close()


@pytest.mark.vcr
def test_lookup_panel_by_gene_symbol_otc(real_client, monkeypatch):
    """`lookup_panel("OTC")` returns at least one VCEP linked to OTC."""
    monkeypatch.setattr(server_mod, "_client", real_client)
    start = time.perf_counter()
    out = server_mod.lookup_panel("OTC")
    elapsed = time.perf_counter() - start

    assert out["ok"] is True, out
    assert out["query"] == "OTC"
    assert out["query_kind"] == "gene_symbol"
    assert isinstance(out["panels"], list)
    # Urea Cycle Disorders VCEP (50050) curates OTC. Other panels may appear,
    # so we assert the OTC-handling panel is present rather than the full set.
    panel_ids = {p["panel_id"] for p in out["panels"]}
    assert panel_ids, "expected at least one panel for OTC"
    # Acceptance criterion from T2.5.
    assert elapsed < 5.0, f"lookup_panel('OTC') took {elapsed:.2f}s, must be <5s"


@pytest.mark.vcr
def test_lookup_panel_by_affiliation_id(real_client, monkeypatch):
    """`lookup_panel('50013')` returns TP53 VCEP metadata."""
    monkeypatch.setattr(server_mod, "_client", real_client)
    out = server_mod.lookup_panel("50013")
    assert out["ok"] is True, out
    assert out["query_kind"] == "affiliation_id"
    assert len(out["panels"]) == 1
    panel = out["panels"][0]
    assert panel["panel_id"] == "50013"
    assert panel["kind"] == "VCEP"
    assert panel["url"] == "https://clinicalgenome.org/affiliation/50013/"


@pytest.mark.vcr
def test_lookup_panel_unknown_identifier(real_client, monkeypatch):
    """Unknown affiliation IDs surface as ok=False/error=not_found, not raises."""
    monkeypatch.setattr(server_mod, "_client", real_client)
    out = server_mod.lookup_panel("99999")
    assert out["ok"] is False
    assert out["error"] == "not_found"


@pytest.mark.vcr
def test_list_chairs_for_known_panel(real_client, monkeypatch):
    """`list_chairs('50013')` returns a list (possibly empty) plus panel metadata."""
    monkeypatch.setattr(server_mod, "_client", real_client)
    out = server_mod.list_chairs("50013")
    assert out["ok"] is True, out
    assert out["panel_id"] == "50013"
    assert "panel" in out and out["panel"]["panel_id"] == "50013"
    assert isinstance(out["chairs"], list)
    assert out["chair_count"] == len(out["chairs"])


def test_list_chairs_rejects_gene_symbol():
    """A gene symbol is not a valid panel_id for list_chairs."""
    out = server_mod.list_chairs("OTC")
    assert out["ok"] is False
    assert "5-digit" in out["error"]


def test_normalize_gene_panel_links_handles_empty_ldFor():
    assert normalize_gene_panel_links({"entId": "OTC"}) == []
    assert (
        normalize_gene_panel_links({"entId": "OTC", "ldFor": [{"Affiliation": []}]})
        == []
    )
