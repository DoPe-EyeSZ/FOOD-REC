from .input import input


def register_blueprint(app):
    app.register_blueprint(input)
