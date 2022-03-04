import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

username = 'flaskdjangopython@gmail.com'
***REMOVED*** = 'Ciap3k123#'


def send_mail(html=None, text='Email_body', subject='Pizza online', from_email='', to_emails=[]):
    assert isinstance(to_emails, list)
    msg = MIMEMultipart('alternative')
    msg['From'] = from_email
    msg['To'] = ", ".join(to_emails)
    msg['Subject'] = subject
    txt_part = MIMEText(text, 'plain')
    msg.attach(txt_part)

    html_part = MIMEText(f"<p>Here is your ***REMOVED*** reset token</p><h1>{html}</h1>", 'html')
    msg.attach(html_part)
    msg_str = msg.as_string()

    server = smtplib.SMTP(host='smtp.gmail.com', port=465)
    server.ehlo()
    server.starttls()
    server.login(username, ***REMOVED***)
    server.sendmail(from_email, to_emails, msg_str)
    server.quit()
