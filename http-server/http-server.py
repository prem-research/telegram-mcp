import uvicorn
import uvloop
from telethon import TelegramClient
from os import environ

# load environ from env file
with open(".env", "r") as f:
    for line in f.readlines():
        if not line.__contains__("=") or line.startswith("#"):
            continue
        key, value = line.strip().split("=")
        environ[key] = value.strip()

dc_id = environ["DC_ID"]
dc_ip = environ["DC_IP"]
dc_port = environ["DC_PORT"]

api_id = environ["API_ID"]
api_hash = environ["API_HASH"]

http_server = environ.get("HTTP_SERVER", "127.0.0.1")
http_port = int(environ.get("HTTP_PORT", 8080))


async def start_telegram():
    client = TelegramClient("my", api_id=api_id, api_hash=api_hash)

    if dc_id and dc_ip and dc_port:
        client.session.set_dc(dc_id, dc_ip, dc_port)

    await client.start()
    return client


async def main():
    import telegram

    telegram.client = await start_telegram()
    telegram.me = await telegram.client.get_me()

    config = uvicorn.Config(
        "http-api:app",
        host=http_server,
        port=http_port,
    )
    server = uvicorn.Server(config)

    await server.serve()


if __name__ == "__main__":
    uvloop.run(main())
