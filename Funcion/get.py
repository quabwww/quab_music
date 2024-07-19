from youtube_search import YoutubeSearch
import json
import re

async def search_download_return_url(query_or_url):
    # Verificar si el input es una URL de YouTube
    youtube_url_pattern = re.compile(r'^https://www\.youtube\.com/watch\?v=[\w-]+')
    
    if youtube_url_pattern.match(query_or_url):
        return query_or_url  # Devolver la URL directamente
    
    # Si no es una URL, buscar video por texto
    results = YoutubeSearch(query_or_url, max_results=1).to_json()
    results_dict = json.loads(results)
    
    if results_dict['videos']:
        video_info = results_dict['videos'][0]
        video_url = f"https://www.youtube.com{video_info['url_suffix']}"
        return video_url
    
    return None  # Devolver None si no se encontró ningún video

