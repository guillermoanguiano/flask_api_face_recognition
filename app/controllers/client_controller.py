from datetime import datetime

from flask import jsonify, request

from app.services.client_service import ClientService


class ClientController:
    @staticmethod
    def get_all_clients():
        """Get all clients"""
        try:
            clients = ClientService.get_all_clients()
            return jsonify(
                {
                    "success": True,
                    "clients": [
                        {**client.to_dict(), "has_face": bool(client.face_encoding)}
                        for client in clients
                    ],
                }
            ), 200
        except Exception as e:
            return jsonify(
                {"success": False, "message": f"Error retrieving clients: {str(e)}"}
            ), 500

    @staticmethod
    def get_client_by_id(client_id):
        """Get specific client by ID"""
        try:
            client = ClientService.get_client_by_id(client_id)
            if not client:
                return jsonify({"success": False, "message": "Client not found"}), 404

            return jsonify({"success": True, "client": client.to_dict()}), 200
        except Exception as e:
            return jsonify(
                {"success": False, "message": f"Error retrieving client: {str(e)}"}
            ), 500

    @staticmethod
    def create_client():
        """Create client without face (legacy endpoint - not recommended)"""
        try:
            data = request.get_json()
            if not data:
                return jsonify({"success": False, "message": "No data provided"}), 400

            name = data.get("name")
            email = data.get("email")
            expiration_date = data.get("expiration_date")

            if not all([name, email, expiration_date]):
                return jsonify(
                    {
                        "success": False,
                        "message": "Name, email, and expiration_date are required",
                    }
                ), 400

            # Validar formato de fecha
            try:
                datetime.strptime(expiration_date, "%Y-%m-%d")
            except ValueError:
                return jsonify(
                    {"success": False, "message": "Invalid date format. Use YYYY-MM-DD"}
                ), 400

            client, error = ClientService.create_client(
                name=name,
                email=email,
                expiration_date=expiration_date,
                face_encoding=None,
            )

            if error:
                return jsonify({"success": False, "message": error}), 400

            return jsonify(
                {
                    "success": True,
                    "message": f"Client {client.name} created successfully. Remember to register facial recognition!",
                    "client": client.to_dict(),
                }
            ), 201

        except Exception as e:
            return jsonify(
                {"success": False, "message": f"Internal server error: {str(e)}"}
            ), 500

    @staticmethod
    def update_client(client_id):
        """Update client information"""
        try:
            data = request.get_json()
            if not data:
                return jsonify({"success": False, "message": "No data provided"}), 400

            existing_client = ClientService.get_client_by_id(client_id)
            if not existing_client:
                return jsonify({"success": False, "message": "Client not found"}), 404

            # Validar email único si se está actualizando
            if "email" in data and data["email"] != existing_client.email:
                email_client = ClientService.get_client_by_email(data["email"])
                if email_client:
                    return jsonify(
                        {"success": False, "message": "Email already exists"}
                    ), 400

            if "expiration_date" in data:
                try:
                    datetime.strptime(data["expiration_date"], "%Y-%m-%d")
                except ValueError:
                    return jsonify(
                        {
                            "success": False,
                            "message": "Invalid date format. Use YYYY-MM-DD",
                        }
                    ), 400

            updated_client, error = ClientService.update_client(client_id, **data)

            if error:
                return jsonify({"success": False, "message": error}), 400

            return jsonify(
                {
                    "success": True,
                    "message": f"Client {updated_client.name} updated successfully",
                    "client": updated_client.to_dict(),
                }
            ), 200

        except Exception as e:
            return jsonify(
                {"success": False, "message": f"Internal server error: {str(e)}"}
            ), 500

    @staticmethod
    def delete_client(client_id):
        """Delete (deactivate) client"""
        try:
            client, error = ClientService.delete_client(client_id)

            if error:
                return jsonify({"success": False, "message": error}), 404

            return jsonify(
                {
                    "success": True,
                    "message": f"Client {client.name} deactivated successfully",
                    "client": client.to_dict(),
                }
            ), 200

        except Exception as e:
            return jsonify(
                {"success": False, "message": f"Internal server error: {str(e)}"}
            ), 500
