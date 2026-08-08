import requests

from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_GET
import httpx
from bs4 import BeautifulSoup
import re


TMDB_DISCOVER_URL = "https://api.themoviedb.org/3/discover/movie"

ONE_MONTH = 60 * 60 * 24 * 30
CACHE_KEY = "netflix_movies_pl_by_tmdb_rating_v1"
settings.TMDB_ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5ZGM2ZmJhMzcyYmEzMzNkZDc4M2I2OTgwM2IxYTg1NyIsIm5iZiI6MTc3NjcwNDg4NC4xMTIsInN1YiI6IjY5ZTY1ZDc0ZTliNjJjOWNlNDgwMzA0MSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.WhfK_gOBACNuf513utkWe7CjmpkX5Al4unke-OQ2pf0"


def template(request, params: dict, cache_key: str):
    page = request.GET.get("page", 1)
    params["page"] = page

    page_cache_key = f"{cache_key}:page:{page}"
    cached_movies = cache.get(page_cache_key)

    if cached_movies is not None:
        return JsonResponse({
            "source": "cache",
            "count": len(cached_movies),
            "results": cached_movies,
        })

    if not settings.TMDB_ACCESS_TOKEN:
        return JsonResponse(
            {"error": "TMDB_ACCESS_TOKEN is not configured"},
            status=500,
        )

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {settings.TMDB_ACCESS_TOKEN}",
    }


    try:
        response = requests.get(
            TMDB_DISCOVER_URL,
            headers=headers,
            params=params,
            timeout=10,
        )
        response.raise_for_status()
    except requests.RequestException as error:
        return JsonResponse(
            {
                "error": "Could not retrieve movies from TMDB",
                "details": str(error),
            },
            status=502,
        )

    data = response.json()

    movies = [
        {
            "tmdb_id": movie["id"],
            "title": movie.get("title"),
            "original_title": movie.get("original_title"),
            "overview": movie.get("overview"),
            "release_date": movie.get("release_date"),
            "rating": movie.get("vote_average"),
            "vote_count": movie.get("vote_count"),
            "poster_path": movie.get("poster_path"),
            "poster_url": (
                f"https://image.tmdb.org/t/p/w500{movie['poster_path']}"
                if movie.get("poster_path")
                else None
            ),
        }
        for movie in data.get("results", [])
    ]

    cache.set(page_cache_key, movies, timeout=ONE_MONTH)

    return JsonResponse({
        "source": "tmdb",
        "count": len(movies),
        "results": movies,
    })


@require_GET
def top_rated_with_1000_votes(request):
    params = {
        "watch_region": "PL",
        "with_watch_providers": "8",
        "with_watch_monetization_types": "flatrate",
        "sort_by": "vote_average.desc",
        "vote_count.gte": 1000,
        "language": "en-US",

    }

    return template(request, params, "netflix_movies_pl_by_tmdb_rating_v1")

@require_GET
def top_rated_with_10000_votes(request):
    params = {
        "watch_region": "PL",
        "with_watch_providers": "8",
        "with_watch_monetization_types": "flatrate",
        "sort_by": "vote_average.desc",
        "vote_count.gte": 10000,
        "language": "en-US",
    }

    return template(request, params, "netflix_movies_pl_by_tmdb_rating_10000_votes")


@require_GET
def top_rated_with_100000_votes(request):
    params = {
        "watch_region": "PL",
        "with_watch_providers": "8",
        "with_watch_monetization_types": "flatrate",
        "sort_by": "vote_average.desc",
        "vote_count.gte": 10000,
        "language": "en-US",
    }

    return template(request, params, "netflix_movies_pl_by_tmdb_rating_100000_votes")


@require_GET
def top_by_votes(request):
    params = {
        "watch_region": "PL",
        "with_watch_providers": "8",
        "with_watch_monetization_types": "flatrate",
        "sort_by": "vote_count.desc",
        "language": "en-US",
        "page": 1,
    }

    return template(request, params, "netflix_movies_pl_by_tmdb_votes")



@require_GET
def top_horrors(request):
    params = {
        "watch_region": "PL",
        "with_watch_providers": "8",       # Netflix
        "with_watch_monetization_types": "flatrate",
        "with_genres": "27",               # Horror
        "vote_count.gte": "1000",
        "sort_by": "vote_average.desc",
        "include_adult": "true",
        "language": "en-US",
        "page": "1",
    }

    return template(request, params, "top_by_rating_horrors")


@require_GET
def top_by_votes_horrors(request):
    params = {
        "watch_region": "PL",
        "with_watch_providers": "8",       # Netflix
        "with_watch_monetization_types": "flatrate",
        "with_genres": "28",               # Horror
        # "vote_count.gte": "1000",
        "sort_by": "vote_count.desc",
        "include_adult": "true",
        "language": "en-US",
        "page": "1",
    }

    return template(request, params, "top_by_rating_horrors")


@require_GET
def top_by_rating_drama(request):
    params = {
        "watch_region": "PL",
        "with_watch_providers": "8",       # Netflix
        "with_watch_monetization_types": "flatrate",
        "with_genres": "18",               # Horror
        "vote_count.gte": "1000",
        "sort_by": "vote_average.desc",
        "include_adult": "true",
        "language": "en-US",
        "page": "1",
    }

    return template(request, params, "top_by_votes_drama")


@require_GET
def top_by_votes_drama(request):
    params = {
        "watch_region": "PL",
        "with_watch_providers": "8",       # Netflix
        "with_watch_monetization_types": "flatrate",
        "with_genres": "18",               # Horror
        # "vote_count.gte": "1000",
        "sort_by": "vote_count.desc",
        "include_adult": "true",
        "language": "en-US",
        "page": "1",
    }

    return template(request, params, "top_by_rating_drama")


@require_GET
def top_by_rating_crime(request):
    params = {
        "watch_region": "PL",
        "with_watch_providers": "8",       # Netflix
        "with_watch_monetization_types": "flatrate",
        "with_genres": "80",               # Horror
        "vote_count.gte": "1000",
        "sort_by": "vote_average.desc",
        "include_adult": "true",
        "language": "en-US",
        "page": "1",
    }

    return template(request, params, "top_by_votes_crime")


@require_GET
def top_by_votes_crime(request):
    params = {
        "watch_region": "PL",
        "with_watch_providers": "8",       # Netflix
        "with_watch_monetization_types": "flatrate",
        "with_genres": "80",               # Horror
        # "vote_count.gte": "1000",
        "sort_by": "vote_count.desc",
        "include_adult": "true",
        "language": "en-US",
        "page": "1",
    }

    return template(request, params, "top_by_rating_crime")


@require_GET
def top_genre_by_rating(request, genre_id):
    params = {
        "watch_region": "PL",
        "with_watch_providers": "8",       # Netflix
        "with_watch_monetization_types": "flatrate",
        "with_genres": genre_id,               # Horror
        "vote_count.gte": "1000",
        "sort_by": "vote_average.desc",
        "include_adult": "true",
        "language": "en-US",
        "page": "1",
    }

    return template(request, params, "top_genre_by_votes_" + genre_id)


@require_GET
def top_genre_by_votes(request, genre_id):
    params = {
        "watch_region": "PL",
        "with_watch_providers": "8",       # Netflix
        "with_watch_monetization_types": "flatrate",
        "with_genres": genre_id,               # Horror
        # "vote_count.gte": "1000",
        "sort_by": "vote_count.desc",
        "include_adult": "true",
        "language": "en-US",
        "page": "1",
    }

    return template(request, params, "top_genre_by_rating_" + genre_id)



@require_GET
def genres(request):


    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {settings.TMDB_ACCESS_TOKEN}",
    }


    response = requests.get(
                "https://api.themoviedb.org/3/genre/movie/list",
                headers=headers,
                timeout=10,
            )

    data = response.json()

    return JsonResponse(data)


@require_GET
def netflix_link(request, tmdb_id):
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {settings.TMDB_ACCESS_TOKEN}",
    }

    response = requests.get(
                f"https://api.themoviedb.org/3/movie/{tmdb_id}/watch/providers",
                headers=headers,
                timeout=10,
            )

    data = response.json()
    link = data["results"]["PL"]["link"]

    html = httpx.get(link).text
    soup = BeautifulSoup(html, "html.parser")

    netflix_img = soup.select_one('.providers a[title*="Netflix"]')
    return JsonResponse({
        "link": netflix_img["href"]
    })



# @require_GET
# def top_rated_with_1000_votes(request):
#     cached_movies = cache.get(CACHE_KEY)

#     if cached_movies is not None:
#         return JsonResponse({
#             "source": "cache",
#             "count": len(cached_movies),
#             "results": cached_movies,
#         })

#     if not settings.TMDB_ACCESS_TOKEN:
#         return JsonResponse(
#             {"error": "TMDB_ACCESS_TOKEN is not configured"},
#             status=500,
#         )

#     headers = {
#         "accept": "application/json",
#         "Authorization": f"Bearer {settings.TMDB_ACCESS_TOKEN}",
#     }

#     params = {
#         "watch_region": "PL",
#         "with_watch_providers": "8",
#         "with_watch_monetization_types": "flatrate",
#         "sort_by": "vote_average.desc",
#         "vote_count.gte": 1000,
#         "language": "en-US",
#         "page": 1,
#     }

#     try:
#         response = requests.get(
#             TMDB_DISCOVER_URL,
#             headers=headers,
#             params=params,
#             timeout=10,
#         )
#         response.raise_for_status()
#     except requests.RequestException as error:
#         return JsonResponse(
#             {
#                 "error": "Could not retrieve movies from TMDB",
#                 "details": str(error),
#             },
#             status=502,
#         )

#     data = response.json()

#     movies = [
#         {
#             "tmdb_id": movie["id"],
#             "title": movie.get("title"),
#             "original_title": movie.get("original_title"),
#             "overview": movie.get("overview"),
#             "release_date": movie.get("release_date"),
#             "rating": movie.get("vote_average"),
#             "vote_count": movie.get("vote_count"),
#             "poster_path": movie.get("poster_path"),
#             "poster_url": (
#                 f"https://image.tmdb.org/t/p/w500{movie['poster_path']}"
#                 if movie.get("poster_path")
#                 else None
#             ),
#         }
#         for movie in data.get("results", [])
#     ]

#     cache.set(CACHE_KEY, movies, timeout=ONE_MONTH)

#     return JsonResponse({
#         "source": "tmdb",
#         "count": len(movies),
#         "results": movies,
#     })
