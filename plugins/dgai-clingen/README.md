# dgai-clingen

A Claude Code plugin that bundles a minimal MCP server for looking up
ClinGen Variant and Gene Curation Expert Panels. Two tools, no auth:

- `clingen.lookup_panel(gene_or_panel)` — resolves an HGNC gene symbol
  (`OTC`, `BRCA1`) or a 5-digit affiliation ID (`50013`) to panel metadata.
- `clingen.list_chairs(panel_id)` — returns the chair roster for an
  affiliation, falling back to coordinators then approvers when CSpec does
  not carry an explicit chair role.

Data source: the public [CSpec Registry API](https://cspec.genome.network/cspec/),
which serves ClinGen affiliation and gene-linkage data in JSON without an
API key.

## Layout

```
dgai-clingen/
  .claude-plugin/plugin.json    # plugin manifest (mcpServers also declared inline)
  .mcp.json                     # MCP server declaration — see "Why two files" below
  mcp/
    pyproject.toml              # installable distribution for the MCP server
    clingen/
      __init__.py
      client.py                 # CSpec HTTP client + response normalizers
      server.py                 # FastMCP server, two tool definitions
  tests/
    conftest.py                 # vcrpy config (record_mode='once')
    test_clingen_tools.py       # unit + VCR-backed integration tests
    cassettes/*.yaml            # recorded CSpec responses (synthetic on day 1)
```

### Why both `plugin.json` and `.mcp.json` declare the server

Per the [Claude Code Plugins reference](https://code.claude.com/docs/en/plugins-reference#mcp-servers),
plugins may declare MCP servers either inline in `plugin.json` or in a
separate `.mcp.json` at the plugin root. Inline `mcpServers` in
`plugin.json` is currently dropped during manifest parsing — see open bug
[anthropics/claude-code#16143](https://github.com/anthropics/claude-code/issues/16143).
Shipping both means we keep the canonical metadata inline and use
`.mcp.json` as the loader the bug-fix-future and bug-affected versions both
honor.

## Prerequisites

The MCP server is a Python module; Claude Code launches it as
`python3 -m clingen.server`. Make sure the `python3` Claude Code finds has
`mcp` and `httpx` available — install once with:

```
pip install "mcp>=1.2.0" "httpx>=0.27"
```

A future iteration will move this into a `SessionStart` hook that
bootstraps a venv in `${CLAUDE_PLUGIN_DATA}` using the [pattern from the
Plugins reference](https://code.claude.com/docs/en/plugins-reference#persistent-data-directory).
For now, keep the dependency install manual to keep this MCP minimal per
the T2.5 spec.

## Install

From the deepgene-plugins marketplace:

```
/plugin marketplace add deepgene-plugins
/plugin install dgai-clingen@deepgene-plugins
```

The MCP server launches automatically once the plugin is enabled.

## Smoke-test inside Claude Code

The T2.5 acceptance criterion is that `clingen.lookup_panel("OTC")` returns
valid panel metadata in under 5 seconds *inside Claude Code*. After
installing, verify with:

```
/mcp                 # confirms `clingen` shows up in the server list
> use clingen.lookup_panel with gene_or_panel="OTC"
```

…and check the elapsed time in the response. You can also exercise the
tools without Claude Code in the loop:

```python
from clingen.server import lookup_panel, list_chairs
lookup_panel("OTC")        # → panels referencing OTC
list_chairs("50013")       # → chair roster for TP53 VCEP
```

## Tests

```
cd plugins/dgai-clingen
pip install -e mcp[test]
pytest tests/
```

The integration tests are wrapped in `@pytest.mark.vcr`. The repo ships
hand-written cassettes that mirror the documented CSpec response shape, so
`pytest` passes on day one without any network access. To replay against
the real CSpec API:

```
rm tests/cassettes/*.yaml
pytest tests/      # records new cassettes once, then replays them
```

## Why CSpec and not the public affiliation pages

`clinicalgenome.org/affiliation/<id>/` is a SPA — fetching the HTML returns
an empty shell. The CSpec Registry exposes the same affiliation metadata
(plus gene linkages) as JSON via `/Affiliation/id/<id>` and
`/Gene/id/<symbol>/ldFor`, which keeps the MCP server simple and avoids
fragile DOM scraping. Trade-off: CSpec only carries the affiliations that
have published criteria specifications, so a brand-new panel with no
CSpec entry will return `not_found`. When that becomes a real problem, the
fallback path is the GenomeKB downloads at
<https://search.clinicalgenome.org/kb/downloads>.

## Acceptance criterion (T2.5)

> `clingen.lookup_panel("OTC")` returns valid panel metadata in under 5
> seconds.

Covered by `tests/test_clingen_tools.py::test_lookup_panel_by_gene_symbol_otc`,
which times the call and asserts `< 5.0s`.
