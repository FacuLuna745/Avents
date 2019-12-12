import datetime
import smtplib
from error import *
from run import mail, app, Message
from flask import render_template
from threading import Thread


# Función que configura el mensaje
def confMsg(to, subject, template, **kwargs):
    # Configurar asunto, emisor y destinatarios
    msg = Message(subject, sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    # Seleccionar template para mensaje de texto plano
    msg.body = render_template(template + '.txt', **kwargs)
    # Seleccionar template para mensaje HTML
    msg.html = render_template(template + '.html', **kwargs)
    return msg


# Función para mandar un mail de manera asincrónica
def enviarMailAsync(app, msg, subject, to):
    # Se utiliza el contexto de la aplicación para tener acceso a la configuración
    with app.app_context():
        try:
            mail.send(msg)
        except smtplib.SMTPAuthenticationError as e:
            print("Error de autenticación: " + str(e))
            viewFile_logMail(e, "Error de autenticación ", subject, to)

        except smtplib.SMTPServerDisconnected as e:
            print("Servidor desconectado: " + str(e))
            viewFile_logMail(e, "Servidor desconectado ", subject, to)

        except smtplib.SMTPSenderRefused as e:
            print("Se requiere autenticacion: " + str(e))
            viewFile_logMail(e, "Se requiere autenticacion ", subject, to)

        except smtplib.SMTPException as e:
            print("Unexpected error: " + str(e))
            viewFile_logMail(e, "Unexpected error ", subject, to)


# Función que genera el hilo que enviará el mail
def sendMail(to, subject, template, **kwargs):
    # Crear configuración
    msg = confMsg(to, subject, template, **kwargs)
    # Crear hilo
    thr = Thread(target=enviarMailAsync, args=[app, msg, subject, to])
    # Iniciar hilo
    thr.start()
