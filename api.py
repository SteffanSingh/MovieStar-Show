# api.py
import requests
from flask import Blueprint, jsonify
from data_managers.data_models import  User, Movie,db, Review
from flask import Flask,  render_template, request,redirect,url_for
from sess import  session
import  json
import jwt
from datetime import  datetime
from werkzeug.security import check_password_hash


#secret key for creating token in jwt
SECRET_KEY = "123456"

api = Blueprint('api', __name__)


@api.route('/userslist', methods=['GET'])
def get_users():
    # Implementation here
    users = session.query(User).all()
    print(users)

    user_list = [{"id":user.id, 'name':user.name,
                  "email":user.email,
                  "password":user.password,
                  "is_admin":user.is_admin
                  } for user in users ]
    print(user_list)
    return user_list


@api.route('/users/<int:user_id>/movies', methods=['GET'])
def get_user_movies(user_id):
    user = session.query(User).get(user_id)
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

    key = "2837c90f"
    url = f"http://www.omdbapi.com/?apikey={key}&t={movie_name}"
    res = requests.get(url)
    response_data = res.json()

    if 'Title' not in response_data:
        return jsonify({'error': 'Movie not found in OMDB database. Please try different movie.'}), 404

    user = session.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    for movie in user.movies:
        if movie.movie_name == response_data["Title"]:
            return jsonify({'message': 'Movie already exists in user movie list.'}), 200
    if response_data['Response'] == "False":
        return jsonify({'message': 'Movie is not found.'}), 200

    existing_movie = session.query(Movie).filter_by(movie_name=response_data["Title"]).first()

    if existing_movie:
        if existing_movie not in user.movies:
            user.movies.append(existing_movie)
            session.commit()  # Commit the session after appending the existing movie
            return jsonify({'message': 'Movie added successfully'}), 201
        else:
            return jsonify({'message': 'Movie already exists in user movie list.'}), 200

    new_movie = Movie(
        movie_name=response_data["Title"],
        director=response_data["Director"],
        rating=response_data["imdbRating"],
        year=response_data["Year"],
        poster=response_data["Poster"],
        note=""
    )

    user.movies.append(new_movie)
    session.add(new_movie)
    session.commit()

    return jsonify({'message': 'Movie added successfully'}), 201

@api.route("/register", methods=["POST"])
def signup():
    """The function to implement the signup component for registration."""
    try:
        data = request.json
        name = data["name"]
        email = data["email"]
        password = data["password"]

        # Check if name is provided and not empty
        if not name:
            return jsonify({"message": "Name cannot be empty!"}), 400

        existing_user = session.query(User).filter_by(email=email).first()
        if existing_user:
            return jsonify({"message": "Email has already been registered!"}), 400

        new_user = User(name=name.title(), email=email, password=password)
        session.add(new_user)
        session.commit()

        current_time = datetime.now().isoformat()

        # Generate user JSON data
        user_json = {
            "id": new_user.id,
            "name": new_user.name,
            "email": new_user.email,
            "createdAt": current_time
            # Add other user details as needed
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

        user = session.query(User).filter_by(email=email).first()

        if not user:
            return jsonify({"message": "Email is not registered yet. Please register."}), 400


        # Here you can return the user details as a JSON response if needed
        user_json = {
            "id": user.id,
            "name":user.name,
            "email": user.email,
            "password": user.password,
            "created_at":str(user.createdAt)
            # Add other user details as needed
        }
        token = jwt.encode(user_json, "123456", algorithm="HS256")
        if user and not check_password_hash(user.password, password):
            return  jsonify({"message": "Password is incorrect!"}), 400
        if user and check_password_hash(user.password, password):
            return jsonify({"message": "Login successful!", "token": token,"user":user_json}), 200

    except Exception as error:
        return jsonify({"message": "An error occurred", "error": str(error)}), 500
