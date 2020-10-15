
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager



app = Flask(__name__)


app.secret_key = 'asdfcnvbg*shadowwhite*hkjsdhfkj'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/cguide'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'sign_in'
login_manager.login_message_category = 'info'

from career_guide import routes