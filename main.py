# main.py

from bot import MusicBot
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from dotenv import load_dotenv
from pydantic import BaseModel
from youtube_search import YoutubeSearch
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

bot = MusicBot(command_prefix="!")

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

    if not bot.is_user_in_voice_channel(req.guild_id, req.user_id):
       return {"message": f"¡El usuario \"{req.user_id}\"debe estar en un canal de voz para usar este comando!", "status": 400}
    
    is_playing = bot.is_playing(req.guild_id)
    result = await bot.play(req.guild_id, req.channel_id, req.user_id, search)
    n = YoutubeSearch(search, max_results=1).to_dict()

    if result:
        message = "Reproduciendo ahora"
        status = 200
    else:
        message = "Una canción ya está en reproducción. Se agregó la nueva canción a la lista."
        status = 201

    return {"voice": True, "data": n, "message": message, "status": status}

@app.get("/api/music-list/")
async def get_queue(guild_id: int):
    import json
    queue = bot.get_queue(guild_id)
    list = []
    for i in queue:
        results = YoutubeSearch(i, max_results=1).to_dict()
        list.append(results)
    data = {"data": list}
    op = json.dumps(data, indent=4)

    return Response(content=op, media_type="application/json")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app=app, host="0.0.0.0", port=9000)

