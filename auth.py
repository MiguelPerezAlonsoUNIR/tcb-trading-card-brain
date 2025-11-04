"""
Authentication utilities
"""
from functools import wraps
from flask import jsonify
from flask_login import current_user
import hashlib
import secrets

def hash_password(password):
    """Hash a password using SHA-256 with salt"""
    salt = secrets.token_hex(16)
    pwd_hash = hashlib.sha256((password + salt).encode()).hexdigest()
    return f"{salt}${pwd_hash}"

def verify_password(password, stored_hash):
    """Verify a password against a stored hash"""
    try:
        salt, pwd_hash = stored_hash.split('$')
        test_hash = hashlib.sha256((password + salt).encode()).hexdigest()
        return test_hash == pwd_hash
    except:
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
