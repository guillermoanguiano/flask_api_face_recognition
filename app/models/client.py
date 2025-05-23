from app import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import BYTEA


class Client(db.Model):
    __tablename__ = "clients"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)
    expiration_date = db.Column(db.Date, nullable=False)
    face_encoding = db.Column(BYTEA, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __repr__(self):
        return f"<Client {self.name}>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "active": self.active,
            "expiration_date": self.expiration_date.isoformat()
            if self.expiration_date
            else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def is_membership_active(self):
        from datetime import date

        return self.active and self.expiration_date >= date.today()
