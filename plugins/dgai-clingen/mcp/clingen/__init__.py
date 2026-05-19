"""dgai-clingen MCP server.

Exposes two MCP tools that hit the public ClinGen CSpec Registry
(https://cspec.genome.network/cspec/) with no auth: `lookup_panel` resolves
a gene symbol or 5-digit affiliation ID to panel metadata, and `list_chairs`
returns the chair roster for an affiliation when CSpec carries it.
"""

__version__ = "0.1.0"
