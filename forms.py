# - *- coding: utf- 8 - *-
from datetime import date

from flask_wtf import FlaskForm  # Importa funciones de formulario
from wtforms import StringField, TextField, HiddenField, PasswordField, TextAreaField, SelectField, RadioField, \
    SubmitField  # Importa campos
from wtforms.fields.html5 import EmailField, DateField  # Importa campos HTML
from wtforms import validators  # Importa validaciones
from wtforms_components import TimeField
from flask_wtf.file import FileField, FileRequired, FileAllowed  # Importa funciones, validaciones y campos de archivo


# Clase de Registro
class Register(FlaskForm):

    # Función de validación de nombre de usuario
    def name_user(form, field):
        # Verificar que no contenga guiones bajors o numeral
        if (field.data.find("_") != -1) or (field.data.find("#") != -1):
            # Mostrar error de validación
            raise validators.ValidationError("El nombre de usuario solo puede contener letras, números y .")



    # Definición de campo String
    nombre = StringField('Nombre',
                         [
                             # Definición de validaciones
                             validators.Required(message="Completar nombre")
                         ])

    apellido = StringField('Apellido',
                           [
                               validators.Required(message="Completar apellido")
                           ])

    # Definición de campo de contraseña
    password = PasswordField('Contraseña', [
        validators.DataRequired(),
        # El campo de contraseña debe coincidir con el de confirmuar
        validators.EqualTo('confirm', message='La contraseña no coincide')
    ])

    confirm = PasswordField('Repetir contraseña')

    # Definición de campo de correo
    email = EmailField('Correo',
                       [
                           validators.Required(message="Completar email"),
                           validators.Email(message='Formato de mail incorrecto')
                       ])
    # Definición de campo submit
    submitRegister = SubmitField("Crear")

    # Clase de Login


class Login(FlaskForm):
    # Definición de campo de contraseña
    passwordLogin = PasswordField('Password', [
        validators.Required(),
    ])

    # Definición de campo de mail
    emailLogin = EmailField('E-mail',
                            [
                                validators.Required(message="Completar email"),
                                validators.Email(message='Formato de mail incorrecto')
                            ])
    # Definición de campo submit
    submitLogin = SubmitField("Iniciar")





class CreateEvent(FlaskForm):
    def event_name(self, field):
        if (field.data.find("_") != -1) or (field.data.find("*") != -1):
            raise validators.ValidationError("Solo los siguientes caracteres especiales estan admitidos (! - # @ . ,)")
        if (field.data.find("fuck") != -1) or (field.data.find("nigga") != -1):
            raise validators.ValidationError("El nombre del evento no puede contener malas palabras.")

    def opcional(field):
        field.validators.insert(0, validators.Optional())


    def date_range(self, field):  # Esta funcion no deja ingresar una fecha en el pasado
        if field.data < date.today():
            raise validators.ValidationError("Por favor, ingrese una fecha valida")

    nameEvent = StringField('Nombre del evento',
                            {
                                validators.Required(message="Completar nombre"),
                                validators.length(min=5, max=70,
                                                  message='El nombre del evento debe tener entre 5 y 70 caracteres'),
                                event_name
                            })

    dateEvent = DateField('Fecha del Evento',
                          [
                              validators.DataRequired(message="Ingrese la fecha de su evento"),
                              date_range
                          ])
    timeEvent = TimeField('Hora',
                     [
                         validators.DataRequired(message="Ingrese una hora válida")
                     ])

    place = StringField('Ubicacion',
                        [
                            validators.Required(message="Completar Ubicacion")
                        ])

    image = FileField(validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], 'El archivo debe ser una imagen jpg o png')
    ])

    description = TextAreaField('Introduzca una descripcion del evento',
                                [
                                    validators.DataRequired(message="Por favor ingrese una descripcion"),
                                    validators.length(min=40,
                                                      message='La descripcion del evento no puede ser tan corta.')
                                ])

    type_event = [
        ('1', '--Seleccione el tipo de evento--'),
        ('Obra', 'Obra'),
        ('Festival', 'Festival'),
        ('Curso', 'Curso'),
        ('Conferencia', 'Conferencia'),
        ('Fiesta', 'Fiesta'),
    ]
    options = SelectField('Opción', choices=type_event)

    submitEvent = SubmitField("Crear evento!")
    update = SubmitField("Actualizar")

class Filter(FlaskForm):
        def event_name(self, field):
            if (field.data.find("_") != -1) or (field.data.find("*") != -1):
                raise validators.ValidationError(
                    "Solo los siguientes caracteres especiales estan admitidos (! - # @ . ,)")
            if (field.data.find("fuck") != -1) or (field.data.find("nigga") != -1):
                raise validators.ValidationError("El nombre del evento no puede contener malas palabras.")


        nameEvent = StringField('Nombre del evento',
                                {
                                    validators.optional(),
                                })

        dateEventSince= DateField('Desde',
                              [
                                  validators.optional(),
                              ])
        dateEventUntil = DateField('Hasta',
                              [
                                  validators.optional(),
                              ])

        place = StringField('Ubicacion',
                            [
                                validators.optional()
                            ])
        typeEvent = [
            ('1', 'Tipo de Evento'),
            ('Obra', 'Obra'),
            ('Festival', 'Festival'),
            ('Curso', 'Curso'),
            ('Conferencia', 'Conferencia'),
            ('Fiesta', 'Fiesta'),
        ]
        options = SelectField('Opción', choices=typeEvent)

        search=SubmitField("Buscar")
class Comment (FlaskForm):
    commentEvent=TextAreaField('Escriba un comentario',
                               {
                                   validators.DataRequired(message="No puede comentar en blanco"),
                                   validators.length(min=4, max=350,
                                                     message='El nombre del evento debe tener entre 4 y 350 caracteres')
                               })
    submit = SubmitField("Comentar")