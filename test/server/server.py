# -*- coding: utf-8 -*-
from flask import Flask
from flask import request
import time

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def test_root():
    try:
        message = request.form["message"]
        return report_message(message)
    except Exception as e:
        print("ERROR: ", e)
        return "error"


@app.route("/led", methods=["POST", "GET"])
def test_led():
    try:
        message = str(dict(request.form))
        return report_message(message)
    except Exception as e:
        print("ERROR: ", e)
        return "error: "


@app.route("/test", methods=["POST", "GET"])
def test_connection():
    try:
        message = str(dict(request.form))
        print('test connection request received: ', message)
        return "roger"
    except Exception as e:
        print("ERROR: ", e)
        return "error: "


def report_message(message):
    current_time = time.ctime()
    towrite = current_time + ": " + message
    with open("messages.log", "a") as f:
        f.write(towrite + "\n")
        print("Message received: ", message)
    return "message received " + towrite


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
