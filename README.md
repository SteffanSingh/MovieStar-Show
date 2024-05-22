# MovieStar Show

MovieStar Show is a web application for managing and browsing a collection of movies. Users can add, update, delete, and view movies. The application also allows for sorting movies based on various criteria such as name, rating, and year.

## Table of Contents

- [Introduction](#introduction)
- [Description](#description)
- [Project Structure](#project-structure)
- [Features](#features)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Installation Steps](#installation-steps)
- [Usage](#usage)
- [Deployment](#deployment)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)
- [Demo](#demo)

## Introduction

Welcome to MovieStar Show, a web application for managing and browsing a collection of movies. Users can add, update, delete, and view movies, as well as sort them based on various criteria such as name, rating, and year.

- **User Authentication:** Secure signup, login, and password reset functionalities.
- **Search Functionality:** Search for movies by title, rating, and year.
- **Sorting:** Sort movies for a particular user by name, rating, and year.
- **Technologies Used:** Python, Flask, SQLAlchemy, Jinja2, HTML, CSS.

## Description

MovieStar Show is designed to help users manage their movie collections. The application allows users to add, update, delete, and view movie details, search for movies, and sort them by various criteria.

## Project Structure

The MovieStar Show project is structured as follows:

- `.authentication`: Contains the Python files for user signup, login, and password reset.
- `.data`: Contains the SQLite database file and other data files.
- `.data_manager`: Includes data management modules for handling movie data and queries.
- `.implementation`: Contains the implementation Python files for users, movies, and recommendations.
- `.static`: CSS files and image/icon assets.
- `.templates`: HTML templates for web pages.
- `app.py`: The main application file that connects routes and manages error handling.

## Features

- User authentication and authorization
- Add, update, delete, and view movies
- Search for movies
- Sort movies by name, rating, and year
- Movie recommendations based on user interests
- Email notifications for various actions

## Installation

### Prerequisites

- Python 3.7+
- Flask
- SQLAlchemy
- Flask-Login
- Flask-Bootstrap
- Other dependencies listed in `requirements.txt`

### Installation Steps

1. Clone the repository:

    ```bash
    git clone https://github.com/SteffanSingh/MovieStar-Show.git
    cd MovieStar-Show
    ```

2. Create a virtual environment and activate it:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up the database:

    ```bash
    flask db init
    flask db migrate
    flask db upgrade
    ```

5. Run the application:

    ```bash
    flask run
    ```

## Usage

1. Open your web browser and navigate to `http://127.0.0.1:5000`.
2. Create an account or log in if you already have one.
3. Use the navigation menu to add, update, delete, or view movies.
4. Use the search bar to find movies.
5. Sort movies using the dropdown menu.

## Deployment

The MovieStar Show application is currently deployed on PythonAnywhere. You can access the live version of the application at [https://moviestarshow.pythonanywhere.com/](https://moviestarshow.pythonanywhere.com/).

## API Endpoints

### User Endpoints

- **GET /users/<int:user_id>**
  - Get user details.

- **POST /users/<int:user_id>/add_movie**
  - Add a new movie for the user.

- **POST /users/<int:user_id>/update_movie/<int:movie_id>**
  - Update details of an existing movie.

- **GET /users/<int:user_id>/delete_movie/<int:movie_id>**
  - Delete a movie for the user.

### Sorting Movies

- **GET /sort/<int:user_id>**
  - Sort movies by name, rating, or year.

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature/YourFeature`).
6. Open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Demo

### Project Demo Video

Check out the [project demo video](https://www.youtube.com/watch?v=aiZVlWMnHu8) to see the MovieStar Show application in action.

### Project Demo Images

<p align="center">
  <img src="https://github.com/SteffanSingh/MovieStar-Show/blob/48d4588760a33c2da88f8bff57e5ecb49c0864f7/Project%20images/movieStarshow1.png" alt="MovieStar Show Home Page">
  <img src="https://github.com/SteffanSingh/MovieStar-Show/blob/48d4588760a33c2da88f8bff57e5ecb49c0864f7/Project%20images/movieStarshow2details.png" alt="Movie Details Page">
  <img src="https://github.com/SteffanSingh/MovieStar-Show/blob/48d4588760a33c2da88f8bff57e5ecb49c0864f7/Project%20images/movieStarshow3.png" alt="Movie Recommendation Page">
  <img src="https://github.com/SteffanSingh/MovieStar-Show/blob/819df23a04e61b15bac652be41cf704bee196550/MovieWebPictures/welcomeEmail.png" alt="Welcome Email">
  <img src="https://github.com/SteffanSingh/MovieStar-Show/blob/819df23a04e61b15bac652be41cf704bee196550/MovieWebPictures/movieRecommend.png" alt="Email Recommendation Page">
</p>
