import os
from flask import Flask
from meshtastic import tcp_interface

app = Flask(__name__)
meshtastic_node_host = os.getenv('MESHTASTIC_HOST', 'meshtastic.local')
meshtastic_default_sender = os.getenv('MESHTASTIC_DEFAULT_SENDER')
interface = tcp_interface.TCPInterface(hostname=meshtastic_node_host)
messages = []

@app.route("/")
def hello_world():
    return "<p>Hello, World!!!</p>"

@app.route("/send/<message>", methods=['POST'])
def send_message(message):
    try:
        interface.sendText(message, destinationId=meshtastic_default_sender)
    except Exception as e:
        print(f"Error sending message: {e}")
        return {"status": "error", "message": str(e)}
    
    return {"status": "success", "message": message}