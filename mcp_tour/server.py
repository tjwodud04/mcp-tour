"""MCP server exposing Korea Tourism Organization APIs as Claude tools.

This module wires up the :class:`~fastmcp.FastMCP` server and registers the tool
functions that an MCP host (such as Claude Desktop) can call. HTTP and
configuration concerns live in :mod:`mcp_tour.client` and :mod:`mcp_tour.config`.
"""

from typing import Optional

from fastmcp import FastMCP

from mcp_tour import config
from mcp_tour.client import TourApiClient

mcp = FastMCP(config.SERVER_NAME, instructions=config.SERVER_INSTRUCTIONS)
_client = TourApiClient(service_key=config.get_api_key())


@mcp.tool(
    name="get_area_based_list",
    description="Get tourist spots information based on area from Korea Tourism Organization",
)
async def get_area_based_list(
    area_code: str,
    signgu_code: str,
    content_type_id: Optional[str] = None,
    size: int = config.DEFAULT_AREA_BASED_SIZE,
) -> str:
    """Get area-based tourist spots information from Korea Tourism Organization API.

    Args:
        area_code (str): Area code for the region
        signgu_code (str): Signgu (city/district) code
        content_type_id (str, optional): Content type ID (12: Tourist Spots, 39: Restaurants, 32: Accommodation)
        size (int): Number of results to return (max 50)

    Returns:
        str: JSON response containing tourist spot information

    Raises:
        Exception: If API request fails
    """
    return await _client.area_based_list(
        area_code=area_code,
        signgu_code=signgu_code,
        content_type_id=content_type_id,
        size=size,
    )


@mcp.tool(
    name="search_by_keyword",
    description="Search tourist spots by keyword from Korea Tourism Organization",
)
async def search_by_keyword(
    keyword: str,
    area_code: str,
    signgu_code: str,
    content_type_id: Optional[str] = None,
    size: int = config.DEFAULT_AREA_BASED_SIZE,
) -> str:
    """Search tourist spots by keyword from Korea Tourism Organization API.

    Args:
        keyword (str): Search keyword
        area_code (str): Area code for the region
        signgu_code (str): Signgu (city/district) code
        content_type_id (str, optional): Content type ID (12: Tourist Spots, 39: Restaurants, 32: Accommodation)
        size (int): Number of results to return (max 50)

    Returns:
        str: JSON response containing search results

    Raises:
        Exception: If API request fails
    """
    return await _client.search_by_keyword(
        keyword=keyword,
        area_code=area_code,
        signgu_code=signgu_code,
        content_type_id=content_type_id,
        size=size,
    )


@mcp.tool(
    name="get_standard_tour_list",
    description="Get tourist spots information from the National Standard Tourism Data API",
)
async def get_standard_tour_list(
    page_no: int = config.DEFAULT_STANDARD_PAGE_NO,
    num_of_rows: int = config.DEFAULT_STANDARD_ROWS,
    tourist_spot_name: Optional[str] = None,
    address: Optional[str] = None,
) -> str:
    """Get tourist spots information from the National Standard Tourism Data API.

    Args:
        page_no (int): Page number (default: 1)
        num_of_rows (int): Number of rows per page (default: 100)
        tourist_spot_name (str, optional): Name of the tourist spot to search for
        address (str, optional): Address to search for

    Returns:
        str: JSON response containing tourist spot information

    Raises:
        Exception: If API request fails
    """
    return await _client.standard_tour_list(
        page_no=page_no,
        num_of_rows=num_of_rows,
        tourist_spot_name=tourist_spot_name,
        address=address,
    )


def main() -> None:
    """Run the MCP server over stdio (the transport Claude Desktop expects)."""
    mcp.run()


if __name__ == "__main__":
    main()
