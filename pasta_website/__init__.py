from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(__name__)
    #app.config["SECRET_KEY"] = "your secret key"
    #app.config.from_pyfile(config_filename)
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        DATABASE   = os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    from . import main_interface
    app.register_blueprint(main_interface.bp)

    from . import db
    db.init_app(app)
    return app