
# coding: utf-8

# # Twitter y MongoDB

# De las múltiples librerías que nos permiten usar la API de Twitter, usaremos [Python Twitter Tools](https://github.com/sixohsix/twitter). Con esta librería podremos descargar tweets e información de sus usuarios, así que el **ejercicio** será modelar estas dos entidades y almacenar instancias de ellas.
# 
# La idea de este ejercicio está basada en uno anterior que realizó [Gabriel Muñoz](https://twitter.com/Gabi_mu_ri).

# ## Requisitos

# * Python 2. MongoKit no es compatible Python 3, nos topamos con la realidad en Python.
#   * `jupyter`
#   * [`twitter`](https://github.com/sixohsix/twitter)
#   * `pymongo` (en la versión 2.8)
#   * `mongokit`
# * MongoDB

# ## El modelo

# Más o menos todos tenemos en la cabeza como funciona Twitter:
# * Un usuario puede publicar cero o muchos tweets.
# * Un tweet tienes varias propiedades, siendo una de ellas el tweet en si, donde podemos encontrar:
#   * Texto.
#   * Menciones a otros usuarios: [`@josemazo`](https://twitter.com/josemazo).
#   * Enlaces: [`https://www.mongodb.org/`](https://www.mongodb.org/).
#   * Hashtags: `#MongoDB`.

# ## Autorización

# Para usar la API pública de Twitter necesitamos ciertos parámetros, así que vamos a ver como obtenerlos.
# 1. Debemos tener una cuenta en Twitter y estar logueados.
# 2. Visitamos [https://apps.twitter.com/](https://apps.twitter.com/) y pulsamos sobre **`Create New App`**.
# ![Pasos 1 y 2](https://i.imgur.com/85p8ROC.png)
# 3. Rellenamos los campos obligatorios:
#   * **`Name`**: debe ser único.
#   * **`Description`**: debe tener más de 10 carácteres.
#   * **`Website`**: debe ser una URL válida.
#   * **`Yes, I agree`**: debemos marcar ese checkbox.
#   * Finalmente puslamos sobre **`Create your Twitter application`**.
# ![Paso 3](https://i.imgur.com/Yi3vATT.png)
# 4. Pulsamos en el enlace **`Keys and Access Tokens`**.
# ![Paso 4](https://i.imgur.com/BVbSK4M.png)
# 5. En `Application Settings` tenemos dos de los parámetros que necesitamos:
#   * **`Consumer Key`**
#   * **`Consumer Secret`**
# ![Paso 5](https://i.imgur.com/R0UQFTq.png)
# 6. Al final de la misma página hay un botón que dice **`Create my access token`**, pulsamos sobre él.
# ![Paso 6](https://i.imgur.com/x6HO5Wy.png)
# 7. De nuevo al final de esa misma página, bajo `Your Access Token` tenemos los otros dos parámetros restantes:
#   * **`Access Token`**
#   * **`Access Token Secret`**
# ![Paso 7](https://i.imgur.com/oNvj1z5.png)

# ## ¡A programar!

# In[ ]:

# Importing packages
from bson.objectid import ObjectId
import datetime
from mongokit import Connection, Document
import twitter


# In[ ]:

# Twitter configuration, we need to use the parameters that we got before
ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''
CONSUMER_KEY = ''
CONSUMER_SECRET = ''

auth = twitter.oauth.OAuth(ACCESS_TOKEN, ACCESS_TOKEN_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET)

twitter_api = twitter.Twitter(auth=auth)


# In[ ]:

# MongoDB configuration
# Important: For creating a DB for each one of use, we need to use an unique name in the DB_NAME constant,
# like our name un snake_case, e.g.: jose_manuel_camacho
connection = Connection(host='localhost', port=27017)
DB_NAME = ''

db = connection[DB_NAME]


# Vamos a obtener tweets, para ellos usaremos la API y veremos que nos devuelve.

# In[ ]:

# Obtaining tweets
search_word = '__________'  # We can search by a word, a text or a hashtag
count = 100

search_results = twitter_api.search.tweets(q=search_word, count=count, lang='es')
search_results


# In[ ]:

search_results['statuses']


# In[ ]:

search_results['statuses'][0]


# In[ ]:

search_results['statuses'][0]['user']


# Vamos a crear nuestros modelos. Primero haremos uno para los tweets, donde podremos utilizar las propiedades que querramos, pero por ejemplo, podriamos usar los siguientes:
# * `created_at`
# * `text`
# * `retweet_count`
# * `favorite_count`
# * `hashtags`
# * `urls`
# * `mentions`
# * `user_id`
# 
# Para los usuarios podríamos usar algo así:
# * `created_at`
# * `screen_name`
# * `name`
# * `description`
# * `favourites_count`
# * `followers_count`
# * `friends_count`
# * `profile_image_url`
# 
# Algunos de ellos no existen como tal en los resultados de la API, pero para ello podremos programar funciones que nos transformen los resultados en datos válidos para el modelo.

# In[ ]:

@connection.register
class Tweet(Document):
    __collection__ = 'tweets'
    __database__ = DB_NAME
    structure = {
        #########################################
        # Here we need a block for the properties
        #########################################
        'user_id': ObjectId
    }
    required_fields = ['text', 'user_id']
    default_values = {
        'retweet_count': 0,
        'favorite_count': 0,
        'created_at': datetime.datetime.utcnow
    }

@connection.register
class User(Document):
    __collection__ = 'users'
    __database__ = DB_NAME
    structure = {
        #########################################
        # Here we need a block for the properties
        #########################################
    }
    required_fields = ['screen_name']
    default_values = {
        'favourites_count': 0,
        'followers_count': 0,
        'friends_count': 0,
        'created_at': datetime.datetime.utcnow
    }
    indexes = [
        {
            'fields': 'screen_name',
            'unique':True
        }
    ]


# In[ ]:

# Function for transform the datetime from Twitter to Python's format
def twitter_date_to_datetime(twitter_date):
    return datetime.datetime.strptime(twitter_date, '%a %b %d %H:%M:%S +0000 %Y')

## Constructors for the documents
# User getter and constructor
def get_or_create_user(api_user):
    user = db.users.find_one({'screen_name': api_user['screen_name']})
    if not user:
        user = db.User()
        
        user['created_at'] = twitter_date_to_datetime(api_user['created_at'])
        user['screen_name'] = api_user['screen_name']
        
        ###############################################
        # Here we need a block for link more properties
        ###############################################
        
        user.validate()
        
        ####################
        # After validate ...
        ####################
    
    return user

# Tweet constructor
def create_tweet(api_tweet, user):
    tweet = db.Tweet()
    
    tweet['created_at'] = twitter_date_to_datetime(api_tweet['created_at'])
    tweet['text'] = api_tweet['text']
    
    ###############################################
    # Here we need a block for link more properties
    ###############################################

    hashtags = [hashtag['text'] for hashtag in api_tweet['entities']['hashtags']]
    urls = [url['expanded_url'] for url in api_tweet['entities']['urls']]
    mentions = [mention['screen_name'] for mention in api_tweet['entities']['user_mentions']]
    
    tweet['hashtags'] = hashtags
    tweet['urls'] = urls
    tweet['mentions'] = mentions

    tweet['user_id'] = user['_id']
    
    tweet.validate()
    
    ####################
    # After validate ...
    ####################
    
    return tweet


# Por último, vamos a rellenar nuestra base de datos con los resultados obtenidos y comprobar en MongoChef los resultados.

# In[ ]:

for result in search_results['statuses']:
    api_user = result['user']
    user = get_or_create_user(api_user)
    tweet = create_tweet(result, user)


# Para conectarnos a MongoDB desde MongoChef:
# 1. Al abrir MongoChef se nos abre la ventana `Connection Manager` donde pulsaremos en **`New Connection`**.
# 2. Ponemos un nombre a nuestra conexión y en el campo **`Server`** ponemos **`church.cs.us.es`** y pulsamos en **`Save`**.
# 3. Seleccionamos la conexión recién creada y puslamos en **Connect**.
