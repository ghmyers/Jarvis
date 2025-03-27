import requests
from config import API_TOKEN

class SlackHandler:
    def __init__(self):
        self.base_url = "https://slack.com/api/chat.postMessage"

    def send_message(self, channel, text):
        """ Send a Slack message """
        requests.post(self.base_url, data={"token": API_TOKEN, "channel": channel, "text": text})

    def send_gif(self, channel, file_name):
        """ Uploads a GIF to Slack """
        try:
            with open(f"gifs/{file_name}.gif", "rb") as f:
                content = f.read()
            url = "https://slack.com/api/files.upload"
            data = {'token': API_TOKEN, 'channels': channel, 'filetype': 'gif', 'title': file_name, 'content': content}
            requests.post(url=url, data=data)
        except Exception as e:
            print(f"Error sending GIF: {e}")

    def handle_response(self, state, message, prediction=None):
        """ Handles different Slack bot states """
        channel = message["payload"]["event"]["channel"]

        if state == "training":
            self.send_message(channel, "OK, I'm ready for training. What NAME should this ACTION be?")
        elif state == "testing":
            self.send_message(channel, "OK, I've trained on the data you've given me, and I'm ready for testing!")
        elif state == "prediction":
            self.send_message(channel, f"Are you asking about {prediction}?")
