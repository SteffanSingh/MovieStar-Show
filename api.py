# api.py
import requests
from flask import Blueprint, jsonify
from data_managers.data_models import  User, Movie,db, Review
from flask import Flask,  render_template, request,redirect,url_for
from sess import  session
import  json


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


