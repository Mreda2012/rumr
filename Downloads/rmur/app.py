from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Store colors for each session
user_colors = {}

def generate_color():
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEEAD', 
              '#D4A5A5', '#9B59B6', '#3498DB', '#E74C3C', '#1ABC9C']
    return random.choice(colors)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    # Assign random color to new user
    user_colors[request.sid] = generate_color()

@socketio.on('message')
def handle_message(message):
    emit('message', {
        'text': message,
        'color': user_colors[request.sid]
    }, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=3000)