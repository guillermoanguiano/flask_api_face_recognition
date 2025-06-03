from datetime import date

from app import db
from app.models.client import Client


class ClientService:
    @staticmethod
    def get_active_clients():
        """Get all active clients"""
        return Client.query.filter(
            Client.active is True, Client.expiration_date >= date.today()
        ).all()

    @staticmethod
    def get_client_by_id(client_id):
        """Get client by ID"""
        return Client.query.get(client_id)

    @staticmethod
    def get_client_by_email(email):
        """Get client by email"""
        return Client.query.filter_by(email=email).first()

    @staticmethod
    def create_client(name, email, expiration_date, face_encoding=None):
        """Create a new client"""
        try:
            # Verificar que el email no esté ya registrado
            existing_client = ClientService.get_client_by_email(email)
            if existing_client:
                return None, "A client with this email already exists"

            client = Client(
                name=name,
                email=email,
                expiration_date=expiration_date,
                face_encoding=face_encoding,
            )
            db.session.add(client)
            db.session.commit()
            return client, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def update_client_face_encoding(client_id, face_encoding):
        """updating client's face encoding"""
        try:
            client = Client.query.get(client_id)
            if not client:
                return None, "Client not found"

            client.face_encoding = face_encoding
            db.session.commit()
            return client, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def get_all_clients():
        """Get all clients"""
        return Client.query.all()

    @staticmethod
    def update_client(client_id, **kwargs):
        """Update client with provided fields"""
        try:
            client = Client.query.get(client_id)
            if not client:
                return None, "Client not found"

            for key, value in kwargs.items():
                if hasattr(client, key):
                    setattr(client, key, value)

            from datetime import datetime

            client.updated_at = datetime.utcnow()
            db.session.commit()
            return client, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def delete_client(client_id):
        """Delete a client (soft delete by setting active=False)"""
        try:
            client = Client.query.get(client_id)
            if not client:
                return None, "Client not found"

            client.active = False
            db.session.commit()
            return client, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)
