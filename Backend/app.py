import os
from api import create_app

app = create_app(os.environ.get("FLASK_CONFIG") or "default")


@app.route("/hello")
def hello():
    return {"msg": "Hello From Flask"}
