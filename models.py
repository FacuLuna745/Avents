from run import db

class Event(db.Model):

    eventoId = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(60), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    descripcion = db.Column(db.String(500), nullable=False)
    imagen = db.Column(db.String(70), nullable=False)
    lugar = db.Column(db.String(60), nullable=False)
    user = db.relationship("User", back_populates="event")
    comment = db.relationship("Comment", back_populates="event", cascade="all, delete-orphan")
    usuarioId = db.Column(db.Integer, db.ForeignKey('user.usuarioId'), nullable=False)
    aprobado = db.Column(db.Boolean, nullable=False, default=False)
    hora = db.Column(db.Time, nullable=False)
    tipo = db.Column(db.String(15), nullable=False)


class User(db.Model):

    usuarioId = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(40), nullable=False)
    apellido = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(60), nullable=False)
    password= db.Column(db.String(128), nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    event = db.relationship("Event", back_populates="user", cascade="all, delete-orphan")
    comment = db.relationship("Comment", back_populates="user", cascade="all, delete-orphan")

class Comment(db.Model):

    comentarioId = db.Column(db.Integer, primary_key=True)
    contenido = db.Column(db.String(350), nullable=False)
    fechahora = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    user = db.relationship("User", back_populates="comment")
    usuarioId = db.Column(db.Integer, db.ForeignKey('user.usuarioId'), nullable=False)
    event = db.relationship("Event", back_populates="comment")
    eventoId = db.Column(db.Integer, db.ForeignKey('event.eventoId'), nullable=False)


#db.drop_all() #elimina las tablas
#db.create_all() #crea las tablas en base a modelos
