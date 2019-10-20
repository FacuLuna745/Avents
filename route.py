#-*-coding: utf-8 *-*
import datetime
import os.path
from random import randint
from run import app, db
from flask import Flask
from flask import flash  # importar para mostrar mensajes flash
from flask import redirect, url_for  # importar para permitir redireccionar y generar url
from flask import render_template
from flask_wtf import CSRFProtect
from werkzeug.utils import secure_filename
from forms import Register, Login, CreateEvent, Filter  # importar clase de formulario
from functions import *
from models import *
from sqlalchemy import or_

csrf = CSRFProtect(app)  # Iniciar protección CSRF
app.secret_key = 'topsecret'  # clave secreta


# Función que muestra los datos obtenidos del envío de formulario
def show_data(formRegister):
    print(formRegister.nombre.data)
    print(formRegister.apellido.data)
    print(formRegister.password.data)


#-----------------------INICIO------------------------------------------------------------------------
@app.route('/',methods=["POST","GET"])
def index():
    title = "Avents"
    user = 'nolog'
    formFilter = Filter()
    listevent = list_event()#consultar eventos en bd
    return render_template('cont_index.html', listevent=listevent, user=user, title=title, formFilter=formFilter)


@app.route('/my-event')
def my_event():
    user = 'log'
    title = "Avents-MyEvent"
    listevent = list_event()
    return render_template('cont_myevent.html', title=title, listevent=listevent, user=user,id=id)

#------------------------------------USUARIO-----------------------------------------------
@app.route('/register')
def register():
    user = 'nolog'
    formRegister = Register()
    title = "Avents-Register"
    return render_template('register.html', title=title, user=user, formRegister=formRegister)


@app.route('/insert', methods=["POST", "GET"])
def insert():
    formRegister = Register()  # Instanciar formRegister de registro
    if formRegister.validate_on_submit():  # Si el formRegister ha sido enviado y es validado correctamente
        flash('Usuario registrado exitosamente', 'success')  # Mostrar mensaje
        users = User(nombre=formRegister.nombre.data,
                     apellido=formRegister.apellido.data,
                     email=formRegister.email.data,
                     password=formRegister.password.data,
                     admin=0)
        insert_db(users)
        return redirect(url_for('index'))  # Redirecciona a la página principal
    elif formRegister.is_submitted():
        flash('Error en la carga de datos', 'danger')  # Mostrar mensaje
    return render_template('register.html', formRegister=formRegister)


@app.route('/login')
def login():
    user = 'nolog'
    formLogin = Login()
    title = "Avents-Login"
    return render_template('login.html', title=title, user=user, formLogin=formLogin)


@app.route('/loginuser', methods=["POST"])
def loginuser():
    formLogin = Login()  # Instanciar formulario de Login
    if formLogin.validate_on_submit():  # Si el formulario ha sido enviado y es validado correctamente
        print(formLogin.emailLogin.data)
        print(formLogin.passwordLogin.data)
        # Verifica que el usuario y pass sean correctos
        if formLogin.emailLogin.data == "luna@mail.com" and formLogin.passwordLogin.data == "12345":
            flash('Login realizado correctamente', 'success')  # Mostrar mensaje
            return redirect(url_for('index'))  # Redirecciona a la página principal}
        else:
            flash('Login incorrecto', 'danger')  # Mostrar mensaje de error
            return redirect(url_for('index'))  # Redirecciona a la página principal
    else:
        flash('Formato del email incorrecto', 'danger')
        return redirect(url_for('index'))  # Redirecciona a la página principal
    return render_template('cont_index.html', formLogin=formLogin)

#------------------------------------------EVENTOS---------------------------------------------------
@app.route('/event/<id>', methods=["POST","GET"])
def event(id):
    event = show_event(id)
    list_comment = show_comment(id)
    title = "Evento"
    user = "noLog"
    return render_template('cont_event.html', title=title, event=event, list_comment=list_comment, user=user)


@app.route('/create-event')
def create_event():
    formCreate = CreateEvent()
    user = 'log'
    title = "Avents-CreateEvent"
    return render_template('create_event.html', title=title, user=user, formCreate=formCreate)


@app.route('/new-event', methods=["POST", "GET"])
def new_event():
    formCreate = CreateEvent()
    if formCreate.validate_on_submit():
        f = formCreate.image.data
        filename = secure_filename(formCreate.nameEvent.data + " imagen" + str(randint(1, 100)))
        f.save(os.path.join('static/Save', filename))
        flash('Evento creado con exito! (Debera ser aprobado por un administrador antes de '
              'ser mostrado en la pagina)', 'success')
        formCreate.data_show()
        return redirect(url_for('new_event'))
    elif formCreate.is_submitted():
        flash('Error en la carga de datos', 'danger')  # Mostrar mensaje
    return render_template('create_event.html', formCreate=formCreate)


@app.route('/update-event', methods=["POST", "GET"])
def update_event():
    title = "edit_event"

    class Event:
        nameEvent = "Evento 420"
        dateEvent = datetime.datetime.strptime('2021-05-16', "%Y-%m-%d").date()
        place = "En un lugar muy lejano"
        imageEvent = "carrusel3.jpg"
        description = "Esto es un evento random y estamos probando si podemos hacer el formulario de editar evento! " \
                      "estaria muy cool si nos sale xd "

    formCreate = CreateEvent(obj=Event)
    if formCreate.validate_on_submit():
        flash('Evento actualizado con exito! (La actualizacion debera ser aprobada por un administrador antes'
              ' de ser mostrada en la pagina', 'success')
        formCreate.mostrar_datos()
        return redirect(url_for('update_event'))
    return render_template('event_edit.html', title=title, formCreate=formCreate, event=event)


@app.route('/events-admin')
def events_admin():
    user = 'admin'
    title = "Avents-Events-Admin"
    listevent = list_event()
    return render_template('admin_event.html', title=title, id=id, event=event, user=user, listevent=listevent)


@app.route('/edit-admin/<id>')
def edit_admin(id):
    user = 'admin'
    title = "Avents-Edit-Admin"
    listevent = list_event()
    event = list(filter(lambda event: event['id'] == id, listevent))[0]
    return render_template('admin_Edit.html', title=title, id=id, event=event, user=user, listevent=listevent)


app.run(debug=True)