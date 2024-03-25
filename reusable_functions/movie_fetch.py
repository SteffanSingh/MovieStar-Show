import requests

def movie_fetch(movie_name):
    key = "2837c90f"
    url = f"http://www.omdbapi.com/?apikey={key}&t={movie_name}"
    res = requests.get(url)
    response_data = res.json()
    return response_data