from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime,Float,ARRAY,Boolean
from sqlalchemy.orm import declarative_base, sessionmaker, relationship,validates, relationship, backref
from flask import Flask
from werkzeug.security import generate_password_hash, check_password_hash
from datetime  import  datetime



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
    email = Column(String, unique=True)
    password = Column(String)
    is_admin = Column(Boolean, default=False)  # New column for admin status
    createdAt = Column(DateTime, default = datetime.now)
    movie = relationship('Movie', backref='users', secondary=user_movie_association)


    @validates('password')
    def validate_password(self, key, password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, email={self.email}, is_admin={self.is_admin})"

    def __str__(self):
        return f"The user is {self.name}"

    def make_admin(self):
        self.is_admin = True

    def remove_admin(self):
        self.is_admin = False

    def promote_to_admin(self):
        self.is_admin = True

    def demote_from_admin(self):
        self.is_admin = False

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
        return f"Review(review id={self.review_id}, user id={self.user_id}, movie id={self.movie_id}, rating = {self.rating})"


#user= User()
#print(user)
#movies = db.session.query(User).all()
#for movie in movies:
 #   print(movie.movie_name)

#db.create_all()


