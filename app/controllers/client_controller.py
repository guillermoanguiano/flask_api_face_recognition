from flask import request, jsonify
from app.services.client_service import ClientService
from datetime import datetime

class ClientController:
    
    @staticmethod
    def get_all_clients():
        """Get all active clients"""
        try:
            clients = ClientService.get_active_clients()
            return jsonify({
                'success': True,
                'clients': [client.to_dict() for client in clients],
                'total': len(clients)
            }), 200
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error getting clients: {str(e)}'
            }), 500
    
    @staticmethod
    def get_client_by_id(client_id):
        """Get client by ID"""
        try:
            client = ClientService.get_client_by_id(client_id)
            
            if not client:
                return jsonify({
                    'success': False,
                    'message': 'Client not found'
                }), 404
            
            return jsonify({
                'success': True,
                'client': client.to_dict()
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error getting client: {str(e)}'
            }), 500
    
    @staticmethod
    def create_client():
        """Create new client"""
        try:
            data = request.get_json()
            
            if not data:
                return jsonify({
                    'success': False,
                    'message': 'No data provided'
                }), 400
            
            name = data.get('name')
            email = data.get('email')
            expiration_date_str = data.get('expiration_date')
            
            if not all([name, email, expiration_date_str]):
                return jsonify({
                    'success': False,
                    'message': 'name, email and expiration_date are required'
                }), 400
            
            try:
                expiration_date = datetime.strptime(expiration_date_str, '%Y-%m-%d').date()
            except ValueError:
                return jsonify({
                    'success': False,
                    'message': 'Invalid date format. Use YYYY-MM-DD'
                }), 400
            
            client, error = ClientService.create_client(
                name=name,
                email=email,
                expiration_date=expiration_date
            )
            
            if error:
                return jsonify({
                    'success': False,
                    'message': f'Error creating client: {error}'
                }), 500
            
            return jsonify({
                'success': True,
                'message': 'Client created successfully',
                'client': client.to_dict()
            }), 201
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Internal server error: {str(e)}'
            }), 500
    
    @staticmethod
    def update_client(client_id):
        """Update existing client"""
        try:
            data = request.get_json()
            if not data:
                return jsonify({
                    'success': False,
                    'message': 'No data provided'
                }), 400
            
            update_data = {}
            
            if 'name' in data:
                update_data['name'] = data['name']
            if 'email' in data:
                update_data['email'] = data['email']
            if 'active' in data:
                update_data['active'] = data['active']
            if 'expiration_date' in data:
                try:
                    update_data['expiration_date'] = datetime.strptime(
                        data['expiration_date'], '%Y-%m-%d'
                    ).date()
                except ValueError:
                    return jsonify({
                        'success': False,
                        'message': 'Invalid date format. Use YYYY-MM-DD'
                    }), 400
            
            client, error = ClientService.update_client(client_id, **update_data)
            
            if error:
                return jsonify({
                    'success': False,
                    'message': error
                }), 404 if "not found" in error else 500
            
            return jsonify({
                'success': True,
                'message': 'Client updated successfully',
                'client': client.to_dict()
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error updating client: {str(e)}'
            }), 500