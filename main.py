from flask import Flask, jsonify

from utils import search_by_title, search_by_years, search_by_rating_children, search_by_rating_family, \
    search_by_rating_adult, search_by_genre

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.route("/movie/<title>")  # представление страницы данных по поиску данных по названию фильма
def view_by_title(title):
    movie = search_by_title(title)
    return jsonify(movie)


@app.route("/movie/<year_before>/to/<year_past>")  # представление страницы по поиску данных по диапазону лет
def view_by_years(year_before, year_past):
    movies = search_by_years(year_before, year_past)
    return jsonify(movies)


@app.route("/rating/children/")  # представление страницы данных по Rating G
def view_by_rating_children():
    movies = search_by_rating_children()
    return jsonify(movies)


@app.route("/rating/family")  # представление страницы данных по Rating G, PG, PG-13
def view_by_rating_family():
    movies = search_by_rating_family()
    return jsonify(movies)


@app.route("/rating/adult")  # представление страницы данных по Rating R, NC-17
def view_by_rating_adult():
    movies = search_by_rating_adult()
    return jsonify(movies)


@app.route("/genre/<genre>")  # представление страницы по поиску данных по жанру
def view_by_genre(genre):
    movie = search_by_genre(genre)
    return jsonify(movie)


app.run()
