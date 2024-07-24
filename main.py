from bot import MusicBot
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response, JSONResponse
from dotenv import load_dotenv
from pydantic import BaseModel
from Funcion.otro import search
import os
import asyncio
from Funcion.get import search_download_return_url
from youtube_search import YoutubeSearch
import json

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
if not TOKEN:
    raise ValueError("DISCORD_TOKEN not found in environment variables")
    
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

    try:
        if not bot.is_user_in_voice_channel(req.guild_id, req.user_id):
            return {"message": f"¡El usuario \"{req.user_id}\" debe estar en un canal de voz para usar este comando!", "status": 400}
        

        search_url = await search_download_return_url(req.url)
        print(search_url)

        result = await bot.play(req.guild_id, req.channel_id, req.user_id, search_url)


        if result:
            message = "Reproduciendo ahora"
            status = 200
        else:
            message = "Una canción ya está en reproducción. Se agregó la nueva canción a la lista."
            status = 201

        return JSONResponse({"voice": True, "data": search_url, "message": message, "status": status}, status_code=200)

    except Exception as e:
        print(f"Error: {e}")
        return {"message": "Error al procesar la solicitud", "status": 500, "error": str(e)}

@app.get("/api/pending_urls/{guild_id}")
async def get_pending_urls(guild_id: int):
    try:
        pending_urls = bot.get_pending_urls(guild_id)
        results = [
            YoutubeSearch(url, max_results=1).to_dict()
            for url in pending_urls
        ]
        return {"guild_id": guild_id, "pending_urls": results}
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener las URLs pendientes")

    
@app.get("/api/youtube_info/")
async def o(music: str):
    n = YoutubeSearch(search_terms=music, max_results=1).to_dict()
    return {"data": n}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app=app, host="0.0.0.0", port=9000)


