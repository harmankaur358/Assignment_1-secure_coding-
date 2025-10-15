import os, smtplib
import pymysql
from urllib.request import urlopen
from email.message import EmailMessage


db_config = {
    'host': os.environ.get('DB_HOST', 'mydatabase.com'),
    'user': os.environ.get('DB_USER', 'admin'),
    'password': os.environ.get('DB_PASSWORD') 
}

def get_user_input():
    user_input = input('Enter your name: ')
    return user_input


def send_email(to, subject, body):
    msg = EmailMessage()
    msg["From"] = os.environ["SMTP_USER"]
    msg["To"] = to
    msg["Subject"] = subject.replace("\n","")
    msg.set_content(body)
    
    with smtplib.SMTP_SSL(os.environ["SMTP_HOST"], int(os.environ.get("SMTP_PORT",465))) as smtp:
        smtp.login(os.environ["SMTP_USER"], os.environ["SMTP_PASS"])
        smtp.send_message(msg)

def get_data():
    url = 'https://insecure-api.com/get-data'
    data = urlopen(url).read().decode()
    return data

def save_to_db(data):
    data = str(data).strip()
    
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO mytable (col1, col2) VALUES (%s, %s)"
            cursor.execute(sql, (data, "Another Value"))  
        connection.commit()
    finally:
        connection.close()

if __name__ == '__main__':
    user_input = get_user_input()
    data = get_data()
    save_to_db(data)
    send_email('admin@example.com', 'User Input', user_input)
