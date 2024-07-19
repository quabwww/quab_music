from bot import MyBot
from fastapi import FastAPI
from dotenv import load_dotenv
from pydantic import BaseModel
import os
import asyncio
from Funcion.get import search_download_return_url

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
app = FastAPI()

class Req(BaseModel):
    guild_id: int
    channel_id: int
    user_id: int
    url: str

bot = MyBot(command_prefix="!")

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(bot.start(TOKEN))

@app.get("/")
def on_router():
    return "200"

@app.post("/api/musica/")
async def musica(req: Req):
    print(f"guild_id: {req.guild_id}, channel_id: {req.channel_id}, user_id: {req.user_id}, url: {req.url}")
    search = await search_download_return_url(req.url)
    await bot.play(req.guild_id, req.channel_id, req.user_id, search)
    return "Ok bot"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app=app, host="0.0.0.0", port=9000)
