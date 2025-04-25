from .server import serve
import sys


def main():
    """MCP WAII Server - Database interaction functionality for MCP"""
    import argparse
    import asyncio

    try:
        print("Starting MCP WAII Server...", file=sys.stderr)
        
        parser = argparse.ArgumentParser(
            description="give a model the ability to communicate with a database through WAII"
        )
        parser.add_argument("--database-key", type=str, required=True, help="Database key for authentication")
        parser.add_argument("--api-key", type=str, required=True, help="API key for authentication")
        parser.add_argument("--url", type=str, required=True, help="URL endpoint for the database")

        args = parser.parse_args()
        print(f"Connecting to WAII at {args.url}...", file=sys.stderr)
        
        asyncio.run(serve(args.database_key, args.api_key, args.url))
    except Exception as e:
        print(f"Error starting MCP WAII Server: {str(e)}", file=sys.stderr)
        raise


__all__ = ['serve', 'main']


if __name__ == "__main__":
    main()
