import json
import os
import requests
from flask import Flask, Response, redirect, render_template, url_for, request
from utilities import utilities
from google.cloud import bigquery
from interfaces.api import api_bp
from interfaces.analysis_controller import analysis_bp

from contexts.broker_auth.api_bp import broker_auth_bp
from contexts.holdings.api_bp import holdings_bp


app = Flask(__name__)

@app.route("/")
def index():

    return render_template("home_page.html")
    # return redirect("/broker_auth/vendor_login")

app.register_blueprint(broker_auth_bp)
# app.register_blueprint(api_bp)
app.register_blueprint(analysis_bp)
app.register_blueprint(holdings_bp)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8080")), debug = True)


