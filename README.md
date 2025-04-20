> MCP integration for Korea Tourism Organization's API using Claude Desktop App with help from Cursor.

Example: Using Tourism API in Claude Desktop App

<div align="center">
  <img src="https://github.com/user-attachments/assets/a5cd8ee6-e05a-4fdb-96bc-ceaffaca1a2e" width="500" style="margin-right: 300px;" />
  <img src="https://github.com/user-attachments/assets/f84e9c7c-89a4-4799-a568-9e942630ef1a" width="500" />
</div>

## Description
This MCP server integrates the Korea Tourism Organization's public data API to provide related tourist spots information. It is designed to be used with Claude Desktop via the Model Context Protocol (MCP).

## Features

- Retrieve related tourist spot recommendations
- Get detailed tourist spot information
- Support for multiple content types: tourist attractions, food, and accommodation

## Data Source

We use two main data sources:
1. [Korea Tourism Organization API](https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15128560) - Provides up to 50 highly connected related tourist destinations by region and type
2. [National Standard Tourism Data API](https://www.data.go.kr/data/15101578/openapi.do) - Provides comprehensive information about tourist spots nationwide

## Setup

1. Get API keys from [Data.go.kr](https://www.data.go.kr)
2. Set environment variables in `.env` file:
   ```
   TOUR_API_KEY=your-api-key
   STANDARD_TOUR_API_KEY=your-standard-api-key
   ```

## Installation

### Regular Installation
```bash
pip install mcp-tour
```

### Claude Desktop Installation

Using uv (recommended):
```bash
uv pip install mcp-tour

# Method 1: Using environment variables directly
uv run python -m mcp_tour.hosts.claude_desktop \
  -e TOUR_API_KEY=your-api-key \
  -e STANDARD_TOUR_API_KEY=your-standard-api-key

# Method 2: Using .env file
echo "TOUR_API_KEY=your-api-key" > .env
echo "STANDARD_TOUR_API_KEY=your-standard-api-key" >> .env
uv run python -m mcp_tour.hosts.claude_desktop
```

Using pip:
```bash
pip install mcp-tour

# Method 1: Using environment variables directly
python -m mcp_tour.hosts.claude_desktop \
  -e TOUR_API_KEY=your-api-key \
  -e STANDARD_TOUR_API_KEY=your-standard-api-key

# Method 2: Using .env file
echo "TOUR_API_KEY=your-api-key" > .env
echo "STANDARD_TOUR_API_KEY=your-standard-api-key" >> .env
python -m mcp_tour.hosts.claude_desktop
```

## Usage

### get_related_spots

Fetch related tourist spots:

**Parameters**
- `spot_id`: Tourist spot ID
- `content_type`: one of `all`, `tourist`, `food`, or `accommodation`
- `size`: Number of results (up to 50)

### get_spot_info

Fetch detailed information about a tourist spot:

**Parameters**
- `spot_id`: Tourist spot ID

### get_standard_tour_list

Fetch tourist spots from the National Standard Tourism Data:

**Parameters**
- `page_no`: Page number (default: 1)
- `num_of_rows`: Number of results per page (default: 100)
- `tourist_spot_name`: Optional name of the tourist spot to search for
- `address`: Optional address to search for

## Acknowledgments

This project was inspired by:

- [pfldy2850/py-mcp-naver](https://github.com/pfldy2850/py-mcp-naver)
- [jlowin/fastmcp](https://github.com/jlowin/fastmcp)
- [DYTIS Tistory Blog](https://dytis.tistory.com/113)
- [Cursor](https://www.cursor.com/) – used as the main development environment for integrating the Claude Desktop Plugin
