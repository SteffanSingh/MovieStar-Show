from logging import exception

from werkzeug.security import check_password_hash

from data_managers.data_manager_interface_json import SQLiteDataManager
from flask import Flask, render_template, request, redirect, url_for, flash, abort
from data_managers.data_models import  User, Movie,db, Review
import  requests, json
import os
from flask_sqlalchemy import  SQLAlchemy
from sqlalchemy.orm import declarative_base, sessionmaker,joinedload
#movie_data = "data/data.json"
from sqlalchemy import create_engine, or_
from pprint import  pprint
from flask_paginate import Pagination
from sess import session
from api import api
from sqlalchemy.orm.exc import NoResultFound

app = Flask(__name__)

app.register_blueprint(api, url_prefix='/api')
app.secret_key = '123456'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


"""Base = declarative_base()

#data_file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'moviwebapp.sqlite')


engine = create_engine(f'sqlite:///moviewebapp.sqlite')
Base.metadata.create_all(engine)

# Create a database session
Session = sessionmaker(bind=engine)
session = Session()
"""

data_manager = SQLiteDataManager(app)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///moviewebapp.sqlite'

db.init_app(app)


@app.route('/')
def home():
    """Function to implement home page of Movie web app"""
    return render_template("home.html")


@app.route("/users")
def list_users():
    """function to display all the users with their favourite movies."""
    try:
        users_list = session.query(User).all()
        user_id_list = [user.id for user in users_list]
        return render_template("users.html", users=users_list, user_id_list=user_id_list)
    except Exception as error:
        return render_template("tryAgain.html", error = error)



@app.route("/users/<int:user_id>")
def user_movie_list(user_id):
    """function to implement the add movie to a particular user with the given id."""
    try:
        user = session.query(User).get(user_id)

        user_movies = user.movies
        user_name = user.name if user else "Unknown"

        return render_template("favourite_movie.html", user_name=user_name.title(), movies=user_movies, user_id=user_id)
    except Exception as error:
        return render_template("tryAgain.html", error = error)


@app.route("/add_user", methods = ["GET", "POST"])
def add_user():
    """function to implement the add user in the given user data."""
    try:
        if request.method == "POST":
            users = db.session.query(User).all()
            name = request.form['name']
            email = request.form["email"]
            password = request.form["password"]
            if name == None:
                return render_template("users.html")
            elif len(password) < 6:
                flash("Password should have minimum 6 characters.")
                return redirect(url_for("add_user"))
            elif email in [user.email for user in session.query(User).order_by(User.email)]:
                flash("Email has already been registered ! Please enter different email.")
                return redirect(url_for("add_user"))
            else:
                user = User(
                    name=name.title(),
                    email=email,
                    password=password,
                    movie=[]
                )
                session.add(user)
                session.commit()
                users = db.session.query(User).all()
                return redirect(url_for("list_users"))
        return render_template("add_user.html")
    except Exception as error:
        return render_template("tryAgain.html", error = error)


@app.route("/delete_user/<int:user_id>", methods=["GET","DELETE"])
def delete_user(user_id):
    """function to implement to delete user from a given user list."""

    try:
        session.query(User).filter(User.id == user_id).delete()
        session.commit()
        return redirect(url_for("list_users"))
    except Exception as error:
        return render_template("tryAgain.html", error = error)



@app.route("/users/<int:user_id>/add_movie", methods=["GET", "POST"])
def add_user_movie(user_id):
    """Function to implement adding a movie to a particular user with a given user id"""
    try:
        user = session.query(User).get(user_id)
        user_name = user.name
        if not user:
            return render_template("user_not_found.html")

        if request.method == "POST":
            name = request.form["name"]
            Key = "2837c90f"
            Url = f"http://www.omdbapi.com/?apikey={Key}&t={name}"
            res = requests.get(Url)
            data = res.json()
            if data['Response'] == "False":
                return render_template("movie_not_found.html", user_name=user.name, user_id=user_id)
            existing_movie = session.query(Movie).filter_by(movie_name=data["Title"]).first()
            if existing_movie:
                if existing_movie not in user.movies:
                    user.movies.append(existing_movie)
                    session.commit()  # Commit the session after appending the existing movie
                    return redirect(url_for("user_movie_list", user_id=user_id))
                else:
                    return render_template("movie_already_exists.html", user_name=user.name, user_id=user_id)
            movie_name = data["Title"]
            rating = data["imdbRating"] if data["imdbRating"] != "N/A" else None
            year = data["Year"]
            director = data["Director"]
            poster = data["Poster"]
            note = ""
            movie = Movie(
                movie_name=movie_name,
                director=director,
                rating=rating,
                year=year,
                poster=poster,
                note=note
            )

            user.movies.append(movie)
            session.add(movie)
            session.commit()

            return redirect(url_for("user_movie_list", user_id=user_id))

        return render_template("add_movie.html", user_id=user_id, user_name=user_name)
    except Exception as error:
        return render_template("tryAgain.html", error = error)



@app.route("/users/<int:user_id>/update_movie/<int:movie_id>", methods=["GET", "POST"])
def update_movie(user_id, movie_id):
    """function to implement the update the movie details with the given movie id for a
        particular user with a given user id."""
    try:
        users_list = session.query(User).all()
        user_id_list = [user.id for user in users_list]

        # index = user_id_list.index(user_id)
        user = session.query(User).get(user_id)
        user_name = user.name

        # movies = data_manager.get_user_movies_name_list(user_id)
        user_movie_list = user.movie
        movie_to_update = session.query(Movie).get(movie_id)
        movie_name = movie_to_update.movie_name

        if request.method == "POST":
            rating = request.form["rating"]
            note = request.form["note"]
            for index, movie in enumerate(user_movie_list):
                if int(movie.movie_id) == movie_id:
                    movie_to_update.rating = rating if rating else 0
                    movie_to_update.note = note if note else ""
                    session.commit()
                    return render_template("favourite_movie.html", user_name=user_name, user_id=user_id,
                                           movie_id=movie_id, movies=user_movie_list)
        return render_template("update.html", movie_name=movie_name, user_name=user_name.title(), movie_id=movie_id,
                               movies=user_movie_list, user_id=user_id)
    except Exception as error:
        return render_template("tryAgain.html", error = error)


@app.route("/users/<int:user_id>/delete_movie/<int:movie_id>")
def delete_movie(user_id, movie_id):
    """function to implement to delete a movie with a given id for a given user"""
    try:
        users_list = session.query(User).all()
        user_id_list = [user.id for user in users_list]
        user = session.query(User).get(user_id)
        user_movie_list = user.movie
        movie = session.query(Movie).get(movie_id)
        user_name = user.name if user else "Unknown"

        if movie not in user.movie:
            return render_template("no_movie_found.html", user_id=user_id, user_name=user.name)
        if movie:
            user.movies.remove(movie)
            session.commit()

        user_movie_list = user.movie

        return redirect(url_for("user_movie_list", user_id=user_id))
    except Exception as error:
        return render_template("tryAgain.html", error = error)


@app.route("/sort/<int:user_id>", methods=["GET", "POST"])
def sort_movies(user_id):
    """Function to sort the movie in """
    try:
        user = session.query(User).get(user_id)
        user_name = user.name
        sorted_movie_list = session.query(Movie).join(User.movies).filter(User.id == user_id). \
            order_by(Movie.movie_name).all()

        return render_template("favourite_movie.html", user_name=user_name.title(), movies=sorted_movie_list,
                               user_id=user_id)
    except Exception as error:
        return render_template("tryAgain.html", error = error)


@app.route("/search/<int:user_id>", methods= ["GET", "POST"])
def search_movie(user_id):
    """Function to implement the movies on searched keyword:"""
    try:
        user = session.query(User).get(user_id)
        user_name = user.name
        if request.method == "POST":
            keyword = request.form.get("keyword")
            search_movies_list = session.query(Movie).join(User.movies).filter(User.id == user_id). \
                filter(or_(
                Movie.movie_name.ilike(f"%{keyword}%"),
                Movie.year.ilike(f"%{keyword}%"),
                Movie.director.ilike(f"%{keyword}%"),
                (Movie.rating >= f"{keyword}"))).all()

            if search_movies_list:

                return render_template("search_movie.html", user_name=user_name.title(), keyword=keyword,
                                       movies=search_movies_list, user_id=user_id)
            else:
                return render_template("no_movie_found.html", user_id=user_id, user_name=user.name)

        user_movie_list = user.movie
        return render_template("favourite_movie.html", user_name=user_name.title(), movies=user_movie_list,
                               user_id=user_id)
    except Exception as error:
        return render_template("tryAgain.html", error = error)


@app.route("/add_review/<int:user_id>/<int:movie_id>" , methods=["GET","POST"])
def add_review(user_id, movie_id):
    """function to add the review for a particular user id and movie id:"""
    try:
        review_movie = movie_review(user_id, movie_id)
        if request.method == "POST":
            review = request.form['review']
            rating = request.form['rating']
            print(rating, review)
            # user_id = request.headers.get('user_id')
            user = session.query(User).get(user_id)
            movie_to_review = session.query(Movie).get(movie_id)
            if review == "":
                flash("Please enter your review")
                return redirect(url_for("add_review", user_id=user_id, movie_id=movie_id))
            new_review = Review(
                review_text=review if review else None,
                rating=float(rating) if rating else 0,
                user=user,
                movie=movie_to_review
            )
            print(new_review.review_text)
            session.add(new_review)
            session.commit()

            return redirect(url_for("add_review", user_id=user_id, movie_id=movie_id))
        user = session.query(User).get(user_id)
        movie_to_review = session.query(Movie).get(movie_id)
        return render_template("movie_review.html", movie=movie_to_review, user_id=user_id, movie_id=movie_id,
                               reviews=review_movie)
    except Exception as error:
        return render_template("tryAgain.html", error = error)


def movie_review(user_id, movie_id):
    """"""
    try:
        reviews = session.query(Review).all()
        movie_reviews = []
        for review in reviews:
            if review.movie.movie_id == movie_id:
                movie_reviews.append(review)
        return movie_reviews
    except Exception as  error:
        return render_template("tryAgain.html", error = error)



@app.route("/review/<int:review_id>")
def delete_review(review_id):
    # Retrieve the review to delete
    #review_to_delete = session.query(Review).get(review_id)
    try:
        review_to_delete = session.query(Review).filter_by(review_id=review_id).first()
        if review_to_delete:
            # Delete the review from the database
            session.delete(review_to_delete)
            session.commit()
        return redirect(url_for("add_review", user_id=review_to_delete.user_id,
                                movie_id=review_to_delete.movie_id))
    except Exception as error:
        return render_template("tryAgain.html", error = error)


@app.route("/update/<int:review_id>", methods=["GET", "POST"])
def update_review(review_id):
    """Function to update the review."""
    try:
        review_to_update = session.query(Review).get(review_id)

        if review_to_update is None:
            abort(404)  # Review not found, return 404 error

        if request.method == "POST":
            review = request.form.get('review')
            rating = request.form.get('rating')

            if review == "" or review is None:
                flash("Please enter your review")
                return redirect(url_for("update_review", review_id=review_id))
            if review is not None:
                review_to_update.review_text = review

            if rating == "":
                review_to_update.rating = 0
                print("blank string")
            elif rating is None:
                review_to_update.rating = 0
                print("Nothing")

            else:
                review_to_update.rating = float(rating)

            session.commit()
            return redirect(url_for("add_review", user_id=review_to_update.user_id,
                                    movie_id=review_to_update.movie_id))

        user_id = review_to_update.user_id
        return render_template("edit_review.html", movie=review_to_update.movie,
                               user_id=user_id, movie_id=review_to_update.movie_id,
                               review_id=review_to_update.review_id, review=review_to_update)
    except Exception as error:
        return render_template("tryAgain.html", error = error)


@app.route("/signup", methods= ["GET", "POST"])
def signup():
    """The function to implement the signup component for registration. """
    try:
        if request.method == "POST":
            name = request.form.get("firstName")
            email = request.form.get("email")
            password = request.form.get("password")
            if not name:
                flash("Please enter your name")
                return redirect(url_for("signup"))
            if len(name) > 20:
                flash("Enter your first and last name only.Name cant be more than 20 characters!")
                return redirect(url_for("signup"))
            if "admin" in session.query(User).all() and name == "admin":
                flash("Please enter different name than admin!")
                return redirect(url_for("signup"))
            existing_user = session.query(User).filter_by(email=email).first()
            if existing_user:
                flash("Email address is already in use. Please choose another.")
                return redirect(url_for("signup"))
            if len(password) < 6:
                flash("Password should have minimum 6 characters !")
                return redirect(url_for("signup"))
            if email and password:

                user = User(
                    name=name.title(),
                    email=email,
                    password=password
                )
                session.add(user)
                session.commit()
                flash('Signup successful! You can now sign in.')
                return redirect(url_for("signin"))
            else:
                flash("Email and password cant be blank!")
                return redirect(url_for("signup"))

        return render_template("signup.html")
    except Exception as error:
        return render_template("tryAgain.html", error = error)


@app.route("/login", methods= ["GET", "POST"])
def signin():
    """ The function to implement the sign in component to check user and password."""
    try:
        if request.method == "POST":
            email = request.form["email"]
            password = request.form.get("password")
            user = session.query(User).filter_by(email=email).first()
            if email == "" or password == "":
                flash("Email and password cant be blank!")
                return redirect(url_for("signin"))
            if not user:
                flash("Email is not registered yet.Please register.")
                return redirect(url_for("signup"))
            if user:
                movies = user.movie
                id = user.id
                user_name = user.name
            if user.name == "admin":
                is_admin = True

            if email and password:
                if user and check_password_hash(user.password, password):
                    flash("Login successful ! Welcome to MovieStar Show !")
                    return render_template("favourite_movie.html", user_name=user_name, user_id=id, movies=movies)
                elif user and not check_password_hash(user.password, password):
                    flash("Passsword is incorrect!Please try again.")
                    return redirect(url_for("signin"))
                else:
                    flash("User email or passsword is incorrect!Please try again.")
                    return redirect(url_for("signin"))
        return render_template("login.html")
    except Exception as error:
        return render_template("tryAgain.html", error = error)


@app.route("/resetPassword", methods=["GET", "POST"] )
def resetPassword():
    try:
        users = session.query(User).order_by(User.email).all()
        emails = [user.email for user in users]
        print(emails)
        if request.method == "POST":
            email = request.form.get("email")
            password = request.form.get("password")
            if email == "" or password == "":
                flash("Email and password cant be blank!")
                return redirect(url_for("resetPassword"))
            if len(password) < 6:
                flash("Password should have minimum 6 characters !")
                return redirect(url_for("resetPassword"))
            if email in emails:
                user = session.query(User).filter_by(email=email).first()
                user.password = password
                session.commit()
                flash("Reset Password successful")
                return redirect(url_for("signin"))
            else:
                flash("Email is not registered yet ! Please Register.")
                return redirect(url_for("signup"))

        return render_template("forgot_password.html")
    except Exception as error:
        return render_template("tryAgain.html", error = error)


if __name__ == '__main__':
    #with app.app_context():
     # db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5002)

