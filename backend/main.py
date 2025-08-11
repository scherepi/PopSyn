from flask import Flask
from dotenv import load_dotenv
import threading

app = Flask(secret_key)