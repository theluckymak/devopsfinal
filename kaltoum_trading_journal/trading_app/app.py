from flask import Flask, request, jsonify
import sqlite3
import os
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

# === Logging Setup: console + file ===
app.logger.handlers.clear()

# Console handler (for docker logs)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter('%(asctime)s - %(message)s')
console_handler.setFormatter(console_formatter)
app.logger.addHandler(console_handler)

# File handler (rotating)
log_path = '/app/logs/trades.log'
file_handler = RotatingFileHandler(log_path, maxBytes=1000000, backupCount=3)
file_handler.setLevel(logging.INFO)
file_formatter = logging.Formatter('%(asctime)s - %(message)s')
file_handler.setFormatter(file_formatter)
app.logger.addHandler(file_handler)

app.logger.setLevel(logging.INFO)

# === Database Setup ===
DB_PATH = '/app/trades.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pair TEXT NOT NULL,
            side TEXT NOT NULL,
            result REAL NOT NULL,
            tags TEXT
        )
    ''')
    conn.commit()
    conn.close()

# === Routes ===

@app.route('/')
def index():
    return jsonify({
        'message': 'Welcome to the Trading Journal API',
        'endpoints': {
            'GET /trades': 'List all trades',
            'POST /add_trade': 'Add a new trade (pair, side, result, tags)'
        }
    })

@app.route('/add_trade', methods=['POST'])
def add_trade():
    data = request.json
    pair = data.get('pair')
    side = data.get('side')
    result = data.get('result')
    tags = data.get('tags', '')

    if not pair or side not in ('long', 'short') or result is None:
        return jsonify({'error': 'Invalid input'}), 400

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO trades (pair, side, result, tags) VALUES (?, ?, ?, ?)',
              (pair, side, result, tags))
    conn.commit()
    conn.close()

    log_msg = f"New trade: {pair} {side}, result: {result}, tags: {tags}"
    app.logger.info(log_msg)

    return jsonify({'message': 'Trade added'}), 201

@app.route('/trades', methods=['GET'])
def get_trades():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM trades')
    rows = c.fetchall()
    conn.close()

    trades = [
        {'id': row[0], 'pair': row[1], 'side': row[2], 'result': row[3], 'tags': row[4]}
        for row in rows
    ]
    return jsonify(trades)

# === Run App ===

if __name__ == '__main__':
    if not os.path.exists(DB_PATH):
        init_db()
    app.run(host='0.0.0.0', port=5000)

