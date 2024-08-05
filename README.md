Installation and Setup
======================
Prerequisites
--------------
    1.Python 3.x installed on your system.
    2.MySQL database server.
    3.Basic understanding of Flask and web development concepts.

***********************************************************************************
    
Installation Steps
=======================
Install dependencies:
---------------------
pip install flask flask-socketio flask-mysqldb

***********************************************************************************

Database setup:
===============
Create a MySQL database and configure database settings in app.py:
------------------------------------------------------------------
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'chat_app'

***********************************************************************************

Run the application:
====================
python app.py

The application will be accessible at http://localhost:5000.

***********************************************************************************

Usage
======
Registration
 1.Navigate to http://localhost:5000/register.
 2.Enter a username and password.
 3.Click on the "Register" button.

 ***********************************************************************************

Login
=====
    1.Navigate to http://localhost:5000/login.
    2.Enter your registered username and password.
    3.Click on the "Login" button.

***********************************************************************************

Chat Interface
==============
    1.After logging in, you will be redirected to the chat interface (http://localhost:5000/chat).
    2.Select a user from the list to start a conversation.
    3.Type your message in the input field and press Enter or click the "Send" button to send a message.
    4.Messages are displayed in real-time, and message history can be retrieved by selecting a user.

***********************************************************************************

Logout
======
    To logout, click on the "Logout" button or navigate to http://localhost:5000/logout.

***********************************************************************************

SocketIO Events
===============
join
-----
Purpose: Allows a user to join a chat room.
Usage: Triggered when a user selects another user to chat with.

message
-------
Purpose: Handles sending messages between users.
Usage: Triggered when a user sends a message; stores messages in the database and emits them to the appropriate chat room.

get_messages
------------
Purpose: Retrieves message history between two users.
Usage: Triggered when a user selects a user; retrieves message history from the database and emits it to the client.

Dependencies
------------
Flask (flask)
Flask-SocketIO (flask_socketio)
Flask-MySQLdb (flask_mysqldb)
Werkzeug (werkzeug)

**********************************[ THANK YOU ]*************************************************
