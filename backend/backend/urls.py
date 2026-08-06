"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import netflix_rating.views as routes

urlpatterns = [
    path("api/movies/netflix_top_1000_votes/", routes.top_rated_with_1000_votes, name="netflix-movies"),
    path("api/movies/netflix_top_10000_votes/", routes.top_rated_with_10000_votes, name="netflix-movies"),
    path("api/movies/netflix_top_100000_votes/", routes.top_rated_with_100000_votes, name="netflix-movies"),
    path("api/movies/netflix_top_by_votes/", routes.top_by_votes, name="netflix-movies"),
    path("api/movies/netflix_top_horror/", routes.top_horrors, name="netflix-movies"),
    path("api/movies/netflix_top_by_votes_horror/", routes.top_by_votes_horrors, name="netflix-movies"),
    path("api/movies/netflix_top_by_rating_drama/", routes.top_by_rating_drama, name="netflix-movies"),
    path("api/movies/netflix_top_by_votes_drama/", routes.top_by_votes_drama, name="netflix-movies"),

    path("api/movies/netflix_top_by_rating_crime/", routes.top_by_rating_crime, name="netflix-movies"),
    path("api/movies/netflix_top_by_votes_crime/", routes.top_by_votes_crime, name="netflix-movies"),
    path("api/genre/", routes.genres, name='genres'),


    path("api/movies/netflix_top_genre_by_rating/<str:genre_id>/", routes.top_genre_by_rating, name="netflix-movies"),
    path("api/movies/netflix_top_genre_by_votes/<str:genre_id>/", routes.top_genre_by_votes, name="netflix-movies"),

    path("api/netflix_link/<str:tmdb_id>/", routes.netflix_link, name="netflix-link"),


    path('admin/', admin.site.urls),
]
