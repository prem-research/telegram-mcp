from mcp.server.fastmcp import FastMCP
from requests import get, post
from os import environ

http_server = environ.get("HTTP_SERVER", "127.0.0.1")
http_port = int(environ.get("HTTP_PORT", 8080))
api_endpoint = f"http://{http_server}:{http_port}/"

mcp = FastMCP("telegram")


@mcp.tool(
    name="get_unread_entities",
    description="get entitites which have unread messages in it",
)
async def get_unread_entities() -> dict[dict]:
    return get(f"{api_endpoint}get_unread_chats").json()


@mcp.tool(
    name="get_unread_messages",
    description="get all unread messages from a given entity id",
)
async def get_unread_messages(id: int = None) -> list[dict]:
    return get(f"{api_endpoint}get_unread_messages/{id}").json()


@mcp.tool(
    name="get_messages", description="Get messages limited by a count from an entity"
)
async def get_messages(id: int, count: int = 0) -> list[dict]:
    return get(f"{api_endpoint}get_messages/{id}", params={"count": count}).json()


@mcp.tool(name="get_entities", description="Get all entities in the current session")
async def get_entities() -> dict[dict]:
    """Get all chats in the current session"""
    return get(f"{api_endpoint}get_chats").json()


@mcp.tool(name="get_entity_by_id", description="Get an entity from the current session")
async def get_entity_by_id(id=int | str) -> dict:
    return get(f"{api_endpoint}get_entity/{id}").json()


@mcp.tool(
    name="send_message",
    description="Send a message to an entity with optional markup and reply",
)
async def send_message(
    entity_id: int | str,
    content: str = "",
    reply_to_message_id: int = None,
) -> dict:
    return post(
        f"{api_endpoint}send_message",
        json={
            "entity": entity_id,
            "content": content,
            "reply_to_message_id": reply_to_message_id,
        },
        headers={"Content-Type": "application/json"},
    ).json()


if __name__ == "__main__":
    mcp.run(transport="stdio")
