import pandas as pd
import numpy as np
import plotly.express as px

def recommend(user_no = 45):
    data_path = './ml-100k/'
    # read-in ratings data
    data = pd.read_csv((data_path+'u.data'), sep='\t')
    #columns=['user id', 'item id', 'rating', 'timestamp']
    data.columns = ['user id', 'item id', 'rating', 'timestamp']
    data['datetime'] = pd.to_datetime(data['timestamp'], unit='s')
    data.drop('timestamp', axis=1, inplace=True)

    # read-in item-id to movie-name data: non-standard encoding and necessary exclusion of header
    # header definition from readme file in dataset
    columns = ['movie id', 'movie title', 'release date', 'video release date', 'IMDb URL', 'unknown', 'Action', 'Adventure', 'Animation', 'Childrens', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']

    item_data = pd.read_csv((data_path+'u.item'), sep='|', encoding = "ISO-8859-1", header=None)
    item_data.columns = columns
    item_data.set_index('movie id', inplace=True)

    # reshape the data into a form that is congruent with the examples from the encounters
    # and impute NaN as zeros

    pivot_data = pd.pivot_table(data, values='rating', index='user id', columns='item id')
    pivot_data.fillna(0, inplace=True)

    # calculate cos similarity for whole df with sklearn library

    from sklearn.metrics.pairwise import cosine_similarity
    similarity = pd.DataFrame(cosine_similarity(pivot_data), index=pivot_data.index, columns=pivot_data.index)

    #######################################################################
    ### predict ratings for all unseen movies for user, based on the 
    ### ratings of the most similar neighbours who have seen the movie
    #######################################################################

    # extract user vector
    user_vect = pivot_data[pivot_data.index == user_no]

    # extract the movies that have not been rated by user
    not_rated = user_vect[user_vect == 0].dropna(axis=1).columns.values

    # nearest neighbours with their ids
    neighbours = similarity[user_no].sort_values(ascending=False).index

    predictions = []

    for movie in not_rated:
        
        num = 0
        den = 0.0000000001   # avoid div by zero
        
        # extract the 5 most similar neighbours who have seen the movie
        have_seen_neighbours = neighbours[pivot_data.loc[neighbours][movie] != 0][1:6]
        
        for neighbour in have_seen_neighbours:
            sim = similarity.loc[user_no, neighbour]
            rating = pivot_data.loc[neighbour, movie]
            
            num += rating * sim
            den += sim
        
        pred = round(num / den, 1)
        predictions.append([item_data.loc[movie]['movie title'], pred])

    # make output dataframe from list of predictions

    out = pd.DataFrame(predictions, columns=['movie name', 'predicted rating'])
    out.sort_values('predicted rating', ascending=False, inplace=True)

    return out.set_index('predicted rating').head(20)


