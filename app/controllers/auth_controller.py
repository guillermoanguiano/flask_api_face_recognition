from flask import jsonify, request

from app.services.client_service import ClientService
from app.services.face_recognition_service import FaceRecognitionService


class AuthController:
    @staticmethod
    def create_client_with_face():
        try:
            data = request.get_json()

            if not data:
                return jsonify({"success": False, "message": "No data provided"}), 400

            name = data.get("name")
            email = data.get("email")
            expiration_date = data.get("expiration_date")
            image_data = data.get("image")

            if not all([name, email, expiration_date, image_data]):
                return jsonify(
                    {
                        "success": False,
                        "message": "All fields are required: name, email, expiration_date, and image",
                    }
                ), 400

            existing_client = ClientService.get_client_by_email(email)
            if existing_client:
                return jsonify(
                    {
                        "success": False,
                        "message": "A client with this email already exists",
                    }
                ), 400

            face_encoding, error = FaceRecognitionService.extract_face_encoding(
                image_data
            )

            if error:
                return jsonify(
                    {"success": False, "message": f"Face registration failed: {error}"}
                ), 400

            client, db_error = ClientService.create_client(
                name=name,
                email=email,
                expiration_date=expiration_date,
                face_encoding=face_encoding,
            )

            if db_error:
                return jsonify(
                    {"success": False, "message": f"Database error: {db_error}"}
                ), 500

            return jsonify(
                {
                    "success": True,
                    "message": f"Client {client.name} created successfully with facial recognition",
                    "client": client.to_dict(),
                }
            ), 201

        except Exception as e:
            return jsonify(
                {"success": False, "message": f"Internal server error: {str(e)}"}
            ), 500

    @staticmethod
    def register_face():
        try:
            data = request.get_json()

            if not data:
                return jsonify({"success": False, "message": "No data provided"}), 400

            client_id = data.get("client_id")
            image_data = data.get("image")

            if not client_id or not image_data:
                return jsonify(
                    {"success": False, "message": "client_id and image are required"}
                ), 400

            client = ClientService.get_client_by_id(client_id)
            if not client:
                return jsonify({"success": False, "message": "Client not found"}), 404

            face_encoding, error = FaceRecognitionService.extract_face_encoding(
                image_data
            )

            if error:
                return jsonify({"success": False, "message": error}), 400

            updated_client, db_error = ClientService.update_client_face_encoding(
                client_id, face_encoding
            )

            if db_error:
                return jsonify(
                    {"success": False, "message": f"Database error: {db_error}"}
                ), 500

            return jsonify(
                {
                    "success": True,
                    "message": f"Face registered successfully for {client.name}",
                    "client": updated_client.to_dict(),
                }
            ), 200

        except Exception as e:
            return jsonify(
                {"success": False, "message": f"Internal server error: {str(e)}"}
            ), 500

    @staticmethod
    def verify_access():
        try:
            data = request.get_json()

            if not data:
                return jsonify({"success": False, "message": "No data provided"}), 400

            image_data = data.get("image")

            if not image_data:
                return jsonify({"success": False, "message": "Image is required"}), 400

            clients_with_faces = ClientService.get_all_clients()

            if not clients_with_faces:
                return jsonify(
                    {
                        "success": False,
                        "message": "No clients registered with facial recognition",
                    }
                ), 404

            best_match = None
            best_confidence = 0

            for client in clients_with_faces:
                is_match, confidence, error = FaceRecognitionService.compare_faces(
                    client.face_encoding, image_data
                )

                if error:
                    continue

                if is_match and confidence > best_confidence:
                    best_match = client
                    best_confidence = confidence

            if best_match:
                if best_match.is_membership_active():
                    return jsonify(
                        {
                            "success": True,
                            "access_granted": True,
                            "message": f"Welcome {best_match.name}!",
                            "client": best_match.to_dict(),
                            "confidence": round(best_confidence, 2),
                        }
                    ), 200
                else:
                    return jsonify(
                        {
                            "success": True,
                            "access_granted": False,
                            "message": f"Hello {best_match.name}, your membership has expired. Please contact reception.",
                            "client": best_match.to_dict(),
                            "confidence": round(best_confidence, 2),
                        }
                    ), 200
            else:
                return jsonify(
                    {
                        "success": True,
                        "access_granted": False,
                        "message": "Face not recognized. Access denied.",
                        "client": None,
                    }
                ), 200

        except Exception as e:
            return jsonify(
                {"success": False, "message": f"Internal server error: {str(e)}"}
            ), 500
