from .web_impl import web_impl

frontend_modules = [
    web_impl,
]

def register_frontend(app):
    for i in frontend_modules:
        app.register_blueprint(i)
    return app