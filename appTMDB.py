import flask
import requests
from flask import request

app = flask.Flask(__name__)

TMDB_API_KEY = '4b2d120288082384e592f342a8617056'

def optionTitle(movie_title):
    response = {
      "fulfillment_response": {
        "messages": [
          {
            "text": {
              #fulfillment text response to be sent to the agent
              "text": [f"Confirmar si el nombre de la película es {movie_title}. Sí/no."]
            }
          }
        ]
      }
    }
    return response

def optionYear(year):
    tmdb_response = requests.get(f'https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&year={year}&sort_by=popularity.desc')
    data = tmdb_response.json()
    #print(data)
    if data['results']:
      titles = [movie["title"] for movie in data["results"]]
      titles_list = '\n'.join(titles)
      response = {
        "fulfillment_response": {
          "messages": [
            {
              "text": {
                #fulfillment text response to be sent to the agent
                "text": [f"Aquí tienes una lista de películas estrenadas el año {year}:\n{titles_list} \n\n ¿Quieres realizar otra búsqueda? (Sí/No)"]
              }
            }
          ]
        }
      }
    else:
      response = {
        "fulfillment_response": {
          "messages": [
            {
              "text": {
                #fulfillment text response to be sent to the agent
                "text": [f"Lo lamento, no se encontró información sobre lanzamientos en el año: {year}. \n ¿Quieres consultar más información? (Sí/No)"]
              }
            }
          ]
        }
      }
    return response

def optionActor(actor):
    tmdb_response = requests.get(f"https://api.themoviedb.org/3/search/person?api_key={TMDB_API_KEY}&query={actor}")
    data = tmdb_response.json()
    if data['results']:
      movies = data['results'][0]['known_for']
      titles = [movie["title"] for movie in movies]
      titles_list = '\n'.join(titles)
      response = {
        "fulfillment_response": {
          "messages": [
            {
              "text": {
                #fulfillment text response to be sent to the agent
                "text": [f"Aquí tienes una lista de películas en que actúa {actor}:\n{titles_list} \n\n ¿Quieres realizar otra búsqueda? (Sí/No)"]
              }
            }
          ]
        }
      }
    else:
      response = {
        "fulfillment_response": {
          "messages": [
            {
              "text": {
                #fulfillment text response to be sent to the agent
                "text": [f"Lo lamento, no se encontró información sobre el actor: {actor}. \n ¿Quieres consultar más información? (Sí/No)"]
              }
            }
          ]
        }
      }
    return response

def movieYear(movie_title):
  tmdb_response = requests.get(f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={movie_title}")
  data = tmdb_response.json()
  if data['results'] and 'release_date' in data['results'][0]:
    date = data['results'][0]['release_date']
    response = {
      "fulfillment_response": {
        "messages": [
          {
            "text": {
              #fulfillment text response to be sent to the agent
              "text": [f"La película {movie_title} fue lanzada en: {date}. \n ¿Quieres consultar más información? (Sí/No)"]
            }
          }
        ]
      }
    }
  else:
    response = {
      "fulfillment_response": {
        "messages": [
          {
            "text": {
              #fulfillment text response to be sent to the agent
              "text": [f"Lo lamento, no se encontró información sobre la película {movie_title}. \n ¿Quieres consultar más información? (Sí/No)"]
            }
          }
        ]
      }
    }
    
  return response

def moviePlot(movie_title):
  tmdb_response = requests.get(f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={movie_title}")
  data = tmdb_response.json()
  if data['results']:
    movie_id = data["results"][0]["id"]
    response_info = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US")
    movie_data = response_info.json()
    plot = movie_data.get("overview")
    response = {
      "fulfillment_response": {
        "messages": [
          {
            "text": {
              #fulfillment text response to be sent to the agent
              "text": [f"Aquí tienes la sinópsis de la película {movie_title}: {plot}. \n ¿Quieres consultar más información? (Sí/No)"]
            }
          }
        ]
      }
    }
  else:
    response = {
      "fulfillment_response": {
        "messages": [
          {
            "text": {
              #fulfillment text response to be sent to the agent
              "text": [f"Lo lamento, no se encontró información sobre la película {movie_title}. \n ¿Quieres consultar más información? (Sí/No)"]
            }
          }
        ]
      }
    }
  return response

def movieGenre(movie_title):
  tmdb_response = requests.get(f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={movie_title}")
  data = tmdb_response.json()
  if data['results']:
    movie_id = data["results"][0]["id"]
    response_info = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US")
    movie_data = response_info.json()
    movie_genres = movie_data.get("genres")
    genres = [genre["name"] for genre in movie_genres]
    response = {
      "fulfillment_response": {
        "messages": [
          {
            "text": {
              #fulfillment text response to be sent to the agent
              "text": [f"La película {movie_title} pertenece al género: {','.join(genres)}. \n ¿Quieres consultar más información? (Sí/No)"]
            }
          }
        ]
      }
    }
  else:
    response = {
      "fulfillment_response": {
        "messages": [
          {
            "text": {
              #fulfillment text response to be sent to the agent
              "text": [f"Lo lamento, no se encontró información sobre la película {movie_title}. \n ¿Quieres consultar más información? (Sí/No)"]
            }
          }
        ]
      }
    }
  return response

def movieProduction(movie_title):
  tmdb_response = requests.get(f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={movie_title}")
  data = tmdb_response.json()
  if data['results']:
    movie_id = data["results"][0]["id"]
    response_info = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US")
    movie_data = response_info.json()
    production_company_name = movie_data["production_companies"][0]["name"]
    response = {
      "fulfillment_response": {
        "messages": [
          {
            "text": {
              #fulfillment text response to be sent to the agent
              "text": [f"La película {movie_title} fue producida por la compañía: {production_company_name}. \n ¿Quieres consultar más información? (Sí/No)"]
            }
          }
        ]
      }
    }
  else:
    response = {
      "fulfillment_response": {
        "messages": [
          {
            "text": {
              #fulfillment text response to be sent to the agent
              "text": [f"Lo lamento, no se encontró información sobre la película {movie_title}. \n ¿Quieres consultar más información? (Sí/No)"]
            }
          }
        ]
      }
    }
  return response

def movieActor(movie_title):
  tmdb_response = requests.get(f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={movie_title}")
  data = tmdb_response.json()
  if data['results']:
    movie_id = data["results"][0]["id"]
    response_crew = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={TMDB_API_KEY}")
    movie_crew = response_crew.json()
    actors = movie_crew.get("cast")
    actor_names = [actor["name"] for actor in actors]
    response = {
      "fulfillment_response": {
        "messages": [
          {
            "text": {
              #fulfillment text response to be sent to the agent
              "text": [f"La película {movie_title} cuenta con la participación de los siguientes actores: {','.join(actor_names)}. \n ¿Quieres consultar más información? (Sí/No)"]
            }
          }
        ]
      }
    }
  else:
    response = {
      "fulfillment_response": {
        "messages": [
          {
            "text": {
              #fulfillment text response to be sent to the agent
              "text": [f"Lo lamento, no se encontró información sobre la película {movie_title}. \n ¿Quieres consultar más información? (Sí/No)"]
            }
          }
        ]
      }
    }
  return response

def movieDirector(movie_title):
  tmdb_response = requests.get(f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={movie_title}")
  data = tmdb_response.json()
  if data['results']:
    movie_id = data["results"][0]["id"]
    response_crew = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={TMDB_API_KEY}")
    movie_crew = response_crew.json()
    for crew_member in movie_crew["crew"]:
      if crew_member["job"] == "Director":
          director_name = crew_member["name"]
          break
    response = {
      "fulfillment_response": {
        "messages": [
          {
            "text": {
              #fulfillment text response to be sent to the agent
              "text": [f"La película {movie_title} fue dirigida por: {director_name}. \n ¿Quieres consultar más información? (Sí/No)"]
            }
          }
        ]
      }
    }
  else:
    response = {
      "fulfillment_response": {
        "messages": [
          {
            "text": {
              #fulfillment text response to be sent to the agent
              "text": [f"Lo lamento, no se encontró información sobre la película {movie_title}. \n ¿Quieres consultar más información? (Sí/No)"]
            }
          }
        ]
      }
    }
  return response

@app.route('/webhook', methods=['POST'])
def webhook():
    tag = request.json['fulfillmentInfo']['tag']
    print("tag: ", tag)

    if tag == "title":
      movie_title = request.json['sessionInfo']['parameters']['movie']   
      response = optionTitle(movie_title)
      print (movie_title)
    elif tag == "year": 
      try: 
        year = request.json['sessionInfo']['parameters']['year'] 
      except: 
        year = request.json['sessionInfo']['parameters']['date'] 
      response = optionYear(year)
    elif tag == "actor":  
      actor = request.json['sessionInfo']['parameters']['person']['original']  
      print(actor)
      response = optionActor(actor)
    elif tag == "infoYear":
      movie_title = request.json['sessionInfo']['parameters']['movie']
      response = movieYear(movie_title)
    elif tag == "infoPlot":
      movie_title = request.json['sessionInfo']['parameters']['movie']
      response = moviePlot(movie_title)
    elif tag == "infoGenre":
      movie_title = request.json['sessionInfo']['parameters']['movie']
      response = movieGenre(movie_title)
    elif tag == "infoProduction":
      movie_title = request.json['sessionInfo']['parameters']['movie']
      response = movieProduction(movie_title)
    elif tag == "infoActor":
      movie_title = request.json['sessionInfo']['parameters']['movie']
      response = movieActor(movie_title)
    elif tag == "infoDirector":
      movie_title = request.json['sessionInfo']['parameters']['movie']
      response = movieDirector(movie_title)
    # elif tag == "infoYear":
    #   movie_title = request.json['sessionInfo']['parameters']['movie']
    #   info = request.json['sessionInfo']['parameters']['info'] 
    #   response = movieInfo(info,movie_title)
    return flask.jsonify(response)

if __name__ == '__main__':
    app.run()

