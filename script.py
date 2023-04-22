import os
import time
import smtplib
from email.message import EmailMessage
import signal
import atexit
import win32api

gmail_user = 'your-mail-here'
gmail_password = 'secret-key-from-mail-here'
to = 'to-mail-here'

folder_path = os.path.join(os.environ['PROGRAMFILES'], 'Data')

if not os.path.exists(folder_path):
    os.makedirs(folder_path)

def send_email(subject, body, attachments=None):
    msg = EmailMessage()
    msg['From'] = gmail_user
    msg['To'] = to
    msg['Subject'] = subject
    msg.set_content(body)

    if attachments is not None:
        for attachment in attachments:
            with open(attachment, 'rb') as f:
                file_data = f.read()
                file_name = f.name
            msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)


    with smtplib.SMTP_SSL('smtp.mail.ru', 465) as smtp:
        smtp.login(gmail_user, gmail_password)
        smtp.send_message(msg)


def send_email_on_exit():
    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    with open(os.path.join(folder_path, 'computer_data.txt'), 'a') as f:
        f.write(f'End time: {current_time}\n')

    send_email('Program terminated', 'See attached file.', [os.path.join(folder_path, 'computer_data.txt')])


current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

if not os.path.isfile(os.path.join(folder_path, 'computer_data.txt')):
    with open(os.path.join(folder_path, 'computer_data.txt'), 'a') as f:
        f.write(f'Start time: {current_time}\n')

    send_email('Computer powered on', f'The computer was powered on at {current_time}.')

else:
    with open(os.path.join(folder_path, 'computer_data.txt'), 'r') as f:
        last_line = f.readlines()[-1]

    uptime_seconds = int(win32api.GetTickCount() / 1000)

    if uptime_seconds < 60 and 'graceful shutdown' not in last_line.lower():
        with open(os.path.join(folder_path, 'computer_data.txt'), 'a') as f:
            f.write(f'End time: {current_time}\n')

        send_email('Computer restarted', f'The computer was restarted at {current_time}.', [os.path.join(folder_path, 'computer_data.txt')])

    elif 'graceful shutdown' in last_line.lower():
        with open(os.path.join(folder_path, 'computer_data.txt'), 'a') as f:
            f.write(f'Start time: {current_time}\n')

        send_email('Computer powered on', f'The computer was powered on at {current_time}.')

    else:
        with open(os.path.join(folder_path, 'computer_data.txt'), 'a') as f:
            f.write(f'End time: {current_time}\n')

        send_email('Computer shut down', f'The computer was shut down at {current_time}.', [os.path.join(folder_path, 'computer_data.txt')])

atexit.register(send_email_on_exit)

def sig_handler(signum, frame):
    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    with open(os.path.join(folder_path, 'computer_data.txt'), 'a') as f:
        if signum == signal.SIGINT:
            f.write(f'End time: {current_time} (graceful shutdown)\n')
            send_email('Graceful shutdown', f'The computer was gracefully shut down at {current_time}.', [os.path.join(folder_path, 'computer_data.txt')])
        elif signum == signal.SIGTERM:
            f.write(f'End time: {current_time} (forced shutdown)\n')
            send_email('Forced shutdown', f'The computer was forcefully shut down at {current_time}.', [os.path.join(folder_path, 'computer_data.txt')])
        elif signum == signal.SIGABRT:
            f.write(f'End time: {current_time} (abnormal termination)\n')
            send_email('Abnormal termination', f'The script was abnormally terminated at {current_time}.', [os.path.join(folder_path, 'computer_data.txt')])
    exit(0)

signal.signal(signal.SIGINT, sig_handler)
signal.signal(signal.SIGTERM, sig_handler)
signal.signal(signal.SIGABRT, sig_handler)

while True:
    time.sleep(60)
