from flask import Blueprint
from app.controllers.client_controller import ClientController

client_bp = Blueprint("client", __name__)


@client_bp.route("/clients", methods=["GET"])
def get_clients():
    """Get list of clients"""
    return ClientController.get_all_clients()


@client_bp.route("/clients/<int:client_id>", methods=["GET"])
def get_client(client_id):
    """Get client by ID"""
    return ClientController.get_client_by_id(client_id)


@client_bp.route("/clients", methods=["POST"])
def create_client():
    """Create new client"""
    return ClientController.create_client()


@client_bp.route("/clients/<int:client_id>", methods=["PUT"])
def update_client(client_id):
    """Update client"""
    return ClientController.update_client(client_id)
