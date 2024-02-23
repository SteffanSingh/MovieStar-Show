from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date,Float,ARRAY
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from flask import Flask



db = SQLAlchemy()

user_movie_association = db.Table(
    'user_movie_association',
    db.Column('id', db.Integer, db.ForeignKey('users.id')),
    db.Column('movie_id', db.Integer, db.ForeignKey('movies.movie_id')),

)

class User(db.Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    movie = relationship('Movie', backref='users', secondary=user_movie_association  )

    def __repr__(self):
        return f"user(user id={self.id}, author name = {self.name} )"

    def __str__(self):
        return f"The user is {self.name}  "


class Movie(db.Model):
    __tablename__ = "movies"

    movie_id = Column(Integer, primary_key=True, autoincrement=True)
    movie_name = Column(String, unique=True)
    director = Column(String)
    rating = Column(Float)
    year = Column(Integer)
    poster = Column(String)
    note  = Column(String)

    #user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship('User', backref='movies', secondary=user_movie_association)

    #review = relationship('Review', backref='reviews',secondary=user_movie_association)

    def __repr__(self):
        return f"""Movie(movie id= {self.movie_id}, title= {self.movie_name}, 
        Released year= {self.year} """

    def __str__(self):
        f"""Movie(  movie name= {self.movie_name},  year= {self.year}. """

class Review(db.Model):
    __tablename__ = "reviews"
    review_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    movie_id = Column(Integer, ForeignKey('movies.movie_id'))
    review_text = Column(String)
    rating = Column(Float)
    user = relationship('User')
    movie = relationship('Movie')
    def __repr__(self):
        return f"Review(review id={self.review_id}, user id={self.user_id}, movie id={self.movie_id}, rating={self.rating})"

#user= User()
#print(user)
#movies = db.session.query(User).all()
#for movie in movies:
 #   print(movie.movie_name)

#db.create_all()


