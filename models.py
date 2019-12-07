from flask import url_for

from run import db,app,login_manager
from werkzeug.security import generate_password_hash, check_password_hash  #Permite gener y verificar la pass con hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin, LoginManager

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

    # Convertir Objeto a JSON

    def a_json(self):
        event_json = {
        'eventoId': url_for('viewEventPending', eventId=self.eventoId, _external=True),
            'nombre': self.nombre,
            'fecha': str(self.fecha),
            'hora': str(self.hora),
            'lugar': self.lugar,
            'tipo': self.tipo,
            'descripcion': self.descripcion,
            'imagen': self.imagen,
            'aprobado': self.aprobado,
            'usuarioId': self.usuarioId,
        }
        return event_json

    @staticmethod
    # Convertir JSON a objeto
    def desde_json(event_json):
        nombre = event_json.get('nombre')
        fecha = event_json.get('fecha')
        hora = event_json.get('hora')
        lugar = event_json.get('lugar')
        tipo= event_json.get('tipo')
        descripcion= event_json.get('descripcion')
        imagen= event_json.get('imagen')
        aprobado = event_json.get('aprobado')
        usuarioId = event_json.get('usuarioId')
        return Event(
            nombre=nombre,
            fecha=fecha,
            hora=hora,
            lugar_=lugar,
            tipo=tipo,
            descripcion=descripcion,
            imagen=imagen,
            aprobado=aprobado,
            usuarioId=usuarioId,
        )



class User(UserMixin, db.Model):

    usuarioId = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(40), nullable=False)
    apellido = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(60), nullable=False)
    password_hash= db.Column(db.String(128), nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    event = db.relationship("Event", back_populates="user", cascade="all, delete-orphan")
    comment = db.relationship("Comment", back_populates="user", cascade="all, delete-orphan")

    # No permitir leer la pass de un usuario
    @property
    def password(self):
        raise AttributeError('La password no puede leerse')

    # Al setear la pass generar un hash
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def get_id(self):
        return (self.usuarioId)

    # Al verififcar pass comparar hash del valor ingresado con el de la db
    def verificar_pass(self, password):
        return check_password_hash(self.password_hash, password)

    # Generar token de confirmación
    def generar_token_confirmacion(self, expiracion=300):
        # Crear una JSON Web Signatures a partir de la SECRET_KEY
        # Colocar un tiempo de expiración de 3600 segundos
        s = Serializer(app.config['SECRET_KEY'], expiracion)
        # Convertir JWS en un Token string
        return s.dumps({'confirm': self.usuarioId}).decode('utf-8')

    def __repr__(self):
        return '<Usuario %r>' % self.email

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Comment(db.Model):
    comentarioId = db.Column(db.Integer, primary_key=True)
    contenido = db.Column(db.String(350), nullable=False)
    fechahora = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    user = db.relationship("User", back_populates="comment")
    usuarioId = db.Column(db.Integer, db.ForeignKey('user.usuarioId'), nullable=False)
    event = db.relationship("Event", back_populates="comment")
    eventoId = db.Column(db.Integer, db.ForeignKey('event.eventoId'), nullable=False)

    # Convertir Objeto a JSON
    def a_json(self):
        comentario_json = {
            'comentarioId': self.comentarioId,
            'contenido': self.contenido,
            'fechahora': self.fechahora,
            'eventoId':url_for('viewEventPending', eventId=self.eventoId, _external=True),
            'usuarioId': self.usuarioId,
        }
        return comentario_json

    @staticmethod
    # Convertir JSON a objeto
    def desde_json(comentario_json):
        contenido = comentario_json.get('texto_comentario')
        fechahora = comentario_json.get('fechaHora')
        eventoId = comentario_json.get('eventoId')
        usuarioId = comentario_json.get('usuarioId')
        return Comment(
            contenido=contenido,
            fechahora=fechahora,
            eventoId=eventoId,
            usuarioId=usuarioId,
        )

#db.drop_all() #elimina las tablas
db.create_all() #crea las tablas en base a modelos
