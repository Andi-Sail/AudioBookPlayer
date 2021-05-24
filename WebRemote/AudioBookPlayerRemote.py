import threading
from flask import Flask
from flask import render_template

import socket
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

bookPlayer = None

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/pause_play")
def PausePlay():
    print("Pause Play")
    if bookPlayer is not None:
        bookPlayer.PausePlay()

    return render_template("index.html")

def _run():
    app.run(host=hostname, port=8080, debug=True)

def run():
    app.run(host=hostname, port=8080, debug=False, threaded=True)

def start(player):
    global bookPlayer
    bookPlayer = player
    remoteThread = threading.Thread(target=run)
    remoteThread.daemon = True
    remoteThread.start()

if __name__ == "__main__":
    _run()