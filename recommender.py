from bs4 import BeautifulSoup 
import requests 
import json
import random
import pandas
from pandas import pivot_table
import sklearn
from sklearn.neighbors import NearestNeighbors
import pickle
import openpyxl
#import cPickle as pickle
import gc
import warnings
warnings.filterwarnings('ignore')

url = 'https://graphql.anilist.co'

def findMean(name):
    query = '''
    query ($page: Int, $perPage: Int, $name: String) {
      Page (page: $page, perPage: $perPage) {
          pageInfo {
              total
              currentPage
              lastPage
              hasNextPage
              perPage
          }
          users(name: $name) {
        			
              id
        			name
        siteUrl
        			statistics{
                anime{
                  minutesWatched
                  count
                  meanScore
                  scores {
                    mediaIds
                    meanScore
                    score
                  }
                }
              }
            }
        }
    }
    '''
    variables = {
      "page": 1,
      "perPage": 50,
      "name": name
    }
    response = requests.post(url, json={'query': query, 'variables': variables})
      
    data_json = json.loads(response.text)
    return data_json['data']['Page']['users'][0]['statistics']['anime']['meanScore']

#model_knn = pickle.load(open('knn_recommendations.sav', 'rb'))


#ANIME INPUT
def animes(val, model_knn, animeData):
  print("not a list")
  recommendedAnime = {}
    # disable garbage collector
  
  
  distances, indices = model_knn.kneighbors(animeData.loc[val].values.reshape(1, -1), n_neighbors = 101)
  for i in range(0, len(distances.flatten())):
      if i == 0:
          print('Recommendations for {0}:\n'.format(val))
      else:
          recommendedAnime[animeData.index[indices.flatten()[i]]] = 1-distances.flatten()[i]
          print('{0}: {1}, with distance of {2}:'.format(i, animeData.index[indices.flatten()[i]], distances.flatten()[i]))
  recommendedAnime = sorted(recommendedAnime.items(), key=lambda x: x[1], reverse=True)
  return recommendedAnime

#LIST INPUT
def list(name, model_knn, animeData):
  print("calculating recommendations")

    # disable garbage collector
  print("shit loaded")
  query = '''
  query ($username: String, $type: MediaType) {
    MediaListCollection(userName: $username, type: $type) {
      lists {
        entries {
          id
          score(format: POINT_100)
          progress
          startedAt { year, month, day }
          completedAt { year, month, day }
          media {
            title { romaji }
            averageScore
            popularity
          }
        }
      }
    }
  }
  '''
  variables = {
        'username': name,
        'type': 'ANIME'
    }
  response = requests.post(url, json={'query': query, 'variables': variables})
    
  meanScore = findMean(name)
  meanScore = 65
  data_json = json.loads(response.text)
  
  userAnimeList = data_json['data']['MediaListCollection']['lists'][0]['entries']
  userAnime = []
  userRecommendations = {}
  sum = 0
  for i in userAnimeList:
    userAnime.append(i['media']['title']['romaji'])
  #print(userAnime)
  for i in range(0, len(userAnime)):
    val = userAnime[i]
    score = userAnimeList[i]["score"]
    popularity = userAnimeList[i]["media"]["popularity"]
    if popularity < 10000:
      continue
    if val not in animeData.index:
      continue
    distances, indices = model_knn.kneighbors(animeData.loc[val].values.reshape(1, -1), n_neighbors = 2705)
    for i in range(0, len(distances.flatten())):
        if i == 0:
            bruh = 0
            #print('Recommendations for {0}:\n'.format(val))
        else:
            if animeData.index[indices.flatten()[i]]=='Kaguya-sama wa Kokurasetai: Tensaitachi no Renai Zunousen':
              print(val)
              print('{0} * {1} = {2}:'.format((1-distances.flatten()[i]), (score-meanScore), (1-distances.flatten()[i])*(score-meanScore)))
              #print((1-distances.flatten()[i])*(score-meanScore))
              sum+=(1-distances.flatten()[i])*(score-meanScore)
              print("total:" + str(sum))
            #print('{0}: {1}, with distance of {2}:'.format(i, animeData.index[indices.flatten()[i]], distances.flatten()[i]))
            if animeData.index[indices.flatten()[i]] not in userRecommendations:
              userRecommendations[animeData.index[indices.flatten()[i]]] = (1-distances.flatten()[i])*(score-meanScore)/(35*len(userAnime))
            else:
              userRecommendations[animeData.index[indices.flatten()[i]]] = userRecommendations[animeData.index[indices.flatten()[i]]]+(1-distances.flatten()[i])*(score-meanScore)/(35*len(userAnime))

  userRecommendations = sorted(userRecommendations.items(), key=lambda x: x[1], reverse=True)
  print(userRecommendations)
  print(userRecommendations[0])
  print(userRecommendations[0][0])
  print(userRecommendations[0][1])
  return userRecommendations
  