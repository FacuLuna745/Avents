# -*-coding: utf-8 *-*
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy #Incluye sqlAlchemy
from flask_login import LoginManager
from flask_wtf import CSRFProtect #importar para proteccion CSRF
from dotenv import load_dotenv
load_dotenv()
from flask_mail import Mail,Message
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY') #clave secreta
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://'+os.getenv('DB_USERNAME')+':'+os.getenv('DB_PASS')+'@localhost/avent_bd'
app.config['MAIL_HOSTNAME'] = 'localhost'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['FLASKY_MAIL_SENDER'] = 'Avents <aventsSA@noreply.com>'

db = SQLAlchemy(app)
csrf = CSRFProtect(app)
mail = Mail(app)
login_manager = LoginManager(app)

if __name__ == '__main__': #Asegura que solo se ejectue el servidor cuando se ejecute el script directamente
    from route import *
    app.run(port = 8000, debug = True)
