import requests
import datetime
import socket
import ssl


def has_ssl(url):
    try:
        if 'https' in url:
            if '/' in url.split('://')[1]:
                url = 'https://' + url.split('://')[1].split('/')[0]
            response = requests.get(url)
            if response.ok:
                ip = socket.gethostbyname(url.split('//')[1])
                with socket.create_connection((ip, 443)) as sock:
                    context = ssl.create_default_context()
                    with context.wrap_socket(sock, server_hostname=url.split('//')[1]) as ssock:
                        cert = ssock.getpeercert()
                        cert_expiration_date = datetime.datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                        days_left = (cert_expiration_date - datetime.datetime.utcnow()).days

                        subject = dict(x[0] for x in cert['subject'])
                        issued_to = subject['commonName']
                        alt_names = [x[1] for x in cert['subjectAltName'] if x[0].lower() == 'dns']

                        if any(name == url.split('//www.')[1] for name in [issued_to] + alt_names) \
                                or any(name == url.split('//')[1] for name in [issued_to] + alt_names):
                            ssl_valid_for_this_domain = True
                        else:
                            ssl_valid_for_this_domain = False

                        return [True, days_left, ssl_valid_for_this_domain]

            else:
                return [False, 0, False]
        else:
            return [False, 0, False]
    except Exception as e:
        print(f"Error: {e}")
        return [False, 0, False]
