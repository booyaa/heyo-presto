import os
from time import sleep
from flask import Flask
from meshtastic import tcp_interface
from pubsub import pub

app = Flask(__name__)
meshtastic_node_host = os.getenv('MESHTASTIC_HOST', 'meshtastic.local')
meshtastic_default_sender = os.getenv('MESHTASTIC_DEFAULT_SENDER')
interface = tcp_interface.TCPInterface(hostname=meshtastic_node_host)
messages = []

@app.route("/debug/status", methods=['GET'])
def status():
    try:
        print(interface.getMyNodeInfo())
        return {"status": "success", "message": f"interface: ok / {len(messages)} messages"}
    except Exception as e:
        print(f"Error getting status: {e}")
        return {"status": "error", "message": str(e)}

@app.route("/debug/sideload", methods=['POST'])
def sideload_messages():
    messages.extend(["test message", "hello there", "this message is truncated"])
    print(f"DEBUG|sideloaded messages: {messages}")
    return {"status": "success", "message": "messages side loaded"}

@app.route("/send/<message>", methods=['POST'])
def send_message(message):
    try:
        interface.sendText(message, destinationId=meshtastic_default_sender)
    except Exception as e:
        print(f"Error sending message: {e}")
        return {"status": "error", "message": str(e)}
    
    return {"status": "success", "message": message}

@app.route("/get/message", methods=['GET'])
def get_message():
    print(f"DEBUG|get msg before: {messages}")
    if messages:
        return {"status": "success", "message": messages.pop(0)}
    else:
        return {"status": "error", "message": "No messages available"}
    
def on_receive(packet, interface):
    try:
        if packet.get('decoded', {}).get('portnum') == 'TEXT_MESSAGE_APP':
            print(f"DEBUG|before on_recv: {messages}")
            raw_text = packet['decoded']['text']
            if raw_text.lower().startswith('presto'):
                print(f"DEBUG|{packet['decoded']['text']}")
                messages.append(truncate_message(clean_up_message(raw_text)))
            else:
                print(f"DEBUG|Ignored: {raw_text}")
            print(f"DEBUG|after on_recv: {messages}")
    except Exception as e:
        print(f"Error processing packet: {e}")

def on_connection(interface, topic=pub.AUTO_TOPIC): # called when we (re)connect to the radio
    print(f"Connected to node")

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
    print("Starting presto bridge...")
    app.run(host='0.0.0.0', port=5050) #, threaded=True)