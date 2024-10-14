import requests
from flask import Flask, render_template, request
import pickle
import openpyxl
import gc
import warnings
warnings.filterwarnings('ignore')
import pandas
from pandas import pivot_table
from recommender import *


app = Flask(__name__)

gc.disable()
#output = open('knn_recommendations.sav', 'rb')

#model_knn = pickle.load(output)

# enable garbage collector again
gc.enable()
#output.close()

recommendedAnime = {}
animeData = pandas.read_excel('animeData.xlsx')
animeData = animeData.pivot_table(index='title.romaji')

from scipy.sparse import csr_matrix

anime_matrix = csr_matrix(animeData.values)

from sklearn.neighbors import NearestNeighbors

model_knn = NearestNeighbors(metric = 'cosine', algorithm = 'brute')
model_knn.fit(anime_matrix)

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

@app.errorhandler(404)
def internal_error(error):
    return render_template('404.html'), 404


# Define a route to display the anime list form
@app.route('/')
def anime_list_form():
    return render_template('anime_list_form.html')

# Define a route to handle the anime list form submission
@app.route('/<type>/<anime>', methods=['GET', 'POST'])
def anime_list(anime, type):
    #type = request.form['list_type']
    #anime = request.form['username']
    print(type)
    if type == "anime":
      recommendations = animes(anime, model_knn, animeData)
    elif type == "user":
      recommendations = list(anime, model_knn, animeData)
    else:
      return "whoops"
    print(type)
    return render_template('anime_list.html', username=anime, recommendations=recommendations)
  
#@app.route('/<username>', methods=['POST'])
#def user_list(username):
#    type = request.form['list_type']
#    username = request.form['username']
#    recommendations = list(username, "bro what")
#    print(type)
#    return render_template('anime_list.html', username=username, recommendations=recommendations)



app.run(host='0.0.0.0', port=81, debug=False)
