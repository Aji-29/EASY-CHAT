import random
import string
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_socketio import SocketIO, send, emit, join_room
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'EasyChat'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'chat_app'
socketio = SocketIO(app)
mysql = MySQL(app)

def generate_token():
    return ''.join(random.choices(string.digits, k=10))

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('chat'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('chat'))
    
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        token = generate_token()
        
        # Check if username already exists
        cur = mysql.connection.cursor()
        cur.execute("SELECT id FROM users WHERE name = %s", [name])
        existing_user = cur.fetchone()
        
        if existing_user:
            cur.close()
            flash("Username already exists.")
            return render_template('register.html')
        
        # Insert new user if username is available
        cur.execute("INSERT INTO users (name, password, token) VALUES (%s, %s, %s)", (name, password, token))
        mysql.connection.commit()

        # Get the user's ID after insertion
        cur.execute("SELECT id FROM users WHERE name = %s", [name])
        new_user = cur.fetchone()
        cur.close()

        # Set the session for the new user
        session['user_id'] = new_user[0]
        session['username'] = name 
        return redirect(url_for('chat'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('chat'))
    
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, name, password FROM users WHERE name = %s and password = %s", [name, password])
        user = cur.fetchone()
        cur.close()
        
        if user:
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect(url_for('chat'))
        else:
            flash("Invalid credentials. Please try again.")
    
    return render_template('login.html')

@app.route('/chat')
def chat():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, name, token FROM users WHERE id != %s", [session['user_id']])
    users = cur.fetchall()
    cur.close()
    
    return render_template('chat.html', users=users, username=session['username'])

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('index'))

@socketio.on('join')
def on_join(data):
    username = session['username']
    room = data['room']
    join_room(room)

@socketio.on('message')
def handle_message(data):
    sender_id = session['user_id']
    receiver_id = data['receiver_id']
    message = data['message']
    room = data['room']
    
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO messages (sender_id, receiver_id, message) VALUES (%s, %s, %s)", (sender_id, receiver_id, message))
    mysql.connection.commit()
    cur.close()
    # Send message to both sender and receiver
    emit('message', {'sender_id': sender_id, 'message': message}, room=room)

@socketio.on('get_messages')
def get_messages(data):
    sender_id = session['user_id']
    receiver_id = data['receiver_id']
    room = data['room']
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT sender_id, message, timestamp FROM messages WHERE (sender_id = %s AND receiver_id = %s) OR (sender_id = %s AND receiver_id = %s) ORDER BY timestamp", 
                (sender_id, receiver_id, receiver_id, sender_id))
    messages = cur.fetchall()
    cur.close()
    
    message_history = [{'sender_id': msg[0], 'message': msg[1], 'timestamp': msg[2].strftime('%Y-%m-%d %H:%M:%S'), 'who':sender_id} for msg in messages]
    
    emit('message_history', {'history': message_history}, to=room)
    # Emit the history to the client

if __name__ == '__main__':
    socketio.run(app, debug=True)
    #socketio.run(app, host=' 192.168.12.104', port=5000, debug=True)
