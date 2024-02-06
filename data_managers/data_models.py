from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date,Float
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from flask import Flask


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

    def __repr__(self):
        return f"user(user id={self.user_id}, author name = {self.name} )"

    def __str__(self):
        return f"The user is {self.name}  "


class Movie(db.Model):
    __tablename__ = "movies"

    movie_id = Column(Integer, primary_key=True, autoincrement=True)
    movie_name = Column(String, unique=True)
    director = Column(String)
    rating = Column(Float)
    year = Column(Date)
    poster = Column(String)
    note  = Column(String)

    user_id = Column(Integer, ForeignKey("users.id"))
    movie = relationship('User', backref='movies')

    def __repr__(self):
        return f"""Movie(movie id= {self.movie_id}, title= {self.movie_name}, 
        Released year= {self.year} """

    def __str__(self):
        f"""Movie(  movie name= {self.movie_name},  year= {self.year}. """


#user= User()
#print(user)
#movies = db.session.query(User).all()
#for movie in movies:
 #   print(movie.movie_name)



