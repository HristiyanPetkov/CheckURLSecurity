from flask import Flask, render_template, request
from access_type import has_ssl
from ports import get_open_ports

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        url = request.form['url']

        ssl_response = has_ssl(url)
        is_secure = ssl_response[0]
        days_left = ssl_response[1]
        ssl_valid_for_this_domain = ssl_response[2]

        open_ports = get_open_ports(url)

        return render_template('result.html', is_secure=is_secure, days_left=days_left,
                               ssl_valid_for_this_domain=ssl_valid_for_this_domain, url=url, ports=open_ports)
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)