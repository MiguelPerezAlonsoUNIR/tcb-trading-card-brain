"""
Authentication utilities
Backwards compatibility wrapper for new service layer
"""
from src.services import AuthService
from src.api.utils import login_required_api

# Backwards compatibility functions
def hash_password(password):
    """Hash a password using werkzeug's secure password hashing (pbkdf2)"""
    return AuthService.hash_password(password)

def verify_password(password, stored_hash):
    """Verify a password against a stored hash"""
    return AuthService.verify_password(password, stored_hash)

# Export the decorator
__all__ = ['hash_password', 'verify_password', 'login_required_api']
