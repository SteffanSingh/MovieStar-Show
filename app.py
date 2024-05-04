from flask import render_template, redirect, url_for, request, flash, abort
from sqlalchemy import or_
from data_managers.data_models import User,Movie,Review,db
from data_managers.data_manager_interface_sql import session
from main import app, data_manager
from reusable_functions.movie_fetch import movie_fetch
from api import api
from flask_cors import  CORS
import asynchat
import asyncore


app.register_blueprint(api, url_prefix='/api')
CORS(app, origins='http://localhost:3000')

@app.route('/')
def home():
    """Function to implement home page of Movie web app"""
    return render_template("home.html")


@app.route('/users')
def list_users():
    """function to display all the users with their favourite movies."""
    try:
        users = data_manager.list_all_users()
        return render_template('users.html', users=users)
    except Exception as error:
        return render_template("tryAgain.html" )


def user_dictionary(user_id):
    user = data_manager.get_user(user_id)
    user_dict = {
        "user_name": user.name,
        "movies": user.movie,
        "user_id": user_id,
    }
    if user:
        return user_dict
    else:
        return {}

@app.route("/users/<int:user_id>")
def user_movies_list(user_id):
    """function to implement the add movie to a particular user with the given id."""
    try:
        user_dict= user_dictionary(user_id)
        return render_template("favourite_movie.html", user_dict=user_dict )
    except Exception as error:
        return render_template("tryAgain.html", error=error)


@app.route("/add_user", methods= ["GET", "POST"])
def add_user():
    """function to implement the add user in the given user data."""
    try:
        if request.method == "POST":
            name = request.form.get("name")
            email = request.form.get("email")
            password = request.form.get("password")
            if name == "":
                flash("Name cant be empty!")
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
                    is_admin=True if name.lower()=="admin" else False,
                    movie=  []
                )
            data_manager.add_user(user)
            return redirect(url_for("list_users"))
        return render_template("add_user.html")
    except Exception as error:
        return render_template("tryAgain.html", error=error)


@app.route("/delete_user/<int:user_id>", methods=["GET", "DELETE"])
def delete_user(user_id):
    """function to implement to delete user from a given user list."""
    try:
        user = data_manager.get_user(user_id)
        if not user:
            return render_template("tryAgain.html", error="User not found")
        data_manager.delete_user(user_id)
        return redirect(url_for("list_users"))
    except Exception as error:
        return render_template("tryAgain.html", error=error)


@app.route("/users/<int:user_id>/add_movie", methods=["GET", "POST"])
def add_user_movie(user_id):
    """Function to implement adding a movie to a particular user with a given user id"""
    try:
        user = data_manager.get_user(user_id)
        user_name = user.name
        if not user:
            return render_template("user_not_found.html")

        if request.method == "POST":
            name = request.form["name"]
            data = movie_fetch(name)
            if data['Response'] == "False":
                return render_template("movie_not_found.html", user_name=user.name, user_id=user_id)
            existing_movie = data_manager.movie_exist_or_not(data["Title"])
            if existing_movie:
                if existing_movie not in user.movie:
                    user.movie.append(existing_movie)
                    data_manager.commit_change()
                    return redirect(url_for("user_movies_list", user_id=user_id))
                else:
                    return render_template("movie_already_exists.html", user_name=user.name, user_id=user_id)
            movie = Movie(
                movie_name=data["Title"],
                director=data["Director"],
                rating=data["imdbRating"] if data["imdbRating"] != "N/A" else None,
                year=data["Year"],
                poster=data["Poster"],
                note=""
            )
            user.movie.append(movie)
            data_manager.add_movie(movie)
            return redirect(url_for("user_movies_list", user_id=user_id))
        return render_template("add_movie.html", user_id=user_id, user_name=user_name)
    except Exception as error:
        return render_template("tryAgain.html", error=error)



@app.route("/users/<int:user_id>/update_movie/<int:movie_id>", methods=["GET", "POST"])
def update_movie(user_id, movie_id):
    """function to implement the update the movie details with the given movie id for a
        particular user with a given user id."""
    try:
        users_list = data_manager.list_all_users()
        user = data_manager.get_user(user_id)
        user_name = user.name
        user_movie_list = user.movie
        movie_to_update = data_manager.get_movie(movie_id)
        movie_name = movie_to_update.movie_name
        user_dict = user_dictionary(user_id)
        user_dict["movie_id"] = movie_id
        if request.method == "POST":
            rating = request.form["rating"]
            note = request.form["note"]
            for index, movie in enumerate(user_movie_list):
                if int(movie.movie_id) == movie_id:
                    movie_to_update.rating = rating if rating else 0
                    movie_to_update.note = note if note else ""
                    data_manager.commit_change()
                    return render_template("favourite_movie.html", user_dict=user_dict)
        return render_template("update.html", movie_name=movie_name, user_dict=user_dict)
    except Exception as error:
        return render_template("tryAgain.html", error=error)


@app.route("/users/<int:user_id>/delete_movie/<int:movie_id>")
def delete_movie(user_id, movie_id):
    """function to implement to delete a movie with a given id for a given user"""
    try:
        users_list = data_manager.list_all_users()
        user_dict =user_dictionary(user_id)
        movie = data_manager.get_movie(movie_id)
        user= data_manager.get_user(user_id)
        if movie not in user.movie:
            return render_template("no_movie_found.html", user_dict=user_dict)
        if movie:
            user.movie.remove(movie)
            data_manager.commit_change()
        return redirect(url_for("user_movies_list", user_id=user_id))
    except Exception as error:
        return render_template("tryAgain.html", error=error)



@app.route("/sort/<int:user_id>", methods=["GET", "POST"])
def sort_movies(user_id):
    """Function to sort the movie in """
    try:
        user = data_manager.get_user(user_id)
        sorted_movie_list_by_movie_name_ascending = data_manager.sort_by_movie_name_ascending(user_id)
        sorted_movie_list_by_movie_year_descending = data_manager.sort_by_movie_year_descending(user_id)
        sorted_movie_list_by_rating = data_manager.sort_by_movie_rating_descending(user_id)
        sort_by= request.args.get("sort_by")
        if sort_by == "name":
            sorted_movie_list= sorted_movie_list_by_movie_name_ascending
        elif sort_by== "rating":
            sorted_movie_list= sorted_movie_list_by_rating
        elif sort_by == "year":
            sorted_movie_list= sorted_movie_list_by_movie_year_descending
        else:
            sorted_movie_list = []
        user_dict= user_dictionary(user_id)
        user_dict["sort_by"] = sort_by
        user_dict["movies"]= sorted_movie_list
        return render_template("favourite_movie.html", user_dict=user_dict)
    except Exception as error:
        return render_template("tryAgain.html", error=error)


@app.route("/search/<int:user_id>", methods=["GET", "POST"])
def search_movie(user_id):
    """Function to implement the movies on searched keyword:"""
    try:
        user_dict= user_dictionary(user_id)
        if request.method == "POST":
            keyword = request.form.get("keyword")
            search_movies_list = data_manager.search_movie(user_id, keyword)
            user_dict["keyword"] = keyword
            user_dict["movies"]= search_movies_list
            if search_movies_list:
                return render_template("search_movie.html", user_dict=user_dict)
            else:
                return render_template("no_movie_found.html", user_dict=user_dict)
        return render_template("favourite_movie.html", user_dict=user_dict)
    except Exception as error:
        return render_template("tryAgain.html", error=error)


@app.route("/add_review/<int:user_id>/<int:movie_id>", methods=["GET", "POST"])
def add_review(user_id, movie_id):
    """function to add the review for a particular user id and movie id:"""
    try:
        review_movie = data_manager.list_all_reviews(movie_id)
        user = data_manager.get_user(user_id)
        movie_to_review = data_manager.get_movie(movie_id)
        review_dict = {
            "movie_id": movie_id,
            "user_id": user_id,
            "movie":movie_to_review,
            "reviews":review_movie
        }
        movie= movie_to_review
        reviews = review_movie
        if request.method == "POST":
            review = request.form['review']
            rating = request.form['rating']
            if review == "":
                flash("Please enter your review")
                return redirect(url_for("add_review", user_id=user_id, movie_id=movie_id))
            review_movie = data_manager.list_all_reviews(movie_id)
            user = data_manager.get_user(user_id)
            new_review = Review(
                review_text=review if review else None,
                rating=float(rating) if rating else 0,
                user=user,
                movie=movie_to_review
            )
            data_manager.add_review(new_review)
            return redirect(url_for("add_review", user_id=user_id, movie_id=movie_id))
        return render_template("movie_review.html", review_dict=review_dict, movie= movie_to_review,reviews=review_movie)
    except Exception as error:
        return render_template("tryAgain.html", error=error)


@app.route("/review/<int:review_id>")
def delete_review(review_id):
    """function to implement the deletion of particular review"""
    try:
        review_to_delete = data_manager.get_review(review_id)
        print(review_to_delete.movie_id, review_to_delete.user_id)
        if review_to_delete:
            data_manager.delete_review(review_to_delete)
            return redirect(url_for("add_review", user_id=review_to_delete.user_id,movie_id=review_to_delete.movie_id))
    except Exception as error:
        return render_template("tryAgain.html", error=error)


@app.route("/update/<int:review_id>", methods=["GET", "POST"])
def update_review(review_id):
    """Function to implement the update of review."""
    try:
        review_to_update = data_manager.get_review(review_id)
        if review_to_update is None:
            abort(404)
        if request.method == "POST":
            review = request.form.get('review')
            rating = request.form.get('rating')
            if review == "" or review is None:
                flash("Please enter your review")
                return redirect(url_for("update_review", review_id=review_id))
            if review is not None:
                review_to_update.review_text = review
            review_to_update.rating = rating if rating else 0
            data_manager.commit_change()
            return redirect(url_for("add_review", user_id=review_to_update.user_id,movie_id=review_to_update.movie_id))
        return render_template("edit_review.html", movie=review_to_update.movie, review=review_to_update)

    except Exception as error:
        return render_template("tryAgain.html", error=error)


if __name__ == '__main__':
    #with app.app_context():
     #   db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)

