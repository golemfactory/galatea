from flask import Flask
from flask_cors import CORS

def create_app():
    """
    Create a Flask application using the app factory pattern.

    :return: Flask app
    """
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)

    @app.route('/api')
    def index():
        """
        Backend API response

        :return: Flask response
        """
        return {
            "version": "0.0.1",
        }


    return app
