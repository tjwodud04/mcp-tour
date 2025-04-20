# py-mcp-tour

Korea Tourism Organization API integration for Claude using MCP protocol.

## Description

This MCP server provides access to Korea Tourism Organization's tourism data API, specifically focusing on related tourist spots information.

## Features

- Get related tourist spots information
- Get detailed spot information
- Support for different content types (tourist spots, food, accommodation)

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

The server provides the following tools:

### get_related_spots

Get related tourist spots information:

Parameters:
- spot_id: Tourist spot ID
- content_type: Type of content (all/tourist/food/accommodation)
- size: Number of results (max 50)

### get_spot_info

Get detailed information about a tourist spot:

Parameters:
- spot_id: Tourist spot ID

## Development

1. Clone the repository
2. Install dependencies:
   ```bash
   uv pip install -e ".[dev]"
   ```
   or using pip:
   ```bash
   pip install -e ".[dev]"
   ```
3. Run tests:
   ```bash
   python -m pytest
   ```

## License

This project is licensed under the terms of the MIT license.