import os

from functionsMail import sendMail
from models import *
from run import db, SQLAlchemyError


def pending_event_list():
    return db.session.query(Event).filter(Event.aprobado == 0)

def pending_event_view(id):
    events = pending_event_list()
    return events.filter(Event.eventoId == id).first_or_404()

def get_comment(id):
    return db.session.query(Comment).get(id)

def view_comment(id):
    return db.session.query(Comment).filter(Comment.comentarioId == id)

def list_event():
    return db.session.query(Event).all()

def insert_db(objeto):
    try:
        db.session.add(objeto)
        db.session.commit()
    except SQLAlchemyError as e:
        db.rollback()
        sendMail(os.getenv('ADMIN_MAIL'), 'Error en SQLAlchemy', 'mail/error', e=e)

def update_db():
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.rollback()
        sendMail(os.getenv('ADMIN_MAIL'), 'Error en SQLAlchemy', 'mail/error', e=e)

def delete_element_db(objeto):
    try:
        db.session.delete(objeto)
        db.session.commit()
    except SQLAlchemyError as e:
        db.rollback()
        sendMail(os.getenv('ADMIN_MAIL'), 'Error en SQLAlchemy', 'mail/error', e=e)

def show_event(id):
    return db.session.query(Event).get(id)

def show_user(id):
    return db.session.query(User).get(id)

def show_comment(id):
    return db.session.query(Comment).filter(Comment.eventoId == id).all()

def list_event_user(usuarioID):
    return db.session.query(Event).filter(Event.usuarioId == usuarioID).all()