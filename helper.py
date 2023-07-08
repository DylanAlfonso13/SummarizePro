import imdb

ia = imdb.Cinemagoer()

def get_movies(search):
    movies = ia.search_movie(search)
    return movies

def get_movie_details(movie_id):
    movie_details = ia.get_movie(movie_id)
    return movie_details