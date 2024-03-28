from os import environ
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr, BaseModel
from typing import List

class EmailSchema(BaseModel):
    email: List[EmailStr]

conf = ConnectionConfig(
    MAIL_USERNAME   = environ['MAIL_USERNAME'],
    MAIL_PASSWORD   = environ['MAIL_PASSWORD'],
    MAIL_FROM       = environ['MAIL_FROM'],
    MAIL_PORT       = 587,
    MAIL_SERVER     = environ['MAIL_SERVER'],
    MAIL_FROM_NAME  = environ['MAIL_FROM_NAME'],
    MAIL_STARTTLS   = True,
    MAIL_SSL_TLS    = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS  = True
)
