# -*- coding: utf-8 -*-
# Ejercicio 3 - API de IMDB
# Acceso a la API de IMDB. Recordad instalar las librerías necesarias.

# La plantilla se corresponde con la creación de un archivo csv a partir de
# búsquedas en la API. Además, los comentarios en el código os dan pistas
# sobre lo que se hace en cada momento.
# Este código no es universal. Podéis realizar cualquier mejora o cambio
# de código para obtener otro resultado. En ese caso debéis comentar cuál
# sería vuestro objetivo.

# Podéis consultarme cualquier duda o enviarme vuestras soluciones a mi correo
# electrónico gmunoz4@us.es.

# Rellenar los huecos para:
# 1) Obtener la información deseada de la API
# 2) Crear un archivo csv a partir de los datos obtenidos

########################################################################

# API documentation: http://www.omdbapi.com/

import csv  # package for csv files
import requests  # package to execute requests to the API

search_word = 'star wars'  # We are going to look for 'star wars'
url = "http://www.omdbapi.com/?s=" + search_word
content = requests.get(url).json()  # We get the url

# print the 'content' variable to find the key to get the results
results = content['Search']

# We want only the movies results
movies = []
for result in results:
    type = result['Type']
    if type == 'movie':
        movies.append(result)

# We create a csv file, with columns 'Genre', 'Plot', 'Type', 'Title'
# and 'imdbRating'
movies_file = open('star_wars_movies.csv', "w", newline="")  # Write open
writer = csv.writer(movies_file, delimiter=',')
headers = ['Genre', 'Plot', 'Type', 'Title','imdbRating']  # The headers
writer.writerow(headers)

for movie in movies:
    # print the 'movie' variable to find the key to get the id
    movie_id = movie['imdbID']  # We get the movie id to make the request
    # We get every result by id to get more info
    url = "http://www.omdbapi.com/?i=" + movie_id
    content = requests.get(url).json()

    row = []
    genre = content['Genre']
    plot = content['Plot']
    type = content['Type']
    title = content['Title']
    imdbRating = content['imdbRating']

    row = [genre, plot, type, title, imdbRating]
    try:
        writer.writerow(row)
    except:
        # This exception is fired because text unicode codification
        plot = plot.encode('utf-8')
        row[1] = plot
        writer.writerow(row)

movies_file.close()
