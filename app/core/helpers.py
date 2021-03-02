from flask_mail import Message
from app.extensions import mail


def send_welcome_email(name: str, email: str):
    msg_body = f"<h1>{name} Welcome to the Flask-skeleton family</h1>"
    msg = Message(subject="Welcome", recipients=[email], html=msg_body)
    msg.sender = "noreply@flask-skeleton.com"
    mail.send(msg)
