import discord
from discord.ext import commands
import yt_dlp as youtube_dl  # Cambiar a yt-dlp
import asyncio

class MyBot(commands.Bot):
    def __init__(self, command_prefix):
        super().__init__(command_prefix=command_prefix, intents=discord.Intents.all())

    async def on_ready(self):
        print(f'Bot conectado como {self.user}')

    async def play(self, guild_id, channel_id, user_id, url):
        guild = self.get_guild(guild_id)
        if not guild:
            print(f"No se encontró el guild con id {guild_id}")
            return

        channel = guild.get_channel(channel_id)
        if not channel:
            print(f"No se encontró el canal con id {channel_id}")
            return

        member = guild.get_member(user_id)
        if not member:
            print(f"No se encontró el miembro con id {user_id}")
            return

        if member.voice:
            voice_client = discord.utils.get(self.voice_clients, guild=guild)
            if not voice_client or not voice_client.is_connected():
                voice_client = await member.voice.channel.connect()
            else:
                await voice_client.move_to(member.voice.channel)
        else:
            print("¡El usuario debe estar en un canal de voz para usar este comando!")
            return

        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'quiet': True,
        }

        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                audio_url = info['url']
                print(f"URL de audio extraída: {audio_url}")
        except Exception as e:
            print(f"Error al extraer la URL del audio: {e}")
            return

        ffmpeg_options = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }
        try:
            source = discord.FFmpegPCMAudio(audio_url, **ffmpeg_options)
        except Exception as e:
            print(f"Error al configurar FFmpeg: {e}")
            return
        
        voice_client.play(source)







