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
app.secret_key = os.getenv('SECRET_KEY') #clave secreta, se utiliza para que ninguna API se haga pasar por nosotros
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True #Configuracion para que el ORM (Mapeo de objeto relacional) detecte las modificaciones que realicemos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://'+os.getenv('DB_USERNAME')+':'+os.getenv('DB_PASS')+'@localhost/avent_bd' #Se establece la conexion a nuestra base de datos
app.config['MAIL_HOSTNAME'] = 'localhost' #Direccion del servidor mail utilizado
app.config['MAIL_SERVER'] = 'smtp.googlemail.com' #Se establece la direccion del servidor en este caso es la de google
app.config['MAIL_PORT'] = 587 #Puerto del servidor mail saliente SMTP
app.config['MAIL_USE_TLS'] = True #Protocolos de seguridad del servidor SSL/TLS
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME') #Configuracion del mail desde donde se responde al usuario para que no quede hardcodeado en el codigo
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD') #Contraseña del mail
app.config['FLASKY_MAIL_SENDER'] = 'Avents <aventsSA@noreply.com>'

db = SQLAlchemy(app) #Creamos el objeto que tiene todas las funcionalidades del ORM (mapeo de objeto relacional)
csrf = CSRFProtect(app)# Es util usar un token CSRF, permite que nuestra aplicación haga las peticiones desde nuestro sitio.
# En esta linea estamos Instanciando el modulo de flask que nos permite esta funcionalidad
mail = Mail(app) #Creamos el objetos que tiene las funcionalidades de los mail.
login_manager = LoginManager(app)# Instanciamos el objeto del modulo Flask Login llamado login manager el cual nos permite operar con las sesiones

if __name__ == '__main__': #Asegura que solo se ejectue el servidor cuando se ejecute el script directamente
    from route import *
    from route_api import *
    from error import *
    app.run(port = 8000, debug = True)
