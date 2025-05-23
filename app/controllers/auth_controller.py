from flask import request, jsonify
from app.services.face_recognition_service import FaceRecognitionService
from app.services.client_service import ClientService


class AuthController:
    @staticmethod
    def register_face():
        """
        Register client's face
        Expected: {
            "client_id": int,
            "image": "data:image/jpeg;base64,..."
        }
        """
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
        """
        Verify access through facial recognition
        Expected: {
            "image": "data:image/jpeg;base64,..."
        }
        """
        try:
            data = request.get_json()

            if not data:
                return jsonify({"success": False, "message": "No data provided"}), 400

            image_data = data.get("image")

            if not image_data:
                return jsonify({"success": False, "message": "Image is required"}), 400

            clients_with_faces = ClientService.get_clients_with_face_encoding()

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
