# server.py
import os
from dotenv import load_dotenv
import json
import httpx
from fastmcp import FastMCP

# Load environment variables from .env file
load_dotenv()

mcp = FastMCP("Korea Tourism API", dependencies=["httpx"])

TOUR_API_KEY = os.environ.get("TOUR_API_KEY")
if not TOUR_API_KEY:
    raise ValueError("TOUR_API_KEY environment variable is not set")
    
API_ENDPOINT = "https://apis.data.go.kr/B551011/DataLabAiTour"

@mcp.tool(
    name="get_related_spots",
    description="Get related tourist spots information from Korea Tourism Organization",
)
async def get_related_spots(
    spot_id: str,
    content_type: str = "all",  # all, tourist, food, accommodation
    size: int = 50,
):
    """
    Get related tourist spots information
    
    Args:
        spot_id (str): The ID of the tourist spot
        content_type (str): Type of content (all/tourist/food/accommodation)
        size (int): Number of results to return (max 50)
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{API_ENDPOINT}/relatedSpots",
            params={
                "serviceKey": TOUR_API_KEY,
                "spotId": spot_id,
                "contentType": content_type,
                "size": min(size, 50),
                "_type": "json"
            }
        )
        
        response.raise_for_status()
        return response.text

@mcp.tool(
    name="get_spot_info",
    description="Get detailed information about a tourist spot",
)
async def get_spot_info(
    spot_id: str,
):
    """
    Get detailed information about a tourist spot
    
    Args:
        spot_id (str): The ID of the tourist spot
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{API_ENDPOINT}/spotInfo",
            params={
                "serviceKey": TOUR_API_KEY,
                "spotId": spot_id,
                "_type": "json"
            }
        )
        
        response.raise_for_status()
        return response.text

if __name__ == "__main__":
    mcp.run()

