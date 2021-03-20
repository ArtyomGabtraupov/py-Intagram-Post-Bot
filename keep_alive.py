from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def main():
    return "Sup! I am Alive!"

def run():
    app.run(host="0.0.0.0", port=4037)

def keep_alive():
    server = Thread(target=run)
    server.start()
