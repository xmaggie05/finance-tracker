from flask import Flask
from config import Config
from models import db

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.route("/")
def home():
    return {
        "message": "Welcome to Smart Finance Tracker API!",
        "status": "Backend is running"
    }

@app.route("/health")
def health():
    return {
        "status": "healthy"
    }

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)