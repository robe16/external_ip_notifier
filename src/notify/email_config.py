import json
import os


def get_cfg_json():
    with open(os.path.join(os.path.dirname(__file__), 'config_email.json'), 'r') as data_file:
        data = json.load(data_file)
    return data['config']

################################################################################################
# Email
################################################################################################

def get_config_email():
    data = get_cfg_json()
    return data['email']


def get_config_email_server():
    data = get_config_email()
    return data['SERVER']


def get_config_email_port():
    data = get_config_email()
    return data['PORT']


def get_config_email_username():
    data = get_config_email()
    return data['USERNAME']


def get_config_email_password():
    data = get_config_email()
    return data['PASSWORD']


################################################################################################
# Notifications
################################################################################################

def get_config_notifications():
    data = get_cfg_json()
    return data['notifications']


def get_config_notifications_emailto():
    data = get_config_notifications()
    return data['EML_TO']


################################################################################################
# General
################################################################################################

def get_config_general():
    data = get_cfg_json()
    return data['general']


def get_config_general_name():
    data = get_config_general()
    return data['name']