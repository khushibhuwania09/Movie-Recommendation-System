import pandas as pd
import json
import csv
import statistics
from utils.file_utils import load_properties

def convert_csv():

    configs = load_properties()
    f = open(configs.get('JSON_CURRENT_PATH').data)
    data_users = json.load(f)

    csv_file = configs.get('CSV_CURRENT_PATH').data
    user_ratings = []
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['User_ID', 'Age', 'Occupation', 'Gender', 'Movie_Ids', 'Movie_Rating', 'Movie_Duration'])
        for users_key in data_users:
            user_id = users_key
            user_details = data_users[users_key]['details']
            age = user_details['age']
            occupation = user_details['occupation']
            gender = user_details['gender']
            user_movie_watched = data_users[users_key]['movies_watched']
            for movies_watched in user_movie_watched:
                movie_detail_rating = user_movie_watched[movies_watched]
                movie_user_rating =  movie_detail_rating['rating']
                if movie_user_rating != None:
                    user_ratings.append(movie_user_rating)
            for movies_watched in user_movie_watched:
                movie_detail_rating = user_movie_watched[movies_watched]
                movie_name = movies_watched
                movie_user_rating =  movie_detail_rating['rating']
                movie_mins = movie_detail_rating['minutes']
                if movie_detail_rating['rating'] == None:
                    movie_user_rating = round(statistics.mean(user_ratings),2)
                writer.writerow([user_id, age, occupation, gender, movie_name, movie_user_rating, movie_mins])