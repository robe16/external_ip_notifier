import time
from ip.ip_lookup import get_ip
from notify.notify import send_ip
from log.log import log_general, log_warning, log_error


try:
    #
    log_general('Operation started')
    #
    last_ip = False
    #
    while True:
        #
        current_ip = get_ip()
        #
        if current_ip:
            if not last_ip == current_ip:
                e = send_ip(current_ip)
                if e:
                    last_ip = current_ip
                    log_general('Emails sent with new IP address ({ip})'.format(ip=current_ip))
                else:
                    log_warning('Failure to send emails with new IP address ({ip})'.format(ip=current_ip))
        else:
            log_warning('Current IP failed to be retrieved')
        #
        time.sleep(3600)  # 1 hour
        #
except Exception as e:
    log_error('{error}'.format(error=e))
