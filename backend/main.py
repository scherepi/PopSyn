from flask import Flask, session
from gotrue import SyncSupportedStorage
from dotenv import load_dotenv
import threading

class AnalysisThread(threading.Thread):
    def __init__(self, title, artist, onFailure=None, onFinished=None):
        super().__init__()
        self.title = title
        self.artist = artist
        self.onFailure = onFailure
        self.onFinished = onFinished

    def run(self):
        
app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True)