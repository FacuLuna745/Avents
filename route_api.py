from flask import redirect, url_for, request
from run import app, db, csrf
from models import *
from flask import jsonify
from functions import *
from sqlalchemy.exc import SQLAlchemyError

from functionsMail import sendMail


# Listar Eventos Pendientes
@app.route('/api/events/pending/', methods=["GET"])
def pendingEvent():
    eventsPending = pending_event_list()
    return jsonify({'eventos': [event.a_json() for event in eventsPending]})

# Ver Evento Pendiente
@app.route('/api/event/pending/<eventId>', methods=["GET"])
def viewEventPending(eventId):
    event = pending_event_view(eventId)
    return jsonify(event.a_json())

#Editar evento pendiente
@app.route('/api/event/pending/edit/<eventId>', methods=["PUT"])
@csrf.exempt #Desactivar token para poder editar
def editPendingEvent(eventId):
    event= pending_event_view(eventId)
    event.nombre = request.json.get('nombre', event.nombre)
    event.fecha = request.json.get('fecha', event.fecha)
    event.hora = request.json.get('hora', event.hora)
    event.lugar = request.json.get('lugar', event.lugar)
    event.tipo = request.json.get('tipo', event.tipo)
    event.descripcion = request.json.get('descripcion', event.descripcion)
    event.aprobado = 0
    try:
        db.session.add(event)
        db.session.commit()
        return jsonify(event.a_json()), 201
    except SQLAlchemyError:
        db.rollback()

#Eliminar Evento Pendiente
@app.route('/api/event/pending/delete/<eventId>', methods=["DELETE"])
@csrf.exempt
def deletePendingEvent(eventId):
    event = pending_event_view(eventId)
    try:
        db.session.delete(event)
        db.session.commit()
        return '', 204
    except SQLAlchemyError:
        db.rollback()

#Aprobar evento
@app.route('/api/event/approve/<eventId>', methods=["PUT"])
@csrf.exempt
def approveEvent(eventId):
    event = pending_event_view(eventId)
    event.aprobado = True
    db.session.add(event)
    db.session.commit()
    sendMail(event.user.email, 'Evento Aprobado!', 'mail/event', event=event)
    return jsonify(event.a_json()), 201



#Listar comentario por evento
@app.route('/api/event/comments/<eventId>', methods=["GET"])
def listCommentEvent(eventId):
    comments = show_comment(eventId)
    return jsonify({'comentarios': [comment.a_json()for comment in comments]})


#Mostrar comentario en particular
@app.route('/api/comment/<commentId>', methods=["GET"])
def showCommentEvent(commentId):
    comments = view_comment(commentId)
    return jsonify({'comentario':comments.a_json()})


#Eliminar Comentario
@app.route('/api/comment/delete/<commentId>', methods=["DELETE"])
@csrf.exempt
def deleteComment(commentId):
    comment = get_comment(commentId)
    db.session.delete(comment)
    db.session.commit()
    return '', 204
