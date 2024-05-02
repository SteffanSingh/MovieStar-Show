from flask import Blueprint, jsonify
from data_managers.data_models import  User, Movie
from flask import request
from reusable_functions.movie_fetch import movie_fetch
import jwt
from datetime import  datetime
from werkzeug.security import check_password_hash
from main import  data_manager


#secret key for creating token in jwt
SECRET_KEY = "123456"

api = Blueprint('api', __name__)


@api.route('/userslist', methods=['GET'])
def get_users():
    # Implementation here
    users = data_manager.list_all_users()
    print(users)
    user_list = [{"id":user.id, 'name':user.name,
                  "email":user.email,
                  "password":user.password,
                  "is_admin":user.is_admin
                  } for user in users ]
    print(user_list)
    return jsonify(user_list)


@api.route('/users/<int:user_id>/movies', methods=['GET'])
def get_user_movies(user_id):
    user = data_manager.get_user(user_id)
    print(user)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    user_movies_list = [{'movie_id': movie.movie_id,
                         'movie_name': movie.movie_name,
                         'director': movie.director,
                         'poster': movie.poster,
                         'rating': movie.rating,
                         'year': movie.year,
                         'note': movie.note
                         } for movie in user.movie]
    if not user_movies_list:  # Check if the user has no movies
        return jsonify({'message': 'User has no movies yet'}), 200

    return jsonify(user_movies_list), 200


@api.route('/users/<int:user_id>/movie', methods=['POST'])
def add_user_movie(user_id):
    data = request.json
    if not data or 'movie_name' not in data:
        return jsonify({'error': 'Missing or invalid data in the request'}), 400
    movie_name = data["movie_name"]
    response_data = movie_fetch(movie_name)
    if 'Title' not in response_data:
        return jsonify({'error': 'Movie not found in OMDB database. Please try different movie.'}), 404
    user = data_manager.get_user(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    if response_data['Response'] == "False":
        return jsonify({'message': 'Movie is not found.'}), 200
    existing_movie = data_manager.movie_exist_or_not(response_data["Title"])
    if existing_movie:
        if existing_movie not in user.movie:
            user.movie.append(existing_movie)
            data_manager.commit_change()  # Commit the session after appending the existing movie
            return jsonify({'message': 'Movie added successfully'}), 201
        else:
            return jsonify({'message': 'Movie already exists in user movie lists.'}), 200
    new_movie = Movie(
        movie_name=response_data["Title"],
        director=response_data["Director"],
        rating=response_data["imdbRating"],
        year=response_data["Year"],
        poster=response_data["Poster"],
        note=""
    )
    user.movie.append(new_movie)
    data_manager.add_movie(new_movie)
    return jsonify({'message': 'Movie added successfully'}), 201


@api.route("/register", methods=["POST"])
def signup():
    """The function to implement the signup component for registration."""
    try:
        data = request.json
        name = data["name"]
        email = data["email"]
        password = data["password"]
        if not name:
            return jsonify({"message": "Name cannot be empty!"}), 400
        existing_user = data_manager.user_by_email(email)
        if existing_user:
            return jsonify({"message": "Email has already been registered!"}), 400
        new_user = User(
            name=name.title(),
            email=email,
            password=password
        )
        data_manager.add_user(new_user)
        current_time = datetime.now().isoformat()
        user_json = {
            "id": new_user.id,
            "name": new_user.name,
            "email": new_user.email,
            "createdAt": current_time
        }
        return jsonify({"message": "Registration is successful!", "user": user_json}), 200
    except Exception as error:
        return jsonify({"message": "An error occurred", "error": str(error)}), 500



@api.route("/login", methods=["POST"])
def signin():
    """The function to implement the sign-in component to check user and password."""
    try:

        data = request.json
        email = data["email"]
        password = data["password"]
        if not email or not password:
            return jsonify({"message": "Email and password cannot be blank"}), 400

        user = data_manager.user_by_email(email)
        if not user:
            return jsonify({"message": "Email is not registered yet. Please register."}), 400


        user_json = {
            "id": user.id,
            "name":user.name,
            "email": user.email,
            "password": user.password,
            "created_at":str(user.createdAt)

        }
        token = jwt.encode(user_json, "123456", algorithm="HS256")
        if user and not check_password_hash(user.password, password):
            return  jsonify({"message": "Password is incorrect!"}), 400
        if user and check_password_hash(user.password, password):
            return jsonify({"message": "Login successful!", "token": token,"user":user_json}), 200

    except Exception as error:
        return jsonify({"message": "An error occurred", "error": str(error)}), 500
