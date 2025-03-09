from flask import Flask, render_template, jsonify, Response
from flask_socketio import SocketIO
import paho.mqtt.client as mqtt
import sqlite3
from datetime import datetime
import json
import pandas as pd
from flask_login import LoginManager, UserMixin, login_required, current_user

# Define extensions at module level
login_manager = LoginManager()
socketio = SocketIO()

def create_app(config_name):
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'
    
    # Set configuration based on config_name
    if config_name == 'testing':
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    # Initialize extensions with the app
    socketio.init_app(app, cors_allowed_origins="*")
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    
    # Register route functions with app
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/get_historical_data')
    def get_historical_data():
        conn = sqlite3.connect('weather_data.db')
        c = conn.cursor()
        c.execute('''SELECT timestamp, AVG(temperature) as temp, AVG(humidity) as hum 
                    FROM weather_readings 
                    GROUP BY strftime('%Y-%m-%d %H:%M', timestamp)
                    ORDER BY timestamp DESC LIMIT 288''')
        data = c.fetchall()
        conn.close()
        
        return jsonify(data)
    
    @app.route('/export_data')
    def export_data():
        conn = sqlite3.connect('weather_data.db')
        df = pd.read_sql_query("SELECT * FROM weather_readings", conn)
        conn.close()
        
        # Export to CSV
        return Response(
            df.to_csv(index=False),
            mimetype="text/csv",
            headers={"Content-disposition": "attachment; filename=weather_data.csv"}
        )
    
    @app.route('/admin')
    @login_required
    def admin_panel():
        return render_template('admin.html')
    
    return app

# Simple User class
class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# Database initialization
def init_db():
    conn = sqlite3.connect('weather_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS weather_readings
                 (timestamp DATETIME, temperature FLOAT, humidity FLOAT)''')
    conn.commit()
    conn.close()

# MQTT callbacks
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker")
    client.subscribe("/work_group_01/room_temp/#")

def on_message(client, userdata, msg):
    topic = msg.topic
    value = float(msg.payload.decode())
    
    if topic.endswith('temperature'):
        store_reading('temperature', value)
    elif topic.endswith('humidity'):
        store_reading('humidity', value)
    
    socketio.emit('new_reading', {'topic': topic, 'value': value})

def store_reading(sensor_type, value):
    conn = sqlite3.connect('weather_data.db')
    c = conn.cursor()
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    if sensor_type == 'temperature':
        c.execute('INSERT INTO weather_readings (timestamp, temperature) VALUES (?, ?)',
                 (now, value))
    else:
        c.execute('INSERT INTO weather_readings (timestamp, humidity) VALUES (?, ?)',
                 (now, value))
    
    conn.commit()
    conn.close()

def check_alerts(temperature, humidity):
    alerts = []
    if temperature > 30:
        alerts.append("High temperature alert!")
    if humidity > 80:
        alerts.append("High humidity alert!")
    return alerts

# Only used when running directly
if __name__ == '__main__':
    app = create_app('development')
    init_db()
    
    # Setup MQTT client
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.connect('157.173.101.159', 1883)
    mqtt_client.loop_start()
    
    socketio.run(app, debug=True, host='0.0.0.0', port=5000) 