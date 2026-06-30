import json
import os
import requests
from flask import Flask, Response, redirect, render_template, url_for, request
from utilities import utilities
from google.cloud import bigquery
from interfaces.api import api_bp
from interfaces.analysis_controller import analysis_bp

app = Flask(__name__)

app.register_blueprint(api_bp)
app.register_blueprint(analysis_bp)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8080")), debug = True)


