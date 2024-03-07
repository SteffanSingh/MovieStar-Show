from data_managers.data_manager_interface_json import SQLiteDataManager
from flask import Flask,  render_template, request,redirect,url_for,flash
from data_managers.data_models import  User, Movie,db, Review
import  requests, json
import os
from flask_sqlalchemy import  SQLAlchemy
from sqlalchemy.orm import declarative_base, sessionmaker,joinedload
#movie_data = "data/data.json"
from sqlalchemy import create_engine, or_
from pprint import  pprint
from flask_paginate import Pagination

from api import api
from sqlalchemy.orm.exc import NoResultFound

app = Flask(__name__)

app.register_blueprint(api, url_prefix='/api')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


Base = declarative_base()

#data_file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'moviwebapp.sqlite')


engine = create_engine(f'sqlite:///moviewebapp.sqlite')
Base.metadata.create_all(engine)

# Create a database session
Session = sessionmaker(bind=engine)
session = Session()

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
    users_list =   session.query(User).all()
    user_id_list = [user.id for user in users_list]
    return render_template("users.html", users = users_list, user_id_list = user_id_list)


@app.route("/users/<int:user_id>")
def user_movie_list(user_id):
    """function to implement the add movie to a particular user with the given id."""
    #user_movies =  session.query(User, Movie).join(Movie, Movie.movie.id == user_id).all()
    user = session.query(User).get(user_id)

    user_movies = user.movies
    user_name = user.name if user else "Unknown"
    #page = request.args.get('page', 1, type=int)
    #per_page = 5  # Number of items per page


    # Execute the query and apply pagination

    #user_movies_query = Movie.query.filter(Movie.users.any(id=user_id))  # Get the query for user's movies
    #user_movies_paginated = user_movies_query.paginate(page=page, per_page=per_page)

    #user_movies =  Movie.query.filter(Movie.users.any(id=user_id)).paginate(page=page,per_page=per_page)


    #filtered_movies = user_movies.paginate(page=page, per_page=per_page)




    return render_template("favourite_movie.html", user_name = user_name, movies = user_movies, user_id = user_id)



@app.route("/add_user", methods = ["GET", "POST"])
def add_user():
    """function to implement the add user in the given user data."""
    if request.method == "POST":
        users =  db.session.query(User).all()
        name = request.form['name']
        if name == None:
            return render_template("users.html")
        else:
            user = User(
                name= name.title(),
                movie=[]
            )
            session.add(user)
            session.commit()
            users = db.session.query(User).all()
            return redirect(url_for("list_users"))
    return render_template("add_user.html")


@app.route("/delete_user/<int:user_id>", methods=["GET","DELETE"])
def delete_user(user_id):
    """function to implement to delete user from a given user list."""

    session.query(User).filter(User.id == user_id).delete()
    session.commit()
    return redirect(url_for("list_users"))

@app.route("/users/<int:user_id>/add_movie", methods=["GET", "POST"])
def add_user_movie(user_id):
    """Function to implement adding a movie to a particular user with a given user id"""
    user = session.query(User).get(user_id)
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

    return render_template("add_movie.html", user_id=user_id)

@app.route("/users/<int:user_id>/update_movie/<int:movie_id>", methods=["GET", "POST"])
def update_movie(user_id, movie_id):
    """function to implement the update the movie details with the given movie id for a
        particular user with a given user id."""
    users_list =  session.query(User).all()
    user_id_list = [user.id for user in users_list]

    #index = user_id_list.index(user_id)
    user = session.query(User).get(user_id)
    user_name =  user.name

    #movies = data_manager.get_user_movies_name_list(user_id)
    user_movie_list = user.movie
    movie_to_update =  session.query(Movie).get(movie_id)
    if request.method == "POST":
        rating = request.form["rating"]
        note = request.form["note"]
        for index, movie in enumerate(user_movie_list):
            if int(movie.movie_id) == movie_id:
                movie_to_update.rating = rating if rating else None
                movie_to_update.note  = note if note else None
                session.commit()
                return render_template("favourite_movie.html", user_name=user_name, user_id=user_id, movie_id = movie_id, movies = user_movie_list)
    return render_template("update.html", user_name = user_name, movie_id = movie_id, movies = user_movie_list, user_id = user_id)


@app.route("/users/<int:user_id>/delete_movie/<int:movie_id>")
def delete_movie(user_id, movie_id):
    """function to implement to delete a movie with a given id for a given user"""

    users_list = session.query(User).all()
    user_id_list = [user.id for user in users_list]
    user = session.query(User).get(user_id)
    user_movie_list = user.movie
    movie = session.query(Movie).get(movie_id)
    user_name = user.name if user else "Unknown"

    user.movies.remove(movie)
    session.commit()

    user_movie_list = user.movie

    return redirect(url_for("user_movie_list", user_id=user_id))


@app.route("/sort/<int:user_id>", methods=["GET", "POST"])
def sort_movies(user_id):
    """Function to sort the movie in """
    user= session.query(User).get(user_id)
    user_name = user.name
    sorted_movie_list = session.query(Movie).join(User.movies).filter(User.id==user_id).\
                            order_by(Movie.movie_name).all()

    return render_template("favourite_movie.html", user_name=user_name, movies=sorted_movie_list, user_id=user_id)



@app.route("/search/<int:user_id>", methods= ["GET", "POST"])
def search_movie(user_id):
    """Function to implement the movies on searched keyword:"""
    user = session.query(User).get(user_id)
    user_name = user.name
    if request.method== "POST":
        keyword= request.form.get("keyword")
        search_movies_list = session.query(Movie).join(User.movies).filter(User.id==user_id).\
            filter(or_(
            Movie.movie_name.ilike(f"%{keyword}%"),
            Movie.year.ilike(f"%{keyword}%"),
            Movie.director.ilike(f"%{keyword}%"),
        (Movie.rating >= f"{keyword}"))).all()

        if search_movies_list:

            return render_template("search_movie.html",user_name=user_name,keyword=keyword, movies=search_movies_list, user_id=user_id)
        else:
            return render_template("no_movie_found.html", user_id=user_id)

    user_movie_list = user.movie
    return render_template("favourite_movie.html", user_name=user_name, movies=user_movie_list, user_id=user_id)


@app.route("/add_review/<int:user_id>/<int:movie_id>" , methods=["GET","POST"])
def add_review(user_id, movie_id):
    review_movie = movie_review(user_id,movie_id)
    if request.method == "POST":
        review = request.form['review']
        rating =  request.form['rating']
        print(rating, review)
        #user_id = request.headers.get('user_id')
        user = session.query(User).get(user_id)
        movie_to_review = session.query(Movie).get(movie_id)

        new_review = Review(
                    review_text = review if review else None,
                    rating = float(rating) if rating else None,
                    user = user,
                    movie = movie_to_review
                )
        print(new_review.review_text)
        session.add(new_review)
        session.commit()

        return redirect(url_for("add_review", user_id = user_id, movie_id =  movie_id))
    user= session.query(User).get(user_id)
    movie_to_review = session.query(Movie).get(movie_id)
    return render_template("movie_review.html", movie = movie_to_review, user_id= user_id,movie_id=movie_id, reviews = review_movie)

def movie_review(user_id, movie_id):
    reviews = session.query(Review).all()
    movie_reviews = []
    for review in reviews:
        if review.movie.movie_id == movie_id:
            movie_reviews.append(review)
    return movie_reviews


@app.route("/review/<int:review_id>")
def delete_review(review_id):
    # Retrieve the review to delete
    #review_to_delete = session.query(Review).get(review_id)
    review_to_delete = session.query(Review).filter_by(review_id=review_id).first()
    if review_to_delete:
        # Delete the review from the database
        session.delete(review_to_delete)
        session.commit()
    return   redirect(url_for("add_review", user_id = review_to_delete.user_id,
                                  movie_id =  review_to_delete.movie_id))



@app.route("/update/<int:review_id>" , methods=["GET","POST"])
def update_review(review_id):
    review_to_update=  session.query(Review).get(review_id)
    if request.method == "POST":
        review = request.form['review']
        rating = request.form['rating']
        review_to_update.review_text =review if review else None
        review_to_update.rating = rating if rating else None
        session.commit()
        return redirect(url_for("add_review", user_id = review_to_update.user_id,
                                  movie_id =  review_to_update.movie_id))
    user_id = review_to_update.user_id
    return render_template("edit_review.html", movie = review_to_update.movie,user_id= user_id,movie_id=review_to_update.movie_id,
                           review_id = review_to_update.review_id, review = review_to_update)






if __name__ == '__main__':
    #with app.app_context():
     # db.create_all()
    app.run(debug=True)

