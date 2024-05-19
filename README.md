# MovieStar Show

MovieStar Show is a web application for managing and browsing a collection of movies. Users can add, update, delete, and view movies. The application also allows for sorting movies based on various criteria such as name, rating, and year.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)
- [Demo](#demo)

## Features

- User authentication and authorization
- Add, update, delete, and view movies
- Search for movies
- Sort movies by name, rating, and year
- Movies recommendation based on interests
- Email notifications for various actions

## Installation

### Prerequisites

- Python 3.7+
- Flask
- SQLAlchemy
- Flask-Login
- Flask-Bootstrap
- Other dependencies listed in `requirements.txt`

### Steps

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

Check out the [project demo video ](https://www.youtube.com/watch?v=aiZVlWMnHu8) to see the MovieStar Show application in action.

### Project Demo Images

<p align="center">
  <img src="https://github.com/SteffanSingh/MovieStar-Show/blob/48d4588760a33c2da88f8bff57e5ecb49c0864f7/Project%20images/movieStarshow1.png" alt="MovieStar Show Home Page">
  <img src="https://github.com/SteffanSingh/MovieStar-Show/blob/48d4588760a33c2da88f8bff57e5ecb49c0864f7/Project%20images/movieStarshow2details.png" alt="Movie Details Page">
  <img src="https://github.com/SteffanSingh/MovieStar-Show/blob/48d4588760a33c2da88f8bff57e5ecb49c0864f7/Project%20images/movieStarshow3.png" alt="Movie Recommendation Page">
  <img src="https://github.com/SteffanSingh/MovieStar-Show/blob/819df23a04e61b15bac652be41cf704bee196550/MovieWebPictures/welcomeEmail.png" alt="Welcome Email">
  <img src="https://github.com/SteffanSingh/MovieStar-Show/blob/819df23a04e61b15bac652be41cf704bee196550/MovieWebPictures/movieRecommend.png" alt="Email Recommendation Page">
</p>
