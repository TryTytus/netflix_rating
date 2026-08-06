import requests

url = "https://api.themoviedb.org/3/discover/movie?watch_region=PL&with_watch_providers=8&with_watch_monetization_types=flatrate&sort_by=popularity.desc"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5ZGM2ZmJhMzcyYmEzMzNkZDc4M2I2OTgwM2IxYTg1NyIsIm5iZiI6MTc3NjcwNDg4NC4xMTIsInN1YiI6IjY5ZTY1ZDc0ZTliNjJjOWNlNDgwMzA0MSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.WhfK_gOBACNuf513utkWe7CjmpkX5Al4unke-OQ2pf0"
}

response = requests.get(url, headers=headers)

print(response.text)