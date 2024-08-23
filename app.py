from flask import Flask
from config import Config
from models import db
from routes import products_bp
from flask_migrate import Migrate
from flasgger import Swagger

app = Flask(__name__)
app.config.from_object(Config)

# initialize database
db.init_app(app)

# initalize migration
migrate = Migrate(app, db)

# Initialize Swagger
swagger = Swagger(app)


with app.app_context():
    db.create_all()

app.register_blueprint(products_bp)


@app.route('/')
def home():
    return "Flask Rest API"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)