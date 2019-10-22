# -*-coding: utf-8 *-*
from flask import Flask
from flask_sqlalchemy import SQLAlchemy #Incluye sqlAlchemy
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#Configuración de conexion de base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:fl39131256@localhost/avent_bd'
#Instancia que representa la base de datosapp
db = SQLAlchemy(app)

app.secret_key = 'topsecret'  # clave secreta

#Instalar SQLAlchemy con:
#pip install Flask-SQLAlchemy
#Instalar controlador para MySQL
# pip install Flask-pymysql

if __name__ == '__main__': #Asegura que solo se ejectue el servidor cuando se ejecute el script directamente
    from route import *
    app.run(port = 8000, debug = True)
