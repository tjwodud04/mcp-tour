"""
Korea Tourism Organization API integration for Claude using MCP protocol.

This module provides tools to access Korea Tourism Organization's tourism data API
through the MCP (Model Control Protocol) interface.
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv
import json
import httpx
import certifi
from fastmcp import FastMCP
from typing import Optional
from httpx import HTTPTransport

# Load environment variables from .env file
load_dotenv()

mcp = FastMCP(
    "Korea Tourism API",
    description="Access Korea Tourism Organization's tourism data API",
    dependencies=[
        "httpx",
        "python-dotenv",
        "pydantic",
        "certifi"
    ]
)

TOUR_API_KEY = os.environ.get("TOUR_API_KEY")
if not TOUR_API_KEY:
    raise ValueError("TOUR_API_KEY environment variable is not set")
    
API_ENDPOINT = "https://apis.data.go.kr/B551011/TarRlteTarService"
STANDARD_TOUR_API_ENDPOINT = "https://api.data.go.kr/openapi/tn_pubr_public_trrsrt_api"

# Transport configuration with proper SSL verification
transport = HTTPTransport(verify=certifi.where())

@mcp.tool(
    name="get_area_based_list",
    description="Get tourist spots information based on area from Korea Tourism Organization",
)
async def get_area_based_list(
    area_code: str,
    signgu_code: str,
    content_type_id: Optional[str] = None,
    size: int = 50,
) -> str:
    """
    Get area-based tourist spots information from Korea Tourism Organization API.
    
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
    async with httpx.AsyncClient(transport=transport) as client:
        try:
            # Get current year and month for baseYm parameter
            base_ym = datetime.now().strftime("%Y%m")
            
            params = {
                "serviceKey": TOUR_API_KEY,
                "numOfRows": min(size, 50),
                "pageNo": 1,
                "MobileOS": "ETC",
                "MobileApp": "mcp-tour",
                "baseYm": base_ym,
                "areaCd": area_code,
                "signguCd": signgu_code,
                "_type": "json"
            }
            if content_type_id:
                params["contentTypeId"] = content_type_id

            response = await client.get(
                f"{API_ENDPOINT}/areaBasedList",
                params=params,
                timeout=30.0
            )
            
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Error in get_area_based_list: {str(e)}", file=sys.stderr)
            raise

@mcp.tool(
    name="search_by_keyword",
    description="Search tourist spots by keyword from Korea Tourism Organization",
)
async def search_by_keyword(
    keyword: str,
    area_code: str,
    signgu_code: str,
    content_type_id: Optional[str] = None,
    size: int = 50,
) -> str:
    """
    Search tourist spots by keyword from Korea Tourism Organization API.
    
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
    async with httpx.AsyncClient(transport=transport) as client:
        try:
            # Get current year and month for baseYm parameter
            base_ym = datetime.now().strftime("%Y%m")
            
            params = {
                "serviceKey": TOUR_API_KEY,
                "numOfRows": min(size, 50),
                "pageNo": 1,
                "MobileOS": "ETC",
                "MobileApp": "mcp-tour",
                "baseYm": base_ym,
                "areaCd": area_code,
                "signguCd": signgu_code,
                "keyword": keyword,
                "_type": "json"
            }
            if content_type_id:
                params["contentTypeId"] = content_type_id

            response = await client.get(
                f"{API_ENDPOINT}/searchKeyword",
                params=params,
                timeout=30.0
            )
            
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Error in search_by_keyword: {str(e)}", file=sys.stderr)
            raise

@mcp.tool(
    name="get_standard_tour_list",
    description="Get tourist spots information from the National Standard Tourism Data API",
)
async def get_standard_tour_list(
    page_no: int = 1,
    num_of_rows: int = 100,
    tourist_spot_name: Optional[str] = None,
    address: Optional[str] = None,
) -> str:
    """
    Get tourist spots information from the National Standard Tourism Data API.
    
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
    async with httpx.AsyncClient(transport=transport) as client:
        try:
            params = {
                "serviceKey": TOUR_API_KEY,
                "pageNo": page_no,
                "numOfRows": num_of_rows,
                "type": "json"
            }
            
            if tourist_spot_name:
                params["trrsrtNm"] = tourist_spot_name
            if address:
                params["rdnmadr"] = address

            response = await client.get(
                STANDARD_TOUR_API_ENDPOINT,
                params=params,
                timeout=30.0
            )
            
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Error in get_standard_tour_list: {str(e)}", file=sys.stderr)
            raise

if __name__ == "__main__":
    mcp.run()