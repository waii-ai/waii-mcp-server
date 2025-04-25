# WAII MCP Server

A Model Context Protocol server that provides database interaction capabilities through WAII. This server enables Language Models to interact with databases, execute queries, and process database content through natural language.

## Available Tools

### database
Interact with databases through WAII's natural language interface.

**Arguments:**
- `database-key` (string, required): Your database connection string
- `api-key` (string, required): Your WAII API key
- `url` (string, required): WAII API endpoint URL

## Installation

### Using uv/uvx (recommended)
When using uv/uvx no specific installation is needed. You can directly run the server using either approach:

Using `uv`:
```bash
uv run -m mcp_server_waii \
  --url "YOUR_WAII_URL" \
  --api-key "YOUR_API_KEY" \
  --database-key "YOUR_DATABASE_CONNECTION_STRING"
```

### Using pip
Alternatively, you can install mcp-server-waii via pip:

```bash
pip install mcp-server-waii
```

After installation, you can run it as a module:
```bash
python -m mcp_server_waii \
  --url "YOUR_WAII_URL" \
  --api-key "YOUR_API_KEY" \
  --database-key "YOUR_DATABASE_CONNECTION_STRING"
```

## Requirements

- Python 3.10 or higher
- A WAII account with API access
- Database credentials supported by WAII

## Configuration

### Configure for Claude.app

There are several ways to configure the server for Claude:

#### 1. Using uvx (Recommended)
```json
{
    "mcpServers": {
        "waii": {
            "command": "uvx",
            "args": [
                "--directory",
                "/path/to/waii-mcp-server",
                "mcp_server_waii",
                "--url",
                "YOUR_WAII_URL",
                "--api-key",
                "YOUR_API_KEY",
                "--database-key",
                "YOUR_DATABASE_CONNECTION_STRING"
            ]
        }
    }
}
```

#### 2. Using Python installation
```json
{
    "mcpServers": {
        "waii": {
            "command": "python",
            "args": [
                "-m",
                "mcp_server_waii",
                "--url",
                "YOUR_WAII_URL",
                "--api-key",
                "YOUR_API_KEY",
                "--database-key",
                "YOUR_DATABASE_CONNECTION_STRING"
            ]
        }
    }
}
```

#### Example Values:
- `YOUR_WAII_URL`: e.g., "http://<waii url>/api/"
- `YOUR_API_KEY`: Your WAII API key
- `YOUR_DATABASE_CONNECTION_STRING`: e.g., "snowflake://USER@HOST/DB?role=ROLE&warehouse=WAREHOUSE"

## Features

- Natural language to SQL conversion
- Database schema understanding and management
- Query execution and result formatting
- Automatic query optimization suggestions
- Data visualization capabilities

## Development

To set up the development environment:

1. Clone the repository
```bash
git clone https://github.com/waii-ai/mcp-server-waii.git
cd mcp-server-waii
```

2. Install in development mode:
```bash
uv pip install -e .
```

## Support

For support:
1. Check the [GitHub Issues](https://github.com/waii-ai/mcp-server-waii/issues)
2. Contact WAII support for API-related questions
3. Open a new issue if you find a bug

## License

Apache License 2.0 - see LICENSE file for details. 