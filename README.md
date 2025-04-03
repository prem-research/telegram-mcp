# telegram-mcp

## Requirements

- Python Project Manager, [UV](https://docs.astral.sh/uv/getting-started/installation/)
- [MCP Client](https://modelcontextprotocol.io/clients)

## Usage

1. install dependencies
```
pip3 instsall uv
uv venv
source .venv/bin/activate
uv sync
```

2. edit .env file with your telegram api id and hash ([My Telegram](https://my.telegram.org)), don't share with others.

3. start the http-server

`uv run http-server/http-server.py`

4. install the MCP Server

`uv run mcp install mcp-server/mcp-server.py`
