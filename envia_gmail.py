import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

password = os.getenv('EMAIL_PASSWORD') 

def enviarGmail(subject, to, body, attachment=None):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = 'easyridergames@gmail.com'
    msg['To'] = to

    corpo_mensagem = body
    msg.attach(MIMEText(corpo_mensagem, 'plain'))

    if attachment is not None:
        filename = f'{attachment}.xlsx'
        anexo = open(filename, 'rb')

        part = MIMEBase('application', 'octet-stream')
        part.set_payload((anexo).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename= {filename}')
        anexo.close()

        msg.attach(part)

    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.ehlo()
    s.starttls()
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string())
    print('Email enviado com sucesso!')
    s.quit()