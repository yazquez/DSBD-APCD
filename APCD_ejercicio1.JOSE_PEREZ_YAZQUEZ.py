# -*- coding: utf-8 -*-
# Ejercicio 1 - Web scraping
# Web scraping en la web de 20minutos. Recordad instalar las librerías
# necesarias.

# La plantilla se corresponde con los ejemplos vistos en clase esta semana
# y que están disponible en las transparencias. Además, los comentarios en el
# código os dan pistas sobre lo que se hace en cada momento.
# Este código no es universal. Podéis realizar cualquier mejora o cambio
# de código para obtener otro resultado. En ese caso debéis comentar cuál
# sería vuestro objetivo.
# Por favor, tened siempre en cuenta las condiciones legales de la página web
# que queráis usar.

# Podéis consultarme cualquier duda o enviarme vuestras soluciones a mi correo
# electrónico gmunoz4@us.es. El próximo día las veremos en clase.

# Rellenar los huecos para:
# 1) Obtener la información deseada de la página
# 2) Crear un archivo csv a partir de los datos obtenidos

########################################################################

# Look at the terms and the robots.txt file
# http://www.20minutos.es/robots.txt
from bs4 import BeautifulSoup  # BeautifulSoup package
import csv  # csv package
import datetime
import requests  # requests package

# User agent
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'

headers = {
    'User-Agent': user_agent
}

url = "http://www.20minutos.es"
# BeautifulSoup object using a more complete parser
soup = BeautifulSoup(requests.get(url, headers=headers).text, 'html5lib')

links = []
# We look for the news. We need to get the 'div' elements with class 'sep-top'
all_news_lines = soup('div', 'sep-top')
for line in all_news_lines:
    # For each line, we look for 'a' elements
    link = line.find('a')
    links.append(link)

csv_news = []
# For our csv, we store three columns: the text, the length and the date
csv_news.append(['Text', 'Text length', 'Date'])
for link in links:
    # This is one option to get the date
    date = datetime.datetime.now().strftime('%d/%m/%Y')
    # We get the 'title' from the link
    new = link.get("title")
    # We get the text length
    number_of_letters = len(new)
    csv_news.append([new, number_of_letters, date])

# We write our csv
# We open a file with 'w' to allow the write operation
ofile = open('my_news.csv', "w", newline="")
# We define our writer to write the rows
writer = csv.writer(ofile, delimiter=',')

for row in csv_news:
    print(row)
    # We write the row in our csv file
    writer.writerow(row)

ofile.close()
