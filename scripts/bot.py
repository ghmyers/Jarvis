import os
import sys
# Set working directory
dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
os.chdir(dir_path)

# Add src directory to Python path
sys.path.append(os.path.join(dir_path, "src"))


import json, requests, time
import websocket
from config import APP_TOKEN
from slack_handlers import SlackHandler
from ml_model import JarvisModel


# Initialize instances
slack = SlackHandler()
model = JarvisModel()

# WebSocket Event Handlers
def on_message(ws, message):
    message = json.loads(message)
    
    print("Received Message:", json.dumps(message, indent=2))

    if "bot_id" not in message["payload"]["event"]:
        text = message["payload"]["event"]["text"].lower()
        channel = message["payload"]["event"]["channel"]
        
        if text == "training time":
            slack.handle_response("training", message)
        elif text == "testing time":
            slack.handle_response("testing", message)
            X_train, y_train = model.import_db()
            model.train(X_train, y_train)
        elif text == "gif time":
            slack.send_gif(channel, "hug")
        else:
            prediction = model.predict([text])[0]
            slack.handle_response("prediction", message, prediction)

def on_error(ws, error):
    print(f"WebSocket Error: {error}")

def on_close(ws, close_status_code, close_reason):
    print(f"WebSocket Closed: {close_status_code} - {close_reason}")

def on_open(ws):
    print("WebSocket Connection Opened...")

# WebSocket Connection Setup
if __name__ == "__main__":
    websocket.enableTrace(False)
    req = requests.post("https://slack.com/api/apps.connections.open", headers={"Authorization": f"Bearer {APP_TOKEN}"})
    ws_url = req.json().get("url")
    
    ws = websocket.WebSocketApp(ws_url, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
