from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_object(__name__)
    #app.config["SECRET_KEY"] = "your secret key"
    #app.config.from_pyfile(config_filename)

    from . import main_interface
    app.register_blueprint(main_interface.bp)

    from . import db
    db.init_app(app)
    return app