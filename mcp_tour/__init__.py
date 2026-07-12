"""MCP server wrapping the Korea Tourism Organization Open API for MCP hosts.

Importing this package has no side effects; import :mod:`mcp_tour.server` to
build the FastMCP server (which requires the ``TOUR_API_KEY`` environment
variable).
"""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("mcp-tour")
except PackageNotFoundError:  # pragma: no cover - package not installed
    __version__ = "0.0.0"

__all__ = ["__version__"]
