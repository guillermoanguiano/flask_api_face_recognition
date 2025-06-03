import base64
import io

import face_recognition
import numpy as np
from PIL import Image


class FaceRecognitionService:
    @staticmethod
    def extract_face_encoding(image_data):
        try:
            if isinstance(image_data, str):
                if "," in image_data:
                    image_data = base64.b64decode(image_data.split(",")[1])
                else:
                    image_data = base64.b64decode(image_data)

            image = Image.open(io.BytesIO(image_data))

            if image.mode != "RGB":
                image = image.convert("RGB")

            image_np = np.array(image)

            face_locations = face_recognition.face_locations(image_np, model="hog")

            if not face_locations:
                return None, "No face detected in image"

            if len(face_locations) > 1:
                return None, "Multiple faces detected. Use image with single person"

            face_encodings = face_recognition.face_encodings(
                image_np, face_locations, model="large"
            )

            if face_encodings:
                return face_encodings[0].tobytes(), None
            else:
                return None, "Could not extract face encoding"

        except Exception as e:
            return None, f"Error processing image: {str(e)}"

    @staticmethod
    def compare_faces(known_encoding, test_image_data, tolerance=None):
        try:
            if tolerance is None:
                import os

                tolerance = float(os.getenv("FACE_RECOGNITION_TOLERANCE", 0.45))

            test_encoding_bytes, error = FaceRecognitionService.extract_face_encoding(
                test_image_data
            )

            if error:
                return False, 0.0, error

            known_encoding_np = np.frombuffer(known_encoding, dtype=np.float64)
            test_encoding_np = np.frombuffer(test_encoding_bytes, dtype=np.float64)

            distance = face_recognition.face_distance(
                [known_encoding_np], test_encoding_np
            )[0]

            is_match = distance <= tolerance
            confidence = max(0, (1 - distance) * 100)

            return is_match, confidence, None

        except Exception as e:
            return False, 0.0, f"Error comparing faces: {str(e)}"
