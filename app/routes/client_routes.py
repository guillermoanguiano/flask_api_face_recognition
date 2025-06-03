from flask import Blueprint

from app.controllers.client_controller import ClientController

client_bp = Blueprint("client", __name__)


@client_bp.route("/clients", methods=["GET"])
def get_clients():
    """Get all clients"""
    return ClientController.get_all_clients()


@client_bp.route("/clients", methods=["POST"])
def create_client():
    """Create client without face (legacy endpoint)"""
    return ClientController.create_client()


@client_bp.route("/clients/<int:client_id>", methods=["GET"])
def get_client(client_id):
    """Get specific client"""
    return ClientController.get_client_by_id(client_id)


@client_bp.route("/clients/<int:client_id>", methods=["PUT"])
def update_client(client_id):
    """Update client"""
    return ClientController.update_client(client_id)


@client_bp.route("/clients/<int:client_id>", methods=["DELETE"])
def delete_client(client_id):
    """Delete client"""
    return ClientController.delete_client(client_id)
