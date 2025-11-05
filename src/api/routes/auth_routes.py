"""
Authentication API routes
Handles user registration, login, and logout
"""
from flask import Blueprint, request, jsonify
from flask_login import current_user
import logging

from ...services import AuthService
from ...core.constants import API_MESSAGES
from ..utils import safe_error_response

logger = logging.getLogger(__name__)

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.json
    username = data.get('username', '')
    password = data.get('password', '')
    
    success, user, error = AuthService.register_user(username, password)
    
    if not success:
        # Use safe error response helper
        status_code = 500 if 'Failed to register user:' in str(error) else 400
        return safe_error_response(
            error, 
            'Failed to register user. Please try again.',
            status_code,
            f"Registration error for user: {username}"
        )
    
    return jsonify({
        'success': True,
        'user': {
            'id': user.id,
            'username': user.username
        }
    })


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login a user"""
    data = request.json
    username = data.get('username', '')
    password = data.get('password', '')
    
    success, user, error = AuthService.login_user_with_credentials(username, password)
    
    if not success:
        status_code = 401 if error == API_MESSAGES['INVALID_CREDENTIALS'] else 400
        return jsonify({
            'success': False,
            'error': error
        }), status_code
    
    return jsonify({
        'success': True,
        'user': {
            'id': user.id,
            'username': user.username
        }
    })


@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Logout the current user"""
    success, error = AuthService.logout_current_user()
    
    if not success:
        logger.error(f"Logout error: {error}")
        return jsonify({
            'success': False,
            'error': 'Failed to logout. Please try again.'
        }), 500
    
    return jsonify({
        'success': True
    })


@auth_bp.route('/current-user', methods=['GET'])
def get_current_user():
    """Get the current logged-in user"""
    if current_user.is_authenticated:
        return jsonify({
            'authenticated': True,
            'user': {
                'id': current_user.id,
                'username': current_user.username
            }
        })
    return jsonify({
        'authenticated': False
    })
