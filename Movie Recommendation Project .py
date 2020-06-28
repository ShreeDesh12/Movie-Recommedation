#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np
import warnings
warnings.simplefilter("ignore")
df = pd.read_csv('u.data',sep = '\t',names = ["user_id","item_id","ratings","timestamp"])
df1 = pd.read_csv('u.item',sep = '\|',header= None)
df1 = df1[[0,1]]
df1.columns= ['item_id','MovieName']
movie = pd.merge(df,df1,on ='item_id' )
movie = movie.drop(columns = 'timestamp')
x = pd.DataFrame(movie.groupby('MovieName').count()['ratings'])
x['No. of ratings'] = x['ratings']
x= x.drop(columns = ['ratings'])
movieMatrix = movie.pivot_table(index = "user_id",columns = "MovieName",values = "ratings")

def findMovie(movie):
    Movie = movieMatrix[movie] #finding stats about the movie
    movie_corr = movieMatrix.corrwith( Movie ) #correlating the movie with movies 
    movieList = pd.DataFrame(movie_corr , columns = ['correlation']) #changing the correlation data into dataFrame
    movieList.dropna(inplace = True) #droping the NA 
    movieList  = movieList.join(x['No. of ratings']) # joining the ratings with their resp. movies
    movieList = movieList[movieList['No. of ratings']>100] #getting the movies with min 100 views
    movieList = movieList.sort_values(by = 'correlation', ascending = False)#placing in descending order
    recMovie = movieList.head(n=10)
    print(recMovie.drop(columns = ['correlation']))

movie = input('Enter the movie watched : ')
findMovie(movie)

