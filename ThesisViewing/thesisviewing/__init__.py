from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config["SECRET_KEY"] = 'f5418130a27f18abe557d61201c31d60'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/ThesisViewing'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from thesisviewing import routes