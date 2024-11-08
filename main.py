from flask import Flask, jsonify, render_template,g
import os
import base64
import secrets

app = Flask(__name__)

@app.route("/")
def home():
    nonce = base64.b64encode(secrets.token_bytes(16)).decode('utf-8')
    g.nonce=nonce
    css_nonce = base64.b64encode(secrets.token_bytes(16)).decode('utf-8')
    g.css_nonce=css_nonce
    return render_template("index.html", nonce=nonce, css_nonce=css_nonce)


@app.after_request
def after_request(response):
    response.headers["access-control-allow-methods"] = "DELETE, GET, POST, PUT"
    response.headers["access-control-allow-origin"] = "*"
    response.headers["access-control-allow-headers"] = "content-type"
    nonce = getattr(g, 'nonce', None)
    if nonce:
        response.headers["Content-Security-Policy"] = f"script-src 'nonce-{nonce}'"
    css_nonce = getattr(g, 'css_nonce', None)
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
