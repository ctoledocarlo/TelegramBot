from flask import Flask
from threading import Thread

app = Flask("")
app = Flask(__name__)

@app.route('/')

def home():
    return "Hello. I am alive!"

def run():
  app.run("0.0.0.0", port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()