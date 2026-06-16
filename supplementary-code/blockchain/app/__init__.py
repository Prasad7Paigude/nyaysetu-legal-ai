"""Flask application factory for blockchain peer node and file sharing UI."""

from flask import Flask

app = Flask(__name__)

from blockchain.app import views
