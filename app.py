from data_managers.data_manager_interface_json import SQLiteDataManager
from flask import Flask,  render_template, request,redirect,url_for
from MovieWeb_app.data_managers.data_models import db, User, Movie
import  requests, json

#movie_data = "data/data.json"


app = Flask(__name__)

data_manager = SQLiteDataManager('moviwebapp.sqlite')




@app.route('/')
def home():
    """Function to implement home page of Movie web app"""
    return render_template("home.html")


@app.route("/users")
def list_users():
    """function to display all the users with their favourite movies."""
    users_list = data_manager.get_all_users()
    user_id_list = data_manager.get_all_users_id()
    return render_template("users.html", users = users_list, user_id_list = user_id_list)


@app.route("/users/<int:user_id>")
def user_movie_list(user_id):
    """function to implement the add movie to a particular user with the given id."""
    user_movies = data_manager.get_user_movies(user_id)
    user_list = data_manager.get_all_users()
    user_id_list = data_manager.get_all_users_id()
    #index = user_id_list.index(user_id)
    name = db.session.query(User).filter(User.id == user_id).one()
    return render_template("favourite_movie.html",user_name = name, movies = user_movies, user_id = user_id)


@app.route("/add_user", methods = ["GET","POST"])
def add_user():
    """function to implement the add user in the given user data."""
    if request.method == "POST":
        users = db.session.query(User).all()
        name = request.form['name']
        if name == None:
            return render_template("users.html")
        else:
            data_manager.add_user(name)
            users = db.session.query(User).all()
            return redirect(url_for("list_users"))
    return render_template("add_user.html")

@app.route("/delete_user/<int:user_id>", methods=["GET","DELETE"])
def delete_user(user_id):
    """function to implement to delete user from a given user list."""
    all_user_data = data_manager.get_all_users()
    db.session.query(User).filter(User.id == user_id).delete()
    db.session.commit()
    return redirect(url_for("list_users"))


@app.route("/users/<int:user_id>/add_movie", methods = ["GET","POST"])
def add_user_movie(user_id):
    """function to implement the add movie to particular user with a given user id"""
    users_list = data_manager.get_all_users()
    users_id_list = data_manager.get_all_users_id()
    index = users_id_list.index(user_id)
    user_name = db.session.query(User).filter(User.id == user_id).name

    user_movie_list = data_manager.get_user_movies(user_id)




    if request.method == "POST":
        name = request.form["name"]
        Key = "2837c90f"
        Url = f"http://www.omdbapi.com/?apikey={Key}&t={name}"
        res = requests.get(Url)
        data = res.json()
        if data['Response'] == "False":
            return render_template("movie_not_found.html", user_name = user_name, user_id = user_id)
        for movie in user_movie_list:
            if movie  == data["Title"]:
                return render_template("movie_already_exists.html", user_name=user_name, user_id=user_id)
        movie_name  = data["Title"]
        rating  = data["imdbRating"]
        year  = data["Year"]
        director  = data["Director"]

        poster  = data["Poster"]
        note  = " "
        movie = Movie(
            movie_name = name,
            director = director,
            rating = rating,
            year  = year,
            poster = poster,
            note = note
        )



        for user in users_list:
            if user_id not in users_id_list:
                return render_template("users.html")
            elif user_id in users_id_list:
                data_manager.add_movie(movie)

                return redirect(url_for("user_movie_list",user_id=user_id))
    return render_template("add_movie.html", user_id=user_id)


@app.route("/users/<int:user_id>/update_movie/<int:movie_id>", methods=["GET", "POST"])
def update_movie(user_id, movie_id):
    """function to implement the update the movie details with the given movie id for a
        particular user with a given user id."""
    users_list = data_manager.get_all_users()
    users_id_list = data_manager.get_all_users_id()
    index = users_id_list.index(user_id)
    user_name = db.session.query(User).filter(User.id == user_id).name

    #movies = data_manager.get_user_movies_name_list(user_id)
    user_movie_list = data_manager.get_user_movies(user_id)
    movie_to_update = db.session.query(Movie).filter(Movie.user_id == user_id).one()
    if request.method == "POST":
        rating = request.form["rating"]
        note = request.form["note"]
        for index, movie in enumerate(user_movie_list):
            if int(movie["movie_id"]) == movie_id:
                movie_to_update.rating = rating
                movie_to_update.note  = note
                db.session.commit()
                return render_template("favourite_movie.html", user_name=user_name, user_id=user_id,movie_id=movie_id, movies = user_movie_list)
    return render_template("update.html", user_name=user_name,movie_id=movie_id, movies=user_movie_list, user_id=user_id)


@app.route("/users/<int:user_id>/delete_movie/<int:movie_id>")
def delete_movie(user_id, movie_id):
    """function to implement to delete a movie with a given id for a given user"""

    users_list = data_manager.get_all_users()
    users_id_list = data_manager.get_all_users_id()
    user_name = db.session.query(User).filter(User.id == user_id).name
    user_movie_list = data_manager.get_user_movies(user_id)
    for movie in user_movie_list:
        if int(movie.movie_id) == movie_id:
            db.session.query(Movie).filter(Movie.user_id == user_id)

            return redirect(url_for("user_movie_list", user_id = user_id))

    return render_template("favourite_movie.html", user_name = user_name, movies = user_movie_list, user_id = user_id)



if __name__ == '__main__':
    app.run(debug=True)

