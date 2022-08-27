
from re import L
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask,render_template,request
import pandas as pd
import numpy as np
import pickle
movie_60 = pd.read_csv('correct_60.csv')
df = pd.read_csv('moviss_dup.csv')

def create_similarity():
    data = pd.read_csv('final_data1.csv')
    # creating a count matrix
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(data['combo'])
    # creating a similarity score matrix
    similarity = cosine_similarity(count_matrix)
    return data,similarity

def rcmd(m):
    m = m.lower()
    try:
        data.head()
        similarity.shape
    except:
        data, similarity = create_similarity()
    if m not in data['Title'].unique():
        return('Sorry! The movie you requested is not in our database. Please check the spelling or try with some other movies')
    else:
        i = data.loc[data['Title']==m].index[0]
        lst = list(enumerate(similarity[i]))
        lst = sorted(lst, key = lambda x:x[1] ,reverse=True)
        lst = lst[0:11] # excluding first item since it is the requested movie itself
        l = []
        for i in range(len(lst)):
            a = lst[i][0]
            l.append(data['Title'][a])
    return l


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html',
    movie_name = list(movie_60['Title'].values),
    movie_director = list(movie_60['director'].values),
    movie_genre = list(movie_60['Genre'].values),
    image_url = list(movie_60['Image_url'].values),
    movie_vote = list(movie_60['Average_vote'].values),
    movie_runtime = list(movie_60['Runtime'].values),
    movie_imdb = list(movie_60['imdb_link'].values),
    )
@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_movies',methods = ['POST'])
def recommend():
    movie = request.form.get('user_input')
    c = rcmd(movie)
    name =[]
    director = []
    link = []
    imdb = []
    rating = []
    geners = []
    runtime = []
    for i in c:
        df3 = df[df['Title'] == i]
        n = list(df3['Title'])
        name.extend(n)
        d = list(df3['director'])
        p = list(df3['Image_url'])
        q = list(df3['imdb_link'])
        a = list(df3['Average_vote'])
        g = list(df3['Genre'])
        r = list(df3['Runtime'])
        director.extend(d)
        link.extend(p)
        imdb.extend(q)
        rating.extend(a)
        geners.extend(g)
        runtime.extend(r)
    return render_template('recommend.html',
    movie_names = name,
    movie_directors = director,
    movie_genres = geners,
    image_urls = link,
    movie_votes= rating,
    movie_runtimes = runtime,
    movie_imdbs = imdb
    )

    
if __name__ == '__main__':
    app.run(debug=True)
#title ,director ,genre imageurl ,imdb url,vote ,rumtine