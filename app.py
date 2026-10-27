
from flask import Flask

app = Flask(__name__)

#app
@app.route("/")
@app.route("/hello/")
def hello_world():
    return "Hello World! Deployed automatically with Jenkins and Kubernetes.\n"


@app.route("/hello/<username>")
def hello_user(username):
    return f"Hello {username}!\n"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
