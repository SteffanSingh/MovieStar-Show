# api.py
from flask import Blueprint, jsonify
from MovieWeb_app.data_managers.data_models import  User, Movie,db, Review
from flask import Flask,  render_template, request,redirect,url_for, session




api = Blueprint('api', __name__)

@api.route('/users', methods=['GET'])
def get_users():
    # Implementation here
    users = User.query.all()
    user_list = [{id:user.id, 'name':user.name} for user in users ]
    return jsonify(user_list)


@api.route('/users/<int:user_id>/movies', methods=['GET'])
def get_user_movies(user_id):
    user = db.session.query(User).get(user_id)

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


@api.route('/users/<user_id>/movie', methods=['POST'])
def add_user_movie(user_id):
    data = request.json
    print(data["movie_name"], data["director"], data["rating"])
    if 'movie_name' not in data:
        return jsonify({'error': 'Missing movie_name field'}), 400
    movie_name = data["movie_name"]
    #movie = db.session.query(Movie).filter_by(movie_name=movie_name).first()
    user = db.session.query(User).filter(User.id == user_id).first()
    if user:
        new_movie = Movie(
            movie_name = movie_name,
            director= data["director"],
            rating= data["rating"],
            year = data["year"],
            poster = data["poster"],
            note = data["note"]
        )

        user.movie.append(new_movie)
        db.session.add(new_movie)
        db.session.commit()
        return jsonify({'message': 'Movie added successfully'}), 201
    else:
        return jsonify({'error': 'User not found'}), 404

