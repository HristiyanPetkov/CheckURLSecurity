import socket
import threading
import queue


def scan_port(port, results, ip):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)
    result = sock.connect_ex((ip, port))
    if result == 0:
        results.put(port)
    sock.close()


def get_open_ports(url):
    if 'www.' in url:
        domain = url.split('www.')[1]
    else:
        domain = url.split('://')[1]

    if '/' in domain:
        domain = domain.split('/')[0]

    ip = socket.gethostbyname(domain)
    results = queue.Queue()
    threads = []
    for port in range(1, 65535):
        thread = threading.Thread(target=scan_port, args=[port, results, ip])
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    open_ports = []
    while not results.empty():
        open_ports.append(results.get())

    return open_ports
