"""
API utilities
Common decorators and helpers for API routes
"""
from functools import wraps
from flask import jsonify
from flask_login import current_user
import logging

from ..core.constants import API_MESSAGES, is_safe_error_message

logger = logging.getLogger(__name__)


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


def safe_error_response(error: str, default_message: str, status_code: int = 500, log_context: str = ""):
    """
    Safely return an error response, logging sensitive details but only exposing safe messages
    
    Args:
        error: The error message to evaluate
        default_message: Generic message to return if error is not safe
        status_code: HTTP status code
        log_context: Additional context for logging
        
    Returns:
        Flask JSON response tuple
    """
    if is_safe_error_message(error):
        # Error is safe to expose
        return jsonify({
            'success': False,
            'error': error
        }), status_code
    else:
        # Log the actual error but return generic message
        logger.error(f"{log_context}: {error}" if log_context else error)
        return jsonify({
            'success': False,
            'error': default_message
        }), status_code
