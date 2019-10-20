from models import *
from run import db

def list_event():
    return db.session.query(Event).all()

def insert_db(objeto):
    db.session.add(objeto)
    db.session.commit()

def update_db():
    db.session.commit()

def delete_element_db(objeto):
    db.session.delete(objeto)
    db.session.commit()

def show_event(id):
    return db.session.query(Event).get(id)

def show_user(id):
    return db.session.query(User).get(id)

def show_comment(id):
    return db.session.query(Comment).filter(Comment.eventoId == id).all()

def list_event_user(usuarioID):
    return db.session.query(Event).filter(Event.usuarioId == usuarioID).all()