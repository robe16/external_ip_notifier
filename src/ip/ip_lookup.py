import urllib, json
import requests


def get_ip():
    url = 'http://ip.jsontest.com'
    r = requests.get(url)
    #
    if r.status_code == requests.codes.ok:
        data = json.loads(urllib.urlopen(url).read())
        ip = data['ip']
        return ip
    else:
        return False
