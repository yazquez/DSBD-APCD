# -*- coding: utf-8 -*-
# Ejercicio 2 - Web scraping
# Web scraping en la web de Marca. Recordad instalar las librerías
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
# 2) Crear un archivo JSON a partir de los datos obtenidos

########################################################################

# Look at the terms and the robots.txt file
# http://estaticos.marca.com/robots.txt
from bs4 import BeautifulSoup
import ______  # json package
import _______  # Requests package

# User agent
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'

headers = {
    'User-Agent': user_agent
}

url = "http://www.marca.com/futbol/primera/calendario.html"
# The first parameter is the 'text' from the url requested
soup = BeautifulSoup(__________________, 'html5lib')

resultados = []
jornadas = soup('div', 'jornadaCalendario')
# Once we have the 'jornadas', we need to iterate over them
for ______________________:
    # Date and number data
    datos_jornada = jornada.find('div', 'datosJornada')

    # We need to extract the name and the date. We need to look at the page
    # HTML code to check the tag name
    nombre_jornada = datos_jornada.find(___).text
    fecha_jornada = datos_jornada.find(___).text

    # Matches data
    # To set the parameters, we need to get the tag and the class associated
    partidos_jornada = jornada.find(____, ________________)
    for partido_jornada in partidos_jornada:
        local = ""
        visitante = ""
        try:
            # Finally, let's use the class to find the desired data
            local = partido_jornada.find('span', ______).text
            visitante = partido_jornada.find('span', ________).text
            resultado = partido_jornada.find('span', __________).text
        except:
            pass
        if 'Betis' in [local, visitante]:
            # We want to store the information in a dictionary. The values
            # will be 'local', 'visitante', 'resultado' and 'fecha_jornada'
            # We use a dictionary to transform it to a JSON file
            partido = {}
            partido['local'] = local
            partido[_________] = visitante
            partido[_________] = __________
            partido[_________] = __________
            resultados.append(partido)

# We open a file to write our dictionary in JSON format
with open('json_matches.json', ___) as outfile:
    json._____(________, outfile)
