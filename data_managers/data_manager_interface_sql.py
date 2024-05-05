import json
import os
from .data_manager_interface import DataManagerInterface
from sqlalchemy import create_engine, or_
from sqlalchemy.orm import declarative_base, sessionmaker
from flask import  Flask
from data_managers.data_models import User, Movie, Review,user_movie_association
from .data_models import  db
from flask_sqlalchemy import SQLAlchemy


database = f"sqlite:///moviewebapp.sqlite"

Base = declarative_base()
engine = create_engine(database)
Base.metadata.create_all(engine)

Session= sessionmaker(bind=engine)
session= Session()



class SQLiteDataManager(DataManagerInterface):
    def __init__(self, app):
        self.db = db   #db = SQLAlchemy()

    def list_all_users(self):
        # Return all the users all users
        users = db.session.query(User).all()
        if users:
            return users
        else:
            return []

    def list_user_movies(self, user_id):
        user= db.session.query(User).get(user_id)
        if user:
            movies= user.movie
            if movies:
                return movies
            else:
                return []
        else:
            return None

    def add_user(self, user):
        db.session.add(user)
        db.session.commit()

    def delete_user(self, user_id):
        try:
            user = db.session.query(User).get(user_id)
            db.session.query(user_movie_association).filter_by(id=user_id).delete()
            db.session.delete(user)
            db.session.commit()
        except Exception as error:
            db.session.rollback()
            return  error

    def get_user(self, user_id):
        user= db.session.query(User).get(user_id)
        if user:
            return user
        else:
            return None

    def get_movie(self, movie_id):
        movie = db.session.query(Movie).get(movie_id)
        if movie:
            return movie
        else:
            return None

    def add_movie(self, movie):
        movies = db.session.query(Movie).all()
        db.session.add(movie)
        db.session.commit()

    def update_movie(self, movie):
        db.session.commit()

    def commit_change(self):
        db.session.commit()

    def delete_movie(self, movie_id):
        movies = db.session.query(Movie).all()
        movie = db.session.query(Movie).get(movie_id)
        if movie:
            db.session.delete(movie)
            db.session.commit()
        else:
            raise ValueError("Movie not found")

    def movie_exist_or_not(self, movie):
        existing_movie = db.session.query(Movie).filter_by(movie_name=movie).first()
        return existing_movie

    def user_by_email(self, email_check):
        user = db.session.query(User).filter_by(email=email_check).first()
        return  user

    def sort_by_movie_name_ascending(self,user_id):
        sorted_movie_list = db.session.query(Movie).join(User.movies).filter(User.id == user_id). \
            order_by(Movie.movie_name.asc()).all()
        user= self.get_user(user_id)
        if user.movie:
            return sorted_movie_list
        else:
            return []
    def sort_by_movie_year_descending(self, user_id):
        sorted_movie_list = db.session.query(Movie).join(User.movies).filter(User.id == user_id). \
            order_by(Movie.year.desc()).all()
        user = self.get_user(user_id)
        if user.movie:
            return sorted_movie_list
        else:
            return []

    def sort_by_movie_rating_descending(self, user_id):
        sorted_movie_list = db.session.query(Movie).join(User.movies).filter(User.id == user_id). \
            order_by(Movie.rating.desc()).all()
        user = self.get_user(user_id)
        if user.movie:
            return sorted_movie_list
        else:
            return []

    def search_movie(self,user_id, keyword):
        search_movies_list = db.session.query(Movie).join(User.movies).filter(User.id == user_id). \
            filter(or_(
            Movie.movie_name.ilike(f"%{keyword}%"),
            Movie.year.ilike(f"%{keyword}%"),
            Movie.director.ilike(f"%{keyword}%"),
            (Movie.rating >= f"{keyword}"))).all()
        return  search_movies_list

    def list_all_reviews(self, movie_id):
        reviews = db.session.query(Review).filter(Review.movie_id == movie_id).all()
        if reviews:
            return  reviews
        else:
            return []

    def add_review(self, review):
        db.session.add(review)
        db.session.commit()

    def get_review(self, review_id):
        review = db.session.query(Review).get(review_id)
        return review

    def delete_review(self, review):
        db.session.delete(review)
        db.session.commit()