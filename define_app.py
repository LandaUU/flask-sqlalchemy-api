import os

from flask import Flask


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pymssql://USERNAME:PASSWORD@db-hostname/db-name"
    app.config['SECRET_KEY'] = 'My Secret Key'
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from empoyee_controller import employee_controller as employee_controller_blueprint
    app.register_blueprint(employee_controller_blueprint)

    return app
