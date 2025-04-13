from telethon.hints import Entity
from telethon import types
from telegram import client, me as myself  # noqa
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()


"""
async def telegram_connection():
    if not client.is_connected():
        await client.connect()
        print(await client.get_me())
"""


def handle_binary_data(obj):
    if isinstance(obj, bytes):
        try:
            return obj.decode('utf-8', errors='replace')
        except Exception:
            return '[Binary content]'
    elif isinstance(obj, dict):
        return {k: handle_binary_data(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [handle_binary_data(item) for item in obj]
    return obj

async def format_entity(entity: Entity) -> dict:
    try:
        entity_dict = entity.to_dict()
        return handle_binary_data(entity_dict)
    except Exception as e:
        print(f"Error formatting entity: {e}")
        return {"error": "Failed to format entity"}


@app.get("/get_unread_chats")
async def get_unread_chats():
    chats = await get_chats()
    return {k: v for k, v in chats.items() if v["unread_count"] > 0}


@app.get("/get_unread_messages/{chat_id}")
async def get_unread_messages(chat_id: int):
    dialogs = await get_chats()
    if chat_id not in dialogs:
        raise HTTPException(status_code=404, detail=f"Entity {chat_id} not found")

    dialog = dialogs[chat_id]
    unread_count = dialog["unread_count"]

    return await get_messages(chat_id=chat_id, count=unread_count)


@app.get("/get_messages/{chat_id}")
async def get_messages(chat_id: int, count: int = 0):
    entities = {}
    messages = []

    e: Entity = await get_entity(entity=chat_id, raw=True)

    async for message in client.iter_messages(entity=e, reverse=False, limit=count):
        e_id: int = None
        if message.from_id is not None:
            e_id = message.from_id.user_id
        elif message.peer_id is not None:
            e_id = message.peer_id.user_id

        if e_id not in entities:
            entity = await client.get_entity(e_id)
            entities[e_id] = entity

        # Handle message text that might be binary
        message_text = message.message
        if isinstance(message_text, bytes):
            try:
                message_text = message_text.decode('utf-8', errors='replace')
            except Exception:
                message_text = '[Binary content]'

        messages += [
            {
                "text": message_text,
                "date": message.date,
                "id": message.id,
                "from": await format_entity(entity=entities[e_id]),
            }
        ]

        await client.send_read_acknowledge(entity=chat_id, message=message)

    return messages


@app.get("/get_chats")
async def get_chats():
    chats = {}

    async for dialog in client.iter_dialogs():
        try:
            entity_dict = handle_binary_data(dialog.entity.to_dict())
            chats[dialog.id] = {
                "id": dialog.id,
                "title": dialog.name,
                "unread_count": dialog.unread_count,
                "is_pinned": dialog.pinned,
                "type": entity_dict.get("_", "unknown"),
                "last_message_id": dialog.message.id if dialog.message else None,
            }
        except Exception as e:
            print(f"Error processing dialog {dialog.id}: {e}")
            continue

    return chats


def represents_int(s):
    try:
        return int(s)
    except ValueError:
        return False


@app.get("/get_entity/{entity}")
async def get_entity(entity: int | str, raw: bool = False):
    if i := represents_int(entity):
        entity = i

    try:
        e_obj = await client.get_entity(entity)
        if raw:
            return e_obj

        return await format_entity(e_obj)
    except ValueError:
        raise HTTPException(status_code=404, detail=f"Entity {entity} not found")


class SendMessagePost(BaseModel):
    entity: int | str
    content: str
    reply_message_id: int = None


@app.post("/send_message")
async def send_message(post_msg: SendMessagePost):
    e_obj = await get_entity(entity=post_msg.entity, raw=True)

    message = await client.send_message(
        entity=e_obj,
        message=post_msg.content,
        reply_to=post_msg.reply_message_id,
        parse_mode="html",
    )

    if isinstance(message, types.Message) and message.id:
        return {"message_id": message.id}
    else:
        raise HTTPException(status_code=404, detail="Error sending message")


# TODO: handle folders
