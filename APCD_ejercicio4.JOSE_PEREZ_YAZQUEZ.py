# -*- coding: utf-8 -*-
# Ejercicio 4 - API de Twitter
# Acceso a la API de Twitter. Recordad instalar las librerías necesarias.

# IMPORTANTE: En relación con esto, puede haber problemas al instalar la
# librería usando pip en Anaconda.
# Una solución es usar el comando pip de Anaconda. Esto se hace ejecutando el
# comando pip de la carpeta Scripts dentro de la carpeta de Anaconda.
# Por ejemplo, en mi ordenador Windows sería:
# C:\Users\Gabi\Anaconda\Scripts\pip.exe install twitter

# La plantilla se corresponde con la creación de un archivo csv a partir de
# una búsqueda en la API. Además, los comentarios en el código os dan pistas
# sobre lo que se hace en cada momento. También tenemos ejemplos muy parecidos
# en las transparencias de clase que os pueden servir como guía.
# Este código no es universal. Podéis realizar cualquier mejora o cambio
# de código para obtener otro resultado. En ese caso debéis comentar cuál
# sería vuestro objetivo.

# Podéis consultarme cualquier duda o enviarme vuestras soluciones a mi correo
# electrónico gmunoz4@us.es.

# Rellenar los huecos para:
# 1) Obtener la información deseada de la API
# 2) Limpiar el texto y extraer información de él usando expresiones regulares
# 3) Crear un archivo csv a partir de los datos obtenidos

########################################################################

# API documentation: https://dev.twitter.com/rest/public/search

import csv  # package for csv files
import twitter  # package for twitter
import re  # package for regular expressions

# Twitter credentials
# Please, try to get your own credentials. In case that you had problems
# getting the credentials, you can use the credentials below by default.
CONSUMER_KEY = 'mSIB6HsL3vJnUq4dJFRkuMdgE'
CONSUMER_SECRET = 'l6gKb7Nzm2dSuM6J0WozK5SGVvBdV7drlvwJMKDhINvaebvOFE'
OAUTH_TOKEN = '365628507-vTziO7gDaDTCeCtn4IppIQAje3dQ4sLmIsUmjTGQ'
OAUTH_TOKEN_SECRET = 'yz5NkkWd3IORVI7kH9LIiowf8uo3KNPSzCHKVEDTmGaee'

auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET)

twitter_api = twitter.Twitter(auth=auth)  # We need to pass the auth parameter

search_word = '#starwars'  # We will look for '#starwars'
count = 100

# Add the parameters for search tweets (q is the parameter for query...)
search_results = twitter_api.search.tweets(q=search_word, count=count, lang='es')
# The results are in the 'statuses' key
statuses = search_results['statuses']
# print the 'statuses[0].keys()' variable to find the keys to get the results
print(statuses[0].keys())

# We create a csv, with columns 'user', 'text', 'geo', 'coordinates',
# 'favorited' and 'hashtags'
twitter_file = open('star_wars_twitter.csv', "w", newline="")
writer = csv.writer(twitter_file, delimiter=',')
headers = ['user', 'text', 'geo', 'coordinates', 'favorited', 'hashtags']
writer.writerow(headers)  # Write the headers

for elem in statuses:
    row = []

    text = elem['text']
    user = elem['user']['name']  # We get the name for the user
    geo = elem['geo']
    coordinates = elem['coordinates']
    favorited = elem['favorited']

    # Let's clean a little bit the text using regular expressions
    # Change RT chars by RETWEET
    text = re.sub(r'RT', r'RETWEET', text)
    # Change the user in tweet "@..." by USER
    text = re.sub(r'@\w+', r'USER', text)
    # Let's find all the hashtags "#..." from the tweet
    hashtags = re.ﬁndall(r'#\w+', text)

    row = [user, text, geo, coordinates, favorited, hashtags]
    try:
        writer.writerow(row)
    except:
        # This exception is fired because text unicode codification
        user = user.encode('utf-8')
        row[0] = user
        text = text.encode('utf-8')
        row[1] = text
        writer.writerow(row)

twitter_file.close()
