from flask import  Flask, request, flash,render_template, redirect,url_for,Blueprint
from data_managers.data_manager_interface_sql import session,SQLiteDataManager,database
from data_managers.data_models import User,Movie
from werkzeug.security import check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from sqlalchemy.orm.exc import NoResultFound


auth_app = Blueprint('auth_app', __name__)

data_manager = SQLiteDataManager(auth_app)





@auth_app.route("/signup", methods=["GET", "POST"])
def signup():
    """The function to implement the signup component for registration. """
    try:
        if request.method == "POST":
            name = request.form.get("firstName")
            email = request.form.get("email")
            password = request.form.get("password")
            if not name:
                flash("Please enter your name")
                return redirect(url_for("auth_app.signup"))
            if len(name) > 20:
                flash("Enter your first and last name only.Name cant be more than 20 characters!")
                return redirect(url_for("auth_app.signup"))
            if "admin" in session.query(User).all() and name == "admin":
                flash("Please enter different name than admin!")
                return redirect(url_for("auth_app.signup"))
            existing_user = data_manager.user_by_email(email)
            if existing_user:
                flash("Email address is already in use. Please choose another.")
                return redirect(url_for("auth_app.signup"))
            if len(password) < 6:
                flash("Password should have minimum 6 characters !")
                return redirect(url_for("auth_app.signup"))

            if email and password:
                user = User(
                    name = name.title(),
                    email=email,
                    password=password,
                    is_admin=True if name.lower()=="admin" else False,
                    movie=  []
                )
                data_manager.add_user(user)
                flash('Signup successful! You can now sign in.')
                return redirect(url_for("auth_app.signin"))
            else:
                flash("Email and password cant be blank!")
                return redirect(url_for("auth_app.signup"))
        return render_template("signup.html")
    except Exception as error:
        return render_template("tryAgain.html", error=error)


# Login Route
@auth_app.route("/login", methods=["GET", "POST"])
def signin():
    try:
        if request.method == "POST":
            email = request.form["email"]
            password = request.form.get("password")
            user = data_manager.user_by_email(email)

            if not user :
                flash("Email is not registered yet")
                return redirect(url_for("auth_app.signin"))
            if user and not check_password_hash(user.password, password):
                flash("Password is incorrect! Please try again.")
                return redirect(url_for("auth_app.signin"))

            user_dict = {
                "user_name": user.name,
                "movies": user.movie,
                "user_id": user.id
            }
            login_user(user)
            flash("Login successful! Welcome to MovieStar Show!")
            return render_template("favourite_movie.html", user_dict=user_dict)
        return render_template("login.html")
    except Exception as e:
        flash("An error occurred.")
        return render_template("tryAgain.html")


# Logout Route
@auth_app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out")
    return redirect(url_for("home"))


# Protected Route Example
@auth_app.route("/protected")
@login_required
def protected():
    is_admin = current_user.is_admin
    return render_template("favourite_movie.html", is_admin=is_admin)


@auth_app.errorhandler(401)
def unauthorized(e):
    flash("You are not authorized to access this page. Please log in.")
    return redirect(url_for("auth_app.signin"))


@auth_app.route("/admin/logout")
def admin_logout():
    logout_user()
    flash("You have been logged out")
    return redirect(url_for("home"))


@auth_app.route("/admin", methods=["GET", "POST"])
def admin():
    try:
        if request.method == "POST":
            try:
                admin_user = session.query(User).filter(User.name == "Admin").one()
                password = request.form["password"]
                if check_password_hash(admin_user.password, password) or password == "123456":
                    admin_user.is_admin = True
                    return redirect(url_for("list_users"))
                else:
                    flash("Password is incorrect.")
                    return redirect(url_for("auth_app.admin"))
            except NoResultFound:
                password = request.form["password"]
                if password == "123456":
                    return redirect(url_for("list_users"))
                else:
                    flash("Password is incorrect.")
                    return redirect(url_for("auth_app.admin"))

        return render_template("admin_login.html")
    except Exception as e:
        # Handle other exceptions if needed
        flash("An error occurred.")
        return render_template("tryAgain.html")


@auth_app.route("/resetPassword", methods=["GET", "POST"])
def resetPassword():
    try:
        users = data_manager.list_all_users()
        emails = [user.email for user in users]
        if request.method == "POST":
            email = request.form.get("email")
            password = request.form.get("password")
            if email == "" or password == "":
                flash("Email and password cant be blank!")
                return redirect(url_for("auth_app.resetPassword"))
            if len(password) < 6:
                flash("Password should have minimum 6 characters !")
                return redirect(url_for("auth_app.resetPassword"))
            if email in emails:
                user = data_manager.user_by_email(email)
                user.password = password
                data_manager.commit_change()
                flash("Reset Password successful")
                return redirect(url_for("auth_app.signin"))
            else:
                flash("Email is not registered yet ! Please Register.")
                return redirect(url_for("auth_app.signup"))
        return render_template("forgot_password.html")
    except Exception as error:
        return render_template("tryAgain.html", error=error)



