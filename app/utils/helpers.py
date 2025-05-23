from datetime import datetime, date
import base64
import io
from PIL import Image


class DateHelper:
    @staticmethod
    def is_date_expired(expiration_date):
        """Check if date has expired"""
        if isinstance(expiration_date, str):
            expiration_date = datetime.strptime(expiration_date, "%Y-%m-%d").date()
        return expiration_date < date.today()


class ImageHelper:
    @staticmethod
    def validate_image_format(image_data):
        """Validate base64 image format"""
        try:
            if not image_data.startswith("data:image/"):
                return False, "Invalid image format"

            image_data = base64.b64decode(image_data.split(",")[1])

            image = Image.open(io.BytesIO(image_data))

            if image.format not in ["JPEG", "PNG", "JPG"]:
                return False, "Only JPEG and PNG images are accepted"

            return True, None

        except Exception as e:
            return False, f"Error validating image: {str(e)}"
