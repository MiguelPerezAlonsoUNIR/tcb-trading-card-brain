"""
API utilities
Common decorators and helpers for API routes
"""
from functools import wraps
from flask import jsonify
from flask_login import current_user

from ..core.constants import API_MESSAGES


def login_required_api(f):
    """Decorator for API routes that require authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({
                'success': False,
                'error': API_MESSAGES['AUTH_REQUIRED']
            }), 401
        return f(*args, **kwargs)
    return decorated_function
