from youtube_search import YoutubeSearch
def search(url):
    results = YoutubeSearch(url, max_results=1).to_dict()
    return results
