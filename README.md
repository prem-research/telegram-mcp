# telegram-mcp

## Requirements

- Python Project Manager, [UV](https://docs.astral.sh/uv/getting-started/installation/)
- [MCP Client](https://modelcontextprotocol.io/clients)

## Usage

1. install dependencies

```
pip3 install uv
uv venv
source .venv/bin/activate
uv sync
```

2. edit .env file with your telegram api id and hash ([My Telegram](https://my.telegram.org)), don't share with others.

3. start the http-server

`uv run http-server/http-server.py`

4. install the MCP Server

`uv run mcp install mcp-server/mcp-server.py`

<a href="https://glama.ai/mcp/servers/@prem-research/telegram-mcp">
  <img width="380" height="200" src="https://glama.ai/mcp/servers/@prem-research/telegram-mcp/badge" alt="Telegram Server MCP server" />
</a>

## Available Functions

The MCP Server provides the following functions:

- `get_unread_entities`: Get entities which have unread messages in them
- `get_unread_messages(id)`: Get all unread messages from a given entity id
- `get_messages(id, count)`: Get messages limited by a count from an entity
- `get_entities`: Get all entities in the current session
- `get_entity_by_id(id)`: Get an entity from the current session
- `send_message(entity_id, content, reply_to_message_id)`: Send a message to an entity with optional markup and reply

## Common Issues & How to Fix

- Claude can't run MCP server >> Install uv with brew : `brew install uv`
- Can't create new app in Telegram >> Disconnect VPN and retry

## License

[MIT](https://choosealicense.com/licenses/mit/)