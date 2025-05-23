from flask import Blueprint
from app.controllers.auth_controller import AuthController

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register-face", methods=["POST"])
def register_face():
    """Register client's face"""
    return AuthController.register_face()


@auth_bp.route("/verify-access", methods=["POST"])
def verify_access():
    """Verify access with facial recognition"""
    return AuthController.verify_access()
