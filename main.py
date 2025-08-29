import asyncio
import uvicorn
from fastapi import FastAPI
from bot import bot, dp
from routes import router

app = FastAPI()
app.include_router(router)

async def main():
    loop = asyncio.get_event_loop()
    loop.create_task(dp.start_polling(bot))

    server = uvicorn.Server(uvicorn.Config(
        app, 
        host="127.0.0.1",
        port=8000,
        log_level="info"))
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())
