"""
Copyright 2023–2025 Waii, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

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
