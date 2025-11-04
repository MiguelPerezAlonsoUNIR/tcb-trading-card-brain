"""
Authentication utilities
"""
from functools import wraps
from flask import jsonify
from flask_login import current_user
from werkzeug.security import generate_password_hash, check_password_hash

def hash_password(password):
    """Hash a password using werkzeug's secure password hashing (pbkdf2)"""
    return generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)

def verify_password(password, stored_hash):
    """Verify a password against a stored hash"""
    try:
        return check_password_hash(stored_hash, password)
    except (ValueError, AttributeError):
        return False

def login_required_api(f):
    """Decorator for API routes that require authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({
                'success': False,
                'error': 'Authentication required'
            }), 401
        return f(*args, **kwargs)
    return decorated_function
