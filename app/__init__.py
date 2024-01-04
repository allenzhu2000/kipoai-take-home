from flask import Flask, render_template
from app import search


def create_app():
    app = Flask(__name__)

    app.register_blueprint(search.bp)

    @app.route("/")
    def home():
        return render_template("index.html")
    
    return app
