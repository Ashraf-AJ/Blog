import os
from api import create_app


app = create_app(os.environ.get("FLASK_CONFIG", "default"))


@app.route("/")
def index():
    return "this should point to react"


import registered_callbacks
