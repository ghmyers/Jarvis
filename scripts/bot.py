import os
import sys
# Set working directory
dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
os.chdir(dir_path)

# Add src directory to Python path
sys.path.append(os.path.join(dir_path, "src"))


import json, requests, time
import websocket
from config import APP_TOKEN, API_TOKEN
from src.slack_handlers import SlackHandler
from src.ml_model import JarvisModel
from src.llm_agent import JarvisLLMAgent 
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_bolt import App


# Initialize instances
app = App(token=API_TOKEN)
slack = SlackHandler(token=API_TOKEN)
model = JarvisModel()
agent = JarvisLLMAgent()

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
        try:
            # Try to use openAI LLM
            prediction = agent.classify(text) 
            slack.send_message(channel, f"{prediction}")
        except Exception as e:
            # Fallback to Naive Bayes Classifier
            prediction = model.predict([text])[0]
            slack.handle_response("prediction", message, prediction)

def on_error(ws, error):
    print(f"WebSocket Error: {error}")

def on_close(ws, close_status_code, close_reason):
    print(f"WebSocket Closed: {close_status_code} - {close_reason}")

def on_open(ws):
    print("WebSocket Connection Opened...")

# WebSocket Connection Setup
@app.event("app_mention") 

if __name__ == "__main__":
    SocketModeHandler(app, APP_TOKEN).start()


