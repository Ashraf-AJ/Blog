from threading import Thread
from flask import render_template, current_app
from flask_mail import Message
from api import mail


def send_async_email(msg, app):
    with app.app_context():
        mail.send(msg)


def send_email(subject, recipient, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(subject, recipients=[recipient])
    msg.body = render_template(f"{template}.txt", **kwargs)
    msg.html = render_template(f"{template}.html", **kwargs)
    thr = Thread(target=send_async_email, args=(msg, app))
    thr.start()
