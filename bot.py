# bot.py

import discord
import yt_dlp

class MusicBot(discord.Client):
    def __init__(self, command_prefix):
        super().__init__(intents=discord.Intents().all())
        self.queue = {}  # Diccionario para mantener la lista de reproducción por guild
        self.command_prefix = command_prefix

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

        # Agregar la URL a la lista de reproducción
        if guild_id not in self.queue:
            self.queue[guild_id] = []

        self.queue[guild_id].append(url)

        if not voice_client.is_playing():
            await self.play_next(guild_id, voice_client)
            return True  # Indica que una nueva canción está comenzando a reproducirse
        else:
            return False  # Indica que una canción ya está en reproducción y la nueva se agregó a la cola

    async def play_next(self, guild_id, voice_client):
        if guild_id not in self.queue or not self.queue[guild_id]:
            return

        url = self.queue[guild_id].pop(0)
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'quiet': True,
            'cookies': 'cookies.txt'
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
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
            voice_client.play(source, after=lambda e: self.loop.create_task(self.play_next(guild_id, voice_client)))
        except Exception as e:
            print(f"Error al configurar FFmpeg: {e}")
            return


    def is_playing(self, guild_id):
        guild = self.get_guild(guild_id)
        if not guild:
            return False
        voice_client = discord.utils.get(self.voice_clients, guild=guild)
        return voice_client.is_playing() if voice_client else False
    
    
    def is_user_in_voice_channel(self, guild_id, user_id):
        guild = self.get_guild(guild_id)
        if not guild:
            return False

        member = guild.get_member(user_id)
        if not member:
            return False

        return member.voice is not None
    
    def get_pending_urls(self, guild_id):
        return self.queue.get(guild_id, [])







