import sqlite3


def search_by_title(title):
    """
    Функция, которая осуществляет поиск по названию
    Args: title - название фильма
    Returns: dict_movie - словарь с данными по названию фильма
    """
    with sqlite3.connect("netflix.db") as connection:
        cursor = connection.cursor()
        sqlite_query = f"""
                       SELECT title, country, release_year, listed_in, description
                       FROM netflix
                       WHERE title LIKE '%{title}%'
                       """
        cursor.execute(sqlite_query)
        data = cursor.fetchone()
        dict_movie = {"title": data[0],
                      "country": data[1],
                      "release_year": data[2],
                      "genre": data[3],
                      "description": data[4]
                      }
    return dict_movie


def search_by_years(year_before, year_past):
    """
    Функция, которая осуществляет поиск по диапазону лет выпуска
    Args: year_before - начальный выбранный диапазон года
    year_past - конечный выбранный диапазон года для поиска данных
    Returns: movie_list - список с данными по диапазону лет
    """
    with sqlite3.connect("netflix.db") as connection:
        cursor = connection.cursor()
        sqlite_query = f"""
                       SELECT title, release_year
                       FROM netflix
                       WHERE release_year BETWEEN {year_before} AND {year_past}
                       LIMIT 100
                       """
        cursor.execute(sqlite_query)
        data = cursor.fetchall()
        movie_list = []
        for i in data:
            movie = {"title": i[0],
                     "release_year": i[1]}
            movie_list.append(movie)
    return movie_list


def search_by_rating_children():
    """
    Функция, которая осуществляет поиск по рейтингу для Rating G
    Args: -
    Returns: movies_list - список словарей с данными по рейтингу для Rating G
    """
    with sqlite3.connect("netflix.db") as connection:
        cursor = connection.cursor()
        sqlite_query = f"""
                       SELECT title, rating, description
                       FROM netflix
                       WHERE rating = 'G'
                       """
        cursor.execute(sqlite_query)
        data = cursor.fetchall()
        movies_list = []
        for i in data:
            movie = {
                'title': i[0],
                'rating': i[1],
                'description': i[2]}
            movies_list.append(movie)
    return movies_list


def search_by_rating_family():
    """
    Функция, которая осуществляет поиск по рейтингу для Rating G, PG, PG-13
    Args: -
    Returns: movies_list - список словарей с данными по рейтингу для Rating G, PG, PG-13
    """
    with sqlite3.connect("netflix.db") as connection:
        cursor = connection.cursor()
        sqlite_query = f"""
                       SELECT title, rating, description
                       FROM netflix
                       WHERE rating = 'G' OR rating = 'PG' OR rating = 'PG-13'
                       """
        cursor.execute(sqlite_query)
        data = cursor.fetchall()
        movies_list = []
        for i in data:
            movie = {"title": i[0],
                     "rating": i[1],
                     "description": i[2]}
            movies_list.append(movie)
    return movies_list


def search_by_rating_adult():
    """
    Функция, которая осуществляет поиск по рейтингу для Rating R, NC-17
    Args: -
    Returns: movies_list - список словарей с данными по рейтингу для Rating R, NC-17
    """
    with sqlite3.connect("netflix.db") as connection:
        cursor = connection.cursor()
        sqlite_query = f"""
                       SELECT title, rating, description
                       FROM netflix
                       WHERE rating = 'R' OR rating = 'NC-17'
                       """
        cursor.execute(sqlite_query)
        data = cursor.fetchall()
        movies_list = []
        for i in data:
            movie = {"title": i[0],
                     "rating": i[1],
                     "description": i[2]}
            movies_list.append(movie)
    return movies_list


def search_by_genre(genre):
    """
    Функция, которая осуществляет поиск по жанру
    Args: genre - жанр для поиска данных
    Returns: movies_list - список словарей с данными по поиску по жанру
    """
    with sqlite3.connect("netflix.db") as connection:
        cursor = connection.cursor()
        sqlite_query = f"""
                       SELECT title, description
                       FROM netflix
                       WHERE listed_in LIKE '%{genre}%'
                       """
        cursor.execute(sqlite_query)
        data = cursor.fetchall()
        movies_list = []
        for i in data:
            movies = {"title": i[0],
                      "description": i[1]}
            movies_list.append(movies)
    return movies_list


def actors_together(actor_1, actor_2):
    """
    Функция, которая получает в качестве аргумента имена двух актеров,
    сохраняет всех актеров из колонки cast и возвращает список тех, кто играет с ними в паре больше 2 раз.
    Args: actor_1 - имя первого актера
    actor_2 - имя второго актера
    Returns: список тех, кто играет с указанными актерами в паре больше 2 раз
    """
    with sqlite3.connect('netflix.db') as connection:
        cursor = connection.cursor()
        sqlite_query = f"""
                       SELECT netflix.cast
                       FROM netflix
                       WHERE netflix.cast LIKE '%{actor_1}%'
                       AND netflix.cast LIKE '%{actor_2}%'
                       """
        cursor.execute(sqlite_query)
        data = cursor.fetchall()
        list_cast_except_two = []  # список, который получает всех актеров кроме переданных в аргументе и равные
        # количеству раз, которые они в сумме встречались во всех кортежах data
        list_actors = []  # список, получающий всех актеров из списка list_cast_two и которые встречаются там >=2 раз
        for actors in data:
            for casts in actors:
                actors_list = casts.split(', ')
                for actor in actors_list:
                    if actor != actor_1 and actor != actor_2:
                        list_actors.append(actor)
        for actor in list_actors:
            if list_actors.count(actor) >= 2:
                list_cast_except_two.append(actor)
        return list(set(list_cast_except_two))  # преобразование списка в множество и обратно для исключения повторений


print(actors_together("Rose McIver", "Ben Lamb"))  # тест функции actors_together


def find_a_movie(film_type, release_year, genre):
    """
    Функция, которая передает тип картины (фильм или сериал), год выпуска и ее жанр и получает на выходе список названий
    картин с их описаниями в JSON
    Args: film_type - тип картины
    release_year - год выпуска картины
    genre - жанр картины
    Returns: список названий картин с их описаниями в JSON
    """
    with sqlite3.connect('netflix.db') as connection:
        cursor = connection.cursor()
        sqlite_query = f"""
                    SELECT type, release_year, title, description
                    FROM netflix
                    WHERE type = '{film_type}'
                    AND release_year = '{release_year}'
                    AND listed_in LIKE '%{genre}%'
                    LIMIT 10
        """

        cursor.execute(sqlite_query)
        data = cursor.fetchall()

    return data


print(find_a_movie("TV Show", 2020, "Dramas"))  # тест функции find_a_movie
