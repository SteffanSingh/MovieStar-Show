import json
import os
from .data_manager_interface import DataManagerInterface


from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from flask import  Flask,session
from data_managers.data_models import User, Movie
from .data_models import   db









# Define the path to the data.json file




class SQLiteDataManager(DataManagerInterface):
    def __init__(self, db):
        self.db = db

    def get_all_users(self):
        # Return all the users all users

        users_list = ""
        return users_list

    def get_all_users_id(self):

        users_id_list = 2
        return users_id_list

    def get_all_movies_id(self, user_id):
        movies_data = self.db.session.query(Movie).filter(Movie.user_id == user_id).all()
        user_movies_id_list = [movie.id for movie in movies_data]
        return user_movies_id_list


    def get_user_movies(self, user_id):
        # Return all the movies for a given user

        movies_data = self.db.session.query(Movie).filter(Movie.user_id == user_id).all()
        #user_movies_list = [movie.movie_name for movie in movies_data]
        return movies_data

    def get_user_movies_name_list(self, user_id):
        movies_data = self.db.session.query(Movie).filter(Movie.user_id == user_id).all()
        user_movies_list = [movie.movie_name for movie in movies_data]
        return user_movies_list

    def add_user(self, user):

        self.db.session.add(user)
        self.db.session.commit()

    def add_movie(self, movie):

        self.db.session.add(movie)
        self.db.session.commit()

    #def update_movie(self, movie ):
     #   movie_to_update = session.query(Movie).filter(Movie.movie_name == movie_name).one()
      #  #movie_to_update.rating = new_rating
       # session.commit()


    #def delete_movie(movie_id):
     #   pass


#obj = SQLiteDataManager(data_file_path)
#x=obj.get_all_movies_id("")
#print(x)

#with app.app_context():
 #   db.create_all()





