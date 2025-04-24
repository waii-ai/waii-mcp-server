from .server import serve


def main():
    """MCP WAII Server - Database interaction functionality for MCP"""
    import argparse
    import asyncio

    parser = argparse.ArgumentParser(
        description="give a model the ability to communicate with a database through WAII"
    )
    parser.add_argument("--database-key", type=str, required=True, help="Database key for authentication")
    parser.add_argument("--api-key", type=str, required=True, help="API key for authentication")
    parser.add_argument("--url", type=str, required=True, help="URL endpoint for the database")

    args = parser.parse_args()
    asyncio.run(serve(args.database_key, args.api_key, args.url))


__all__ = ['serve', 'main']


if __name__ == "__main__":
    main()
