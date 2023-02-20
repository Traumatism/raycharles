import os

from flask.app import Flask
from flask import request


app = Flask("vuln_app")


@app.get("/hello")
def hello():
    name = request.args.get("name", "Titouan")
    os.system(f"echo {name} > /tmp/hello.txt")
    return "Said hello!"


app.run()
