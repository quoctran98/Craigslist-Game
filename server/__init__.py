from flask import Flask

from server.helper import settings, listings

def create_app():

    # Set up Flask app
    app = Flask(__name__)
    app.config["SECRET_KEY"] = settings.FLASK_SECRET_KEY
    
    # Blueprint for non-auth routes from routes/main.py
    from .routes.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Blueprint for api routes from routes/api.py
    from .routes.api import api as api_blueprint
    app.register_blueprint(api_blueprint)

    # Make sure the app is running with the correct settings
    print(f"The server has started in a {settings.ENVIRONMENT} environment 💻")

    return(app)
