"""Convenience entry point; starts the MCP client and its local server."""

import asyncio

from client import main


if __name__ == "__main__":
    asyncio.run(main())
