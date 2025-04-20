> MCP integration for Korea Tourism Organization’s API using Claude Desktop App with help from Cursor.


<div align="center">
  <img src="https://github.com/user-attachments/assets/a5cd8ee6-e05a-4fdb-96bc-ceaffaca1a2e" width="500" style="margin-right: 300px;" />
  <img src="https://github.com/user-attachments/assets/f84e9c7c-89a4-4799-a568-9e942630ef1a" width="500" />
</div>

## Description
This MCP server integrates the Korea Tourism Organization’s public data API to provide related tourist spots information. It is designed to be used with Claude Desktop via the Model Context Protocol (MCP).

## Features

- Retrieve related tourist spot recommendations
- Get detailed tourist spot information
- Support for multiple content types: tourist attractions, food, and accommodation

## Data Source

We use the [Korea Tourism Organization API](https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15128560), which provides up to 50 highly connected related tourist destinations by region and type (tourist spots, food, accommodation).

## Setup

1. Get an API key from [Data.go.kr](https://www.data.go.kr)
2. Set environment variable in `.env` file:
   ```
   TOUR_API_KEY=your-api-key
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

uv run python -m mcp_tour.hosts.claude_desktop \
  -e TOUR_API_KEY=your-api-key
```

Using pip:
```bash
pip install mcp-tour

python -m mcp_tour.hosts.claude_desktop \
  -e TOUR_API_KEY=your-api-key
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

## Acknowledgments

This project was inspired and supported by:

- [pfldy2850/py-mcp-naver](https://github.com/pfldy2850/py-mcp-naver)
- [jlowin/fastmcp](https://github.com/jlowin/fastmcp)
- [DYTIS Tistory Blog](https://dytis.tistory.com/113)
- [Cursor](https://www.cursor.com/) – used as the main development environment for integrating the Claude Desktop Plugin
```

필요한 경우, 상단의 `![placeholder-image](image-url-here)` 자리에 실제 이미지를 삽입하면 됩니다. 수정이나 추가 포맷이 더 필요하면 알려줘!
