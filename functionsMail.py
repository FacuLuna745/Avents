import datetime
import smtplib

from wtforms_components.fields import time

from run import mail,app,Message
from flask import render_template
from threading import Thread

#Función que configura el mensaje
def confMsg(to, subject, template, **kwargs):
    #Configurar asunto, emisor y destinatarios
    msg = Message( subject, sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    #Seleccionar template para mensaje de texto plano
    msg.body = render_template(template + '.txt', **kwargs)
    #Seleccionar template para mensaje HTML
    msg.html = render_template(template + '.html', **kwargs)
    return msg

#Función para mandar un mail de manera asincrónica
def enviarMailAsync(app, msg,subject,to):
    #Se utiliza el contexto de la aplicación para tener acceso a la configuración
    with app.app_context():
        try:
            mail.send(msg)
        except smtplib.SMTPAuthenticationError as e:
            print("Error de autenticacion: " + str(e))
            with open('error_mail_log', 'a') as file:
                file.writelines(str(datetime.datetime.now()) + " Error de autenticacion: " + str(e))
                file.writelines('Recorda enviar mail de ' + str(subject) + ' a: ' + str(to))
        except smtplib.SMTPServerDisconnected as e:
            print("Servidor desconectado: " + str(e))
            with open('error_mail_log', 'a') as file:
                file.writelines(str(datetime.datetime.now()) + " Servidor desconectado: " + str(e) + '\n')
                file.writelines('Recorda enviar mail de ' + str(subject) + ' a: ' + str(to))
        except smtplib.SMTPSenderRefused as e:
            print("Se requiere autenticacion: " + str(e))
            with open('error_mail_log', 'a') as file:
                file.writelines(str(datetime.datetime.now()) + " Se requiere autenticacion: " + str(e) + '\n')
                file.writelines('Recorda enviar mail de ' + str(subject) + ' a: ' + str(to))
        except smtplib.SMTPException as e:
            print("Unexpected error: " + str(e))
            with open('error_mail_log', 'a') as file:
                file.writelines(str(datetime.datetime.now()) + " Unexpected error: " + str(e) + '\n')
                file.writelines('Recorda enviar mail de ' + str(subject) + ' a: ' + str(to))


#Función que genera el hilo que enviará el mail
def sendMail(to, subject, template, **kwargs):
    #Crear configuración
    msg = confMsg(to, subject, template, **kwargs)
    #Crear hilo
    thr = Thread(target=enviarMailAsync, args=[app, msg,subject,to])
    #Iniciar hilo
    thr.start()

