from flask import render_template, request, jsonify
import functionsMail as mail
from run import app, os
import datetime


# Manejar error de página no encontrada
@app.errorhandler(404)
def page_not_found(e):
    viewFile_log(e)
    # Si la solicitud acepta json y no HTML
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        # Responder con JSON
        response = jsonify({'error': 'not found'})
        response.status_code = 404
        return response
    # Sino responder con template HTML
    return render_template('error/404.html'), 404


# Manejar error de error interno
@app.errorhandler(500)
def internal_server_error(e):
    print(e)
    viewFile_log(e)
    mail.sendMail(os.getenv('ADMIN_MAIL'), 'Error en SQLAlchemy', 'mail/error', e=e)
    # Si la solicitud acepta json y no HTML
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        # Responder con JSON
        response = jsonify({'error': 'internal server error'})
        response.status_code = 500
        return response
    # Sino responder con template HTML
    return render_template('error/500.html'), 500


@app.errorhandler(Exception)  # Manejo de errores generales
def generalException(e):
    print(e)
    viewFile_log(e)
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        # Responder con JSON
        response = jsonify({'error': 'Unexpected error ' + str(e)})
        return response
    # Sino responder con template HTML
    return render_template('error/500.html'), 500


def viewFile_log(e):
    with open("errors_log", 'a') as file:
        file.write("\n\n" + str(datetime.datetime.now().strftime("%d %b %Y - %H:%M")) + '-' + str(e))


def viewFile_logMail(e, message, subject, to):
    with open("error_logMail", 'a') as file:
        file.write("\n\n" + str(datetime.datetime.now().strftime("%d %b %Y - %H:%M")) + '-' + message + str(e))
        file.write("\nRecordar que se debe enviar un mail a" + str(to) + "desde" + str(subject))
