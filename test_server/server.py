# -*- coding: utf-8 -*-

from flask import Flask
from flask import request
import time

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def hello_world():
    try:
        message = request.form["message"]
        return do_something(message)
    except Exception as e:
        print(e)
        return "error"


@app.route("/led", methods=["POST", "GET"])
def hello_world2():
    try:
        message = str(dict(request.form))
        return do_something(message)
    except Exception as e:
        print(e)
        return "error: "


def do_something(message):
    current_time = time.ctime()
    towrite = current_time + ": " + message
    with open("messages.log", "a") as f:
        f.write(towrite+"\n")
        print(message)
    return "message received " + towrite


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
