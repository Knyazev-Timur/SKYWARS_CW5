from flask import Flask
from views import main_blueprint

def create_app() -> Flask:
    app = Flask(__name__)
    app.config['JSON_AS_ASCII'] = False
    app.register_blueprint(main_blueprint)
    return app


app = create_app()
if __name__ == "__main__":
    app.run(port=8080)
