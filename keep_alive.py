from flask import Flask, jsonify
from threading import Thread
import datetime

app = Flask('')

@app.route('/')
def home():
    return "Bot está rodando!"

@app.route('/health')
def health():
    return jsonify({
        "status": "online",
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "bot": "Valoris Discord Bot"
    })

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
