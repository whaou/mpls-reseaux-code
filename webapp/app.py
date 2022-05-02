#!/usr/bin/python3

# Tutorial from: https://projects.raspberrypi.org/en/projects/python-web-server-with-flask/

from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    # return "Hello world"
    # return render_template("client_ws.html")
    return render_template("index.html")


@app.route("/carte/<board_number>")
def board(board_number):
    print("Accessing board number" + str(board_number))
    return render_template("board.html", board_number=board_number)


@app.route("/about")
def about():
    return "It's me!"


@app.route("/test")
def test():
    return render_template("test.html")


# @app.route("/hello/<name>")
# def hello(name):
#     print("Accessing " + name)
#     return render_template("page-name.html", name=name)


# @app.route("/packets")
# def packets():
#     tst = {"one": "AAABBBCCC", "two": "xyz"}
#     return render_template("packets.html", packets=tst)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
