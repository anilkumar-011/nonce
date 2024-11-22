from flask import Flask, jsonify, render_template
import os
import base64
import secrets

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.after_request
def after_request(response):
    response.headers["access-control-allow-methods"] = "DELETE, GET, POST, PUT"
    response.headers["access-control-allow-origin"] = "*"
    response.headers["access-control-allow-headers"] = "content-type"
    nonce = base64.b64encode(secrets.token_bytes(16)).decode("utf-8")
    css_nonce = base64.b64encode(secrets.token_bytes(16)).decode("utf-8")
    response.headers["Content-Security-Policy"] = ""
    if nonce:
        response.headers["Content-Security-Policy"] += f" script-src 'nonce-{nonce}'"
    if css_nonce:
        response.headers["Content-Security-Policy"] += f" style-src 'nonce-{css_nonce}'"
    return response


@app.route("/data")
def data():
    data = {
        "name": "flask",
        "nonce": "yes nonce",
    }
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
