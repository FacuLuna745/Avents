# -*-coding: utf-8 *-*
import datetime
import os.path
from random import randint

from sqlalchemy.sql.functions import user

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



# Función que muestra los datos obtenidos del envío de formulario
def show_data(formRegister):
    print(formRegister.nombre.data)
    print(formRegister.apellido.data)
    print(formRegister.password.data)


# -----------------------INICIO------------------------------------------------------------------------
@app.route('/', methods=["POST", "GET"])
def index():
    title = "Avents"
    user = 'noLog'
    formFilter = Filter()
    listevent = list_event()  # consultar eventos en bd
    events = db.session.query(Event).filter(
        Event.fecha >= db.session.query(Event).filter(Event.aprobado == True)).order_by(Event.fecha)  # consulta
    if formFilter.validate_on_submit():
        listevent = db.session.query(Event)
        if formFilter.nameEvent.data is not None:
            listevent = listevent.filter(Event.nombre.ilike("%"+formFilter.nameEvent.data +"%"))
        if formFilter.place.data is not None:
            listevent = listevent.filter(Event.lugar.ilike("%" + formFilter.place.data + "%"))
        if formFilter.dateEventSince.data is not None:
            listevent = listevent.filter(Event.fecha >= formFilter.dateEventSince.data)
        if formFilter.dateEventUntil.data is not None:
            listevent = listevent.filter(Event.fecha <= formFilter.dateEventUntil.data)
        if formFilter.options.data != '1':
            listevent = listevent.filter(Event.tipo == formFilter.options.data)

        events = listevent.filter(Event.aprobado == True).order_by(Event.fecha)

    return render_template('cont_index.html', listevent=listevent, user=user, title=title, formFilter=formFilter,
                           events=events)


@app.route('/my-event')
def my_event():
    user = "Log"
    log = show_user(297)
    title = "Avents-MyEvent"
    listevent = list_event_user(297)
    return render_template('cont_myevent.html', title=title, listevent=listevent, user=user, log=log)


# ------------------------------------USUARIO-----------------------------------------------
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
            return redirect(url_for('login'))  # Redirecciona a la página principal
    else:
        flash('Formato del email incorrecto', 'danger')
        return redirect(url_for('index'))  # Redirecciona a la página principal
    return render_template('cont_index.html', formLogin=formLogin)


# ------------------------------------------EVENTOS---------------------------------------------------
@app.route('/event/<id>', methods=["POST", "GET"])
def event(id):
    user = "noLog"
    particular_event = show_event(id)
    list_comment = show_comment(id)
    title = "Evento"
    return render_template('cont_event.html', title=title, particular_event=particular_event, list_comment=list_comment,
                           user=user)


@app.route('/new-event', methods=["POST", "GET"])
def new_event():
    formCreate = CreateEvent()
    user = "Log"
    title = "Avents-CreateEvent"
    log = show_user(297)
    if formCreate.validate_on_submit():
        f = formCreate.image.data
        filename = secure_filename(formCreate.nameEvent.data + " imagen" + str(randint(1, 100)))
        f.save(os.path.join('static/Save', filename))
        flash('Evento creado con exito! (Debera ser aprobado por un administrador antes de '
              'ser mostrado en la pagina)', 'success')

        event = Event(nombre=formCreate.nameEvent.data,
                      fecha=formCreate.dateEvent.data,
                      lugar=formCreate.place.data,
                      descripcion=formCreate.description.data,
                      tipo=formCreate.options.data,
                      hora=formCreate.timeEvent.data,
                      imagen=formCreate.image.data.filename,
                      usuarioId=297)
        insert_db(event)
        return redirect(url_for('my_event'))
    elif formCreate.is_submitted():
        flash('Error en la carga de datos', 'danger')  # Mostrar mensaje
    return render_template('create_event.html', formCreate=formCreate, title=title, user=user, event=Event, log=log)


@app.route('/update-event/<eventId>', methods=["POST", "GET"])
def update_event(eventId):
    title = "edit_event"
    user = "Log"
    eventUpdate = show_event(eventId)
    log = show_user(297)

    class Event:
        nameEvent = eventUpdate.nombre
        dateEvent = eventUpdate.fecha
        timeEvent = eventUpdate.hora
        place = eventUpdate.lugar
        image = eventUpdate.imagen
        description = eventUpdate.descripcion
        options = eventUpdate.tipo

    formCreate = CreateEvent(obj=Event)
    CreateEvent.opcional(formCreate.image)
    if formCreate.validate_on_submit():
        flash('Evento actualizado con exito! (La actualizacion debera ser aprobada por un administrador antes'
              ' de ser mostrada en la pagina', 'success')

        eventUpdate.nombre = formCreate.nameEvent.data,
        eventUpdate.fecha = formCreate.dateEvent.data,
        eventUpdate.hora = formCreate.timeEvent.data,
        eventUpdate.lugar = formCreate.place.data,
        eventUpdate.tipo = formCreate.options.data,
        eventUpdate.descripcion = formCreate.description.data,
        eventUpdate.aprobado = 0
        update_db()

        return redirect(url_for('my_event'))
    elif formCreate.is_submitted():
        flash('Error en la carga de datos', 'danger')  # Mostrar mensaje
    return render_template('event_edit.html', title=title, formCreate=formCreate, eventUpdate=eventUpdate, user=user,
                           log=log)


@app.route('/delete-event/<eventId>', methods=["POST", "GET"])
def delete_event(eventId):
    user = "Log"
    event = show_event(eventId)
    delete_element_db(event)
    return redirect(url_for('my_event'))


@app.route('/create-comment/<eventId>', methods=["POST", "GET"])
def create_comment(eventId):
    default = db.func.current_timestamp()
    formComment = Comment()
    user = show_user(297)
    event = show_event(eventId)
    if formComment.validate_on_submit():
        flash('Comentario publicado', 'success')  # Mostrar mensaje
        comment = Comment(
            contenido=formComment.commentEvent.data,
            fechaHora=default,
            eventoId=event.eventoId,
            usuarioId=user.usuarioId
        )
        insert_db(comment)
        return redirect(url_for('event'))  # Redirecciona a la página principal}
    else:
        flash('', 'danger')
        return redirect(url_for('event'))  # Redirecciona a la página principal
    return render_template('cont_event.html', title=title, particular_event=particular_event, list_comment=list_comment,
                           user=user, event=event)


# -----------------------------------------------ADMIN------------------------------------------------------------------
@app.route('/events-admin')
def events_admin():
    user = "admin"
    title = "Avents-MyEvent"
    listevent = list_event()
    return render_template('cont_myevent.html', title=title, listevent=listevent, user=user)


@app.route('/event-approve/<eventId>', methods=["POST", "GET"])
def event_approve(eventId):
    user = "admin"
    event = db.session.query(Event).get(eventId)
    event.aprobado = True
    update_db()
    return redirect(url_for('events_admin', event=event, user=user))


@app.route('/event-disapprove/<eventId>', methods=["POST", "GET"])
def event_disapprove(eventId):
    user = "admin"
    event = db.session.query(Event).get(eventId)
    event.aprobado = False
    update_db()
    return redirect(url_for('events_admin', event=event, user=user))


@app.route('/delete-event-admin/<eventId>', methods=["POST", "GET"])
def delete_event_admin(eventId):
    user = "admin"
    event = show_event(eventId)
    delete_element_db(event)
    return redirect(url_for('events_admin'))


app.run(debug=True)
