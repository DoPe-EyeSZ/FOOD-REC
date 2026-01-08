from .submission import submission


def register_blueprint(app):
    app.register_blueprint(submission)
