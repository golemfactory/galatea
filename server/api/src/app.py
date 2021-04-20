from flask import Flask, request
from flask_cors import CORS

import classifier
import os

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)

    @app.route('/api')
    def index():
        return {
            "version": "0.0.1",
            "git.commit": os.getenv("COMMIT", "0000000"),
            "git.branch": os.getenv("BRANCH", ""),
    }

    @app.route('/api/classify', methods=["POST"])
    def classify():
        text = request.form.get("text_file") or request.form.get("text")
        print(text)

        return classifier.classify_text(text)


    return app
