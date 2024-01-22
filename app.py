from flask import Flask, jsonify,render_template,request,redirect, url_for
from data_managers.data_manager_interface_json import JSONDataManager
import  json
import  requests


movie_data = "data/data.json"


app = Flask(__name__)

data_manager = JSONDataManager(movie_data)


def read_data():
    with open("data/data.json", "r") as fileObject:
        data = json.loads(fileObject.read())
    return data


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
    index = user_id_list.index(user_id)
    name = user_list[index]
    return render_template("favourite_movie.html",user_name =name, movies = user_movies, user_id=user_id)


@app.route("/add_user", methods = ["GET","POST"])
def add_user():
    """function to implement the add user in the given user data."""
    if request.method == "POST":
        users = read_data()
        name = request.form['name']
        if name == None:
            return render_template("users.html")
        else:
            users_id_list = data_manager.get_all_users_id()
            user = {}
            id = max(users_id_list) + 1
            user['name'] = name
            users[str(id)] = user
            user["movies"]=[]
            user_list = data_manager.get_all_users()
            user_list.append(name)
            with open("data/data.json", "w") as fileObject:
                fileObject.write(json.dumps(users, indent=4))
            return redirect(url_for("list_users"))
    return render_template("add_user.html")

@app.route("/delete_user/<int:user_id>", methods=["GET","DELETE"])
def delete_user(user_id):
    """function to implement to delete user from a given user list."""
    all_user_data = read_data()
    if str(user_id) in list(all_user_data.keys()):
        all_user_data.pop(str(user_id))
    with open("data/data.json", "w") as fileObject:
        fileObject.write(json.dumps(all_user_data, indent=4))
    return redirect(url_for("list_users"))


@app.route("/users/<int:user_id>/add_movie", methods = ["GET","POST"])
def add_user_movie(user_id):
    """function to implement the add movie to particular user with a given user id"""
    users_list = data_manager.get_all_users()
    users_id_list = data_manager.get_all_users_id()
    index = users_id_list.index(user_id)
    user_name = users_list[index]
    users = read_data()
    user_movie_list = data_manager.get_user_movies(user_id)
    user = {}
    movie = {}
    movie_id_list = []

    for movie in user_movie_list:
        movie_id_list.append(movie["movie_id"])

    if request.method == "POST":
        name = request.form["name"]
        Key = "2837c90f"
        Url = f"http://www.omdbapi.com/?apikey={Key}&t={name}"
        res = requests.get(Url)
        data = res.json()
        if data['Response'] == "False":
            return render_template("movie_not_found.html", user_name=user_name,user_id=user_id)
        for movie in user_movie_list:
            if movie["movie_name"] == data["Title"]:
                return render_template("movie_already_exists.html", user_name=user_name, user_id=user_id)
        movie["movie_name"] = data["Title"]
        movie["rating"] = data["imdbRating"]
        movie["year"] = data["Year"]
        movie["director"] = data["Director"]
        movie["movie_id"] = max(movie_id_list) + 1
        movie["poster"]= data["Poster"]
        movie["note"]=[]


        for user in users_list:
            if user_id not in users_id_list:
                return render_template("users.html")
            elif user_id in users_id_list:
                users[str(user_id)]["movies"].append(movie)
                with open("data/data.json", "w") as fileObject:
                    fileObject.write(json.dumps(users, indent=4))
                return redirect(url_for("user_movie_list",user_id=user_id))
    return render_template("add_movie.html", user_id=user_id)



@app.route("/users/<int:user_id>/update_movie/<int:movie_id>", methods=["GET", "POST"])
def update_movie(user_id, movie_id):
    """function to implement the update the movie details with the given movie id for a
        particular user with a given user id."""
    users_list = data_manager.get_all_users()
    users_id_list = data_manager.get_all_users_id()
    index = users_id_list.index(user_id)
    user_name = users_list[index]
    users = read_data()
    user_movie_list = data_manager.get_user_movies(user_id)
    if request.method == "POST":
        rating = request.form["rating"]
        note = request.form["note"]
        for index,movie in enumerate(user_movie_list):
            if int(movie["movie_id"]) == movie_id:
                movie["rating"] = rating
                movie["note"] = note
                users[str(user_id)]["movies"][index].update(movie)

                with open("data/data.json", "w") as fileObject:
                    fileObject.write(json.dumps(users, indent=4))
                return render_template("favourite_movie.html", user_name=user_name, user_id=user_id,movie_id=movie_id, movies=user_movie_list)
    return render_template("update.html", user_name=user_name,movie_id=movie_id, movies=user_movie_list, user_id=user_id)


@app.route("/users/<int:user_id>/delete_movie/<int:movie_id>")
def delete_movie(user_id, movie_id):
    """function to implement to delete a movie with a given id for a given user"""

    users_list = data_manager.get_all_users()
    users_id_list = data_manager.get_all_users_id()
    index = users_id_list.index(user_id)
    user_name = users_list[index]
    users = read_data()
    user_movie_list = data_manager.get_user_movies(user_id)
    for movie in user_movie_list:
        if int(movie["movie_id"]) == movie_id:
            users[str(user_id)]["movies"].remove(movie)
            with open("data/data.json", "w") as fileObject:
                fileObject.write(json.dumps(users, indent=4))
            return redirect(url_for("user_movie_list",user_id=user_id))

    return render_template("favourite_movie.html", user_name=user_name, movies=user_movie_list, user_id=user_id)



if __name__ == '__main__':
    app.run(debug=True)

