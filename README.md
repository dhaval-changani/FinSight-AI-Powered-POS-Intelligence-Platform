# FinSight — AI-Powered POS Intelligence Platform

A FastMCP server that exposes MongoDB order data to AI assistants (Claude Desktop, Claude Code) via the Model Context Protocol.

## Overview

FinSight connects your POS order database to AI tools by running a local MCP server. Claude can query orders directly using natural language, powered by a single MCP tool backed by MongoDB.

## Requirements

- Python >= 3.10
- [uv](https://github.com/astral-sh/uv) package manager
- MongoDB instance (local or remote)

## Setup

1. **Install dependencies**
   ```bash
   uv sync
   ```

2. **Configure environment** — create a `.env` file in the project root:
   ```env
   MONGODB_URI=mongodb://localhost:27017/
   ```

3. **Start the MCP server**
   ```bash
   uv run python main.py
   ```
   The server listens on `http://127.0.0.1:9000`.

## Connecting to Claude

The `fastmcp.json` file registers this server with MCP clients:

```json
{
  "mcpServers": {
    "finsight-pos": {
      "url": "http://127.0.0.1:9000/mcp"
    }
  }
}
```

**Claude Code:** Run `/mcp` and add the server URL `http://127.0.0.1:9000/mcp`.

**Claude Desktop:** Add the `mcpServers` block from `fastmcp.json` into your Claude Desktop `claude_desktop_config.json`.

## Available Tools

| Tool | Parameters | Description |
|---|---|---|
| `get_orders_by_key` | `key: str`, `value: str` | Find an order by any top-level field (e.g. `orderNum`, `status`) |

**Example prompt to Claude:**
> "Find the order with orderNum ORD-946874"

## Project Structure

```
.
├── main.py          # Entry point — starts the FastMCP server
├── mcpclient.py     # MCP server definition and tool registrations
├── config.py        # Loads environment variables
├── dbclient.py      # MongoDB connection and query logic
├── fastmcp.json     # MCP client configuration (Claude Desktop / Claude Code)
└── pyproject.toml   # Dependencies and project metadata
```

## Dependencies

| Package | Purpose |
|---|---|
| `fastmcp` | MCP server framework |
| `pymongo` | MongoDB driver |
| `python-dotenv` | Environment variable loading |
| `uvicorn` | ASGI server for HTTP transport |
