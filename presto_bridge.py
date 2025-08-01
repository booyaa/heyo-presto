import os
from time import sleep
from flask import Flask, request
from meshtastic import tcp_interface
from pubsub import pub
import logging
logger = logging.getLogger(__name__)

app = Flask(__name__)
meshtastic_node_host = os.getenv('MESHTASTIC_HOST', 'meshtastic.local')
meshtastic_default_sender = os.getenv('MESHTASTIC_DEFAULT_SENDER')
interface = tcp_interface.TCPInterface(hostname=meshtastic_node_host)
my_node_info = interface.getMyNodeInfo()
messages = []

@app.route("/debug/status", methods=['GET'])
def status():
    try:
        app.logger.debug(f"{request.path} messages: {messages}")
        return {"status": "success", "message": f"interface: {my_node_info['user']['longName']} / battery: {my_node_info['deviceMetrics']['batteryLevel']}% / {len(messages)} messages"}
    except Exception as e:
        app.logger.error(f"{request.path} error getting status: {e}")
        return {"status": "error", "message": str(e)}

@app.route("/debug/sideload", methods=['POST'])
def sideload_messages():
    messages.extend(["test message", "hello there", "this message is truncated"])
    app.logger.debug(f"{request.path} sideloaded messages: {messages}")
    return {"status": "success", "message": "messages side loaded"}

@app.route("/send/<message>", methods=['POST'])
def send_message(message):
    try:
        interface.sendText(message, destinationId=meshtastic_default_sender)
    except Exception as e:
        app.logger.error(f"{request.path} error sending message: {e}")
        return {"status": "error", "message": str(e)}
    
    return {"status": "success", "message": message}

@app.route("/get/message", methods=['GET'])
def get_message():
    app.logger.debug(f"{request.path} before: {messages}")
    if messages:
        return {"status": "success", "message": messages.pop(0)}
    else:
        return {"status": "error", "message": "No messages available"}
    
def on_receive(packet, interface):
    try:
        if packet.get('decoded', {}).get('portnum') == 'TEXT_MESSAGE_APP':
            app.logger.debug(f"on_recv before: {messages}")
            raw_text = packet['decoded']['text']
            if raw_text.lower().startswith('presto'):
                app.logger.debug(f"on_recv raw message: {packet['decoded']['text']}")
                messages.append(truncate_message(clean_up_message(raw_text)))
            else:
                app.logger.debug(f"on_recv ignored: {raw_text}")
            app.logger.debug(f"on_recv after: {messages}")
    except Exception as e:
        app.logger.error(f"on_recv error processing packet: {e}")

def on_connection(interface, topic=pub.AUTO_TOPIC): # called when we (re)connect to the radio
    app.logger.info(f"Connected to {my_node_info['user']['longName']}")

def clean_up_message(message):
    if message.lower().startswith('presto'):
        message = message[6:].strip()
        if message.startswith(':'):
            message = message[1:].strip()
    return message

def truncate_message(message):
    if len(message) > 22:
        return message[:22] + "..."
    return message

pub.subscribe(on_receive, "meshtastic.receive")
pub.subscribe(on_connection, "meshtastic.connection.established")

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.logger.info("Starting presto bridge...")
    app.run(host='0.0.0.0', port=5050) #, threaded=True)