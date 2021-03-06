import os

from flask import Flask
from config import DevelopmentConfig

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(DevelopmentConfig())
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from empoyee_controller import employee_controller as employee_controller_blueprint
    app.register_blueprint(employee_controller_blueprint)

    return app
