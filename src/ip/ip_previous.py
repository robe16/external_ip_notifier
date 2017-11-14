import os

def get_last_ip():
    file = open(os.path.join(os.path.dirname(__file__), 'last_ip.txt'), 'r')
    ip = file.read()
    file.close()
    #
    return ip


def set_last_ip(ip):
    file = open(os.path.join(os.path.dirname(__file__), 'last_ip.txt'), 'w')
    file.write(ip)
    file.close()
