# -*-coding: utf-8 *-*
import datetime
import os.path
from random import randint
from sqlalchemy.sql.functions import user
from run import app, db, mail
from flask import request
from flask import Flask
from flask import flash  # importar para mostrar mensajes flash
from flask import redirect, url_for  # importar para permitir redireccionar y generar url
from flask import render_template
from flask_wtf import CSRFProtect
from werkzeug.utils import secure_filename
from forms import *  # importar clase de formulario
from functions import *
from models import *
from flask_login import login_required, login_user, logout_user, current_user, LoginManager
from sqlalchemy import or_
from functionsMail import sendMail

csrf = CSRFProtect(app)  # Iniciar protección CSRF


# Función que sobreescribe el método al intentar ingresar a una ruta no autorizada
@login_manager.unauthorized_handler
def unauthorized_callback():
    flash('Debe iniciar sesión para continuar.', 'warning')
    # Redireccionar a la página que contiene el formulario de login
    return redirect(url_for('index'))


@app.route('/', methods=["POST", "GET"])
def index():
    title = "Avents"
    formFilter = Filter()
    listevent = list_event()  # consultar eventos en bd
    events = db.session.query(Event).filter(
        Event.fecha >= db.session.query(Event).filter(Event.aprobado == True)).order_by(Event.fecha)  # consulta
    if formFilter.validate_on_submit():
        listevent = db.session.query(Event)
        if formFilter.nameEvent.data is not None:
            listevent = listevent.filter(Event.nombre.ilike("%" + formFilter.nameEvent.data + "%"))
        if formFilter.place.data is not None:
            listevent = listevent.filter(Event.lugar.ilike("%" + formFilter.place.data + "%"))
        if formFilter.dateEventSince.data is not None:
            listevent = listevent.filter(Event.fecha >= formFilter.dateEventSince.data)
        if formFilter.dateEventUntil.data is not None:
            listevent = listevent.filter(Event.fecha <= formFilter.dateEventUntil.data)
        if formFilter.options.data != '1':
            listevent = listevent.filter(Event.tipo == formFilter.options.data)

        events = listevent.filter(Event.aprobado == True).order_by(Event.fecha)

    return render_template('cont_index.html', listevent=listevent, title=title, formFilter=formFilter,
                           events=events)


@app.route('/register', methods=["POST", "GET"])
def register():
    user = 'nolog'
    title = "Avents-Register"
    formRegister = Register()  # Instanciar formRegister de registro
    if formRegister.validate_on_submit():  # Si el formRegister ha sido enviado y es validado correctamente}
        auxQuerry = db.session.query(User).filter(User.email == formRegister.email.data)
        if auxQuerry.count() == 0:
            flash('Usuario registrado exitosamente', 'success')  # Mostrar mensaje
            users = User(nombre=formRegister.nombre.data,
                         apellido=formRegister.apellido.data,
                         email=formRegister.email.data,
                         password=formRegister.password.data,
                         admin=0)
            insert_db(users)
            sendMail(formRegister.email.data, 'Bienvenido a Avents', 'mail/mensaje')
            login_user(users, True)
            return redirect(url_for('index'))  # Redirecciona a la página principal
        else:
            flash('Existe una cuenta registrada con el email ingresado', 'danger')
    elif formRegister.is_submitted():
        flash('Error en la carga de datos', 'danger')  # Mostrar mensaje
    return render_template('register.html', formRegister=formRegister, user=user, title=title)


@app.route('/login', methods=["GET", "POST"])
def login():
    title = "Avents-Login"
    formLogin = Login()  # Instanciar formulario de Login
    if formLogin.validate_on_submit():  # Si el formulario ha sido enviado y es validado correctamente
        user = db.session.query(User).filter(User.email == formLogin.emailLogin.data).first()

        if user is not None and user.verificar_pass(formLogin.passwordLogin.data):
            login_user(user, True)
            return redirect(url_for("index", userId=user.usuarioId))
        else:
            flash('Email o pass incorrectas.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html', formLogin=formLogin)


@app.route('/event/<eventId>', methods=["POST", "GET"])
def event(eventId):
    title = "Evento"
    particular_event = show_event(eventId)
    formComment = CreateComment()
    list_comment = show_comment(eventId)
    return render_template('cont_event.html', title=title, particular_event=particular_event, formComment=formComment,list_comment=list_comment)

# ----------------------------------USER------------------------------------------------------------------------

@app.route('/my-event')
@login_required
def my_event():
    title = "Avents-MyEvent"
    listevent = list_event_user(current_user.usuarioId)
    return render_template('cont_myevent.html', title=title, listevent=listevent)


@app.route('/new-event', methods=["POST", "GET"])
@login_required
def new_event():
    formCreate = CreateEvent()
    user = "Log"
    title = "Avents-CreateEvent"
    log = show_user(311)
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
                      usuarioId=311)
        insert_db(event)
        return redirect(url_for('my_event'))
    elif formCreate.is_submitted():
        flash('Error en la carga de datos', 'danger')  # Mostrar mensaje
    return render_template('create_event.html', formCreate=formCreate, title=title, user=user, event=Event, log=log)


@app.route('/update-event/<eventId>', methods=["POST", "GET"])
@login_required
def update_event(eventId):
    title = "edit_event"
    user = "Log"
    eventUpdate = show_event(eventId)
    log = show_user(311)

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
@login_required
def delete_event(eventId):
    event = show_event(eventId)
    delete_element_db(event)
    return redirect(url_for('my_event'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/create-comment/<eventId>', methods=["POST", "GET"])
@login_required
def comment_user(eventId):
    default = db.func.current_timestamp()
    formComment = CreateComment()
    eventUser = show_event(eventId)
    if formComment.validate_on_submit():
        flash("Comentario cargado con exito","success")
        comment = Comment(
            contenido=formComment.commentEvent.data,
            fechahora=default,
            eventoId=eventUser.eventoId,
             usuarioId=current_user.usuarioId)
        insert_db(comment)
    return redirect(url_for('event', userId=current_user.usuarioId, eventId=eventUser.eventoId, formComment=formComment))


# -----------------------------------------------ADMIN------------------------------------------------------------------

@app.route('/list-events-admin')
def events_admin():
    user = "admin"
    title = "Avents-MyEvent"
    listevent = list_event()
    return render_template('cont_myevent.html', title=title, listevent=listevent, user=user)


@app.route('/view-admin/<eventId>', methods=["POST", "GET"])
def view_admin(eventId):
    user = "admin"
    particular_event = show_event(eventId)
    list_comment = show_comment(eventId)
    title = "Evento-Admin"
    return render_template('cont_event.html', title=title, particular_event=particular_event, list_comment=list_comment,
                           user=user)


@app.route('/event-approve/<eventId>', methods=["POST", "GET"])
def event_approve(eventId):
    user = "admin"
    event = db.session.query(Event).get(eventId)
    event.aprobado = True
    update_db()
    sendMail(event.user.email, 'Evento aprobado!', 'mail/event', event=event)

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


@app.route('/delete-comment-admin/<eventId>', methods=["POST", "GET"])
def delete_comment_admin(eventId):
    # Obtener comentario por id
    comment = db.session.query(Comment).get(eventId)
    idEvent = comment.eventoId
    # Eliminar de la db
    db.session.delete(comment)
    db.session.commit()
    flash('EL comentario ha sido borrado con Éxito', 'success')
    return redirect(url_for('view_admin', eventId=idEvent))


app.run(debug=True)
