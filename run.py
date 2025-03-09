from server import create_app, init_db, socketio
import paho.mqtt.client as mqtt
from server import on_connect, on_message

if __name__ == "__main__":
    # Create the application
    app = create_app('development')
    
    # Initialize the database
    init_db()
    
    # Setup MQTT client
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.connect('157.173.101.159', 1883)
    mqtt_client.loop_start()
    
    # Run the app with SocketIO
    socketio.run(app, debug=True, host='0.0.0.0', port=5000) 