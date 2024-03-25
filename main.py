from flask import Flask
from data_managers.data_models import db
from data_managers.data_manager_interface_sql import SQLiteDataManager, database
from Authentication.authentication import auth_app
from flask_login import LoginManager



app = Flask(__name__)
app.secret_key = '123456'
# Blueprint for Authentication logics
app.register_blueprint(auth_app)

login_manager = LoginManager()
login_manager.init_app(app)

# Database configuration
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = database
db.init_app(app)  # Initializing the app

# Creating instance of SQLiteDataManager
data_manager = SQLiteDataManager(app)


@login_manager.user_loader
def load_user(user_id):
    user = data_manager.get_user(user_id)
    if user:
        return user
    else:
        return  None