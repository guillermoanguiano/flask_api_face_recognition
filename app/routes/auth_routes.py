from flask import Blueprint

from app.controllers.auth_controller import AuthController

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register-face", methods=["POST"])
def register_face():
    return AuthController.register_face()


@auth_bp.route("/verify-access", methods=["POST"])
def verify_access():
    return AuthController.verify_access()


@auth_bp.route("/clients/with-face", methods=["POST"])
def create_client_with_face():
    return AuthController.create_client_with_face()
