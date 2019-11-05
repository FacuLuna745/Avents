from flask import redirect, url_for, request
from run import app, db
from models import *
from flask import jsonify
from functions import *
from functionsMail import sendMail


# Listar Eventos Pendientes
@app.route('/', methods=["GET"])
@app.route('/api/events/pending/', methods=["GET"])
def pendingEvent():
    events = pending_event_list()
    return jsonify({'events': [event.a_json() for event in events]})


# Ver Evento Pendiente
@app.route('/api/events/pending/<eventId>', methods=["GET"])
def viewEventPending(eventId):
    events = pending_event_view(eventId)
    return jsonify(events.a_json())


# Editar evento pendiente
@app.route('/api/event/pending/<eventId>/edit', methods=["PUT"])
def editPendingEvent(eventId):
    evento = mostrar_evento_pendiente(id)
    evento.nombre_evento = request.json.get('nombre_evento', evento.nombre_evento)
    evento.fecha_evento = request.json.get('fecha_evento', evento.fecha_evento)
    evento.hora_evento = request.json.get('hora_evento', evento.hora_evento)
    evento.lugar_evento = request.json.get('lugar_evento', evento.lugar_evento)
    evento.tipo_evento = request.json.get('tipo_evento', evento.tipo_evento)
    evento.descripcion_evento = request.json.get('descripcion_evento', evento.descripcion_evento)
    db.session.add(evento)
    db.session.commit()
    return jsonify(evento.a_json()), 201


# Eliminar Evento Pendiente
@app.route('/api/eventos-pendientes/evento/<id>/eliminar', methods=["DELETE"])
def borraEventoPendiente(id):
    evento = mostrar_evento_pendiente(id)
    db.session.delete(evento)
    return '', 204


# Aprobar Evento pendiente
@app.route('/api/eventos-pendientes/evento/<id>/aprobar', methods=["PUT"])
def aprobarEventoPendiente(id):
    evento = mostrar_evento_pendiente(id)
    evento.confirmacion_evento = 1
    db.session.add(evento)
    db.session.commit()
    enviarMail(evento.usuario.email_usuario, 'Tu Evento fue aprobado', 'mail/evento_aprobado')
    return jsonify(evento.a_json()), 201


# Listar comentario por evento
@app.route('/api/comentarios/por-evento/<id>', methods=["GET"])
def listarComentarioEvento(id):
    comentarios = mostrar_comentario_evento(id)
    return jsonify({'comentarios': [comentario.a_json() for comentario in comentarios]})


# Ver Comentario
@app.route('/api/comentario/<id>', methods=["GET"])
def mostrarComentario(id):
    comentario = mostrar_un_comentario(id)
    return jsonify(comentario.a_json())


# Borrar Comentario
@app.route('/api/comentario/<id>/borrar', methods=["DELETE"])
def borrarComentario(id):
    comentario = mostrar_un_comentario(id)
    db.session.delete(comentario)
    db.session.commit()
    return '', 204
