from app import create_app, db
import os

app = create_app(os.getenv("FLASK_ENV", "default"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)
