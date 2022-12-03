from flask import Flask, render_template
import socket

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('8.8.8.8', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP
print(get_ip())


app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello world'

@app.route('/newpage')
def cakes():
    return 'Hey look a new page cool'

@app.route('/image')
def web():
    return render_template('web.html')

@app.route('/movie')
def webmov():
    return render_template('webmov.html')

if __name__ == '__main__':
    app.run(debug=True, host=get_ip())