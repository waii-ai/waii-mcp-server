# MCP Server WAII

An MCP (Model Context Protocol) server implementation for WAII database interactions. This server allows language models to interact with databases through the WAII SDK.

## Requirements

- Python 3.8 or higher
- A WAII account with API access
- Database credentials supported by WAII

## Installation

```bash
pip install mcp-server-waii
```

## Usage

You can run the server using the command-line interface:

```bash
python -m mcp-server-waii --database-key YOUR_DB_KEY --api-key YOUR_API_KEY --url YOUR_WAII_URL
``` 

### Required Arguments

- `--database-key`: Your database connection key
- `--api-key`: Your WAII API key
- `--url`: WAII API endpoint URL

### Example

```python
from mcp_server_waii import serve
import asyncio

# Run the server
asyncio.run(serve(
    database_key="your_database_key",
    api_key="your_api_key",
    url="https://api.waii.ai/api/"
))
```

## Features

- Database metadata management and conversation
- Natural language to SQL query conversion
- Query execution and result formatting
- Automatic query and data visualization

## Development

To set up the development environment:

1. Clone the repository
```bash
git clone https://github.com/waii-ai/mcp-server-waii.git
cd mcp-server-waii
```

2. Install dependencies:
```bash
pip install -e .
```

3. Run tests:
```bash
python -m pytest tests/
```

## Support

For support, please:
1. Check the [GitHub Issues](https://github.com/waii-ai/mcp-server-waii/issues)
2. Contact WAII support for API-related questions
3. Open a new issue if you find a bug

## License

MIT License - see LICENSE file for details. 