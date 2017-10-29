import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import email_config as config
from log.log import log_error


def send_ip(ip):
    try:
        msg = compile_email(ip)
        return send_email(msg)
    except Exception as e:
        log_error(e)
        return False


def compile_email(ip):
    #
    service = config.get_config_general_name()
    #
    msg = MIMEMultipart()
    msg["To"] = '; '.join(config.get_config_notifications_emailto())
    msg["From"] = config.get_config_email_username()
    msg["Subject"] = '{service}: New external IP address'.format(service=service)
    #
    text = 'A new external IP address has been detected for "{service}":'.format(service=service)
    text += '<br>'
    text += '<h2>{ip}</h2>'.format(ip=ip)
    text += '<br>'
    #
    msgText = MIMEText(text, 'html')
    #
    msg.attach(msgText)
    #
    return msg


def send_email(msg):
    eml = smtplib.SMTP(config.get_config_email_server(),
                       config.get_config_email_port())
    eml.starttls()
    eml.set_debuglevel(0)
    eml.login(config.get_config_email_username(),
              config.get_config_email_password())
    eml.sendmail(config.get_config_email_username(),
                 config.get_config_notifications_emailto(),
                 msg.as_string())
    eml.quit()
    return True