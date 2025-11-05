"""
Authentication service
Handles user authentication business logic
"""
from typing import Optional, Tuple
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from ..models import db, User
from ..core.constants import MIN_USERNAME_LENGTH, MIN_PASSWORD_LENGTH, get_auth_error_message


class AuthService:
    """Service for authentication operations"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using werkzeug's secure password hashing"""
        return generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
    
    @staticmethod
    def verify_password(password: str, stored_hash: str) -> bool:
        """Verify a password against a stored hash"""
        try:
            return check_password_hash(stored_hash, password)
        except (ValueError, AttributeError):
            return False
    
    @staticmethod
    def validate_username(username: str) -> Tuple[bool, Optional[str]]:
        """Validate username format"""
        if not username:
            return False, 'Username is required'
        if len(username) < MIN_USERNAME_LENGTH:
            return False, get_auth_error_message('USERNAME_TOO_SHORT')
        return True, None
    
    @staticmethod
    def validate_password(password: str) -> Tuple[bool, Optional[str]]:
        """Validate password format"""
        if not password:
            return False, 'Password is required'
        if len(password) < MIN_PASSWORD_LENGTH:
            return False, get_auth_error_message('PASSWORD_TOO_SHORT')
        return True, None
    
    @staticmethod
    def register_user(username: str, password: str) -> Tuple[bool, Optional[User], Optional[str]]:
        """
        Register a new user
        
        Returns:
            (success, user, error_message)
        """
        username = username.strip()
        
        # Validate username
        valid, error = AuthService.validate_username(username)
        if not valid:
            return False, None, error
        
        # Validate password
        valid, error = AuthService.validate_password(password)
        if not valid:
            return False, None, error
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            return False, None, 'Username already exists'
        
        try:
            # Create new user
            user = User(
                username=username,
                password_hash=AuthService.hash_password(password)
            )
            db.session.add(user)
            db.session.commit()
            
            # Log the user in
            login_user(user)
            
            return True, user, None
        except Exception as e:
            db.session.rollback()
            return False, None, f'Failed to register user: {str(e)}'
    
    @staticmethod
    def login_user_with_credentials(username: str, password: str) -> Tuple[bool, Optional[User], Optional[str]]:
        """
        Authenticate and login a user
        
        Returns:
            (success, user, error_message)
        """
        username = username.strip()
        
        if not username or not password:
            return False, None, 'Username and password are required'
        
        user = User.query.filter_by(username=username).first()
        
        if not user or not AuthService.verify_password(password, user.password_hash):
            return False, None, 'Invalid username or password'
        
        login_user(user)
        return True, user, None
    
    @staticmethod
    def logout_current_user() -> Tuple[bool, Optional[str]]:
        """
        Logout the current user
        
        Returns:
            (success, error_message)
        """
        try:
            logout_user()
            return True, None
        except Exception as e:
            return False, f'Failed to logout: {str(e)}'
