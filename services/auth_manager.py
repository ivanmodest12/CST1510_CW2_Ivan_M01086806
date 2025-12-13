"""
Authentication Manager Service Class
Handles user authentication, registration, and session management
Refactored from procedural users.py to OOP
"""
import bcrypt
from typing import Optional
from models.user import User
from services.database_manager import DatabaseManager

class AuthManager:
    """Manages user authentication and registration"""
    
    def __init__(self, db_manager: DatabaseManager):
        """
        Initialize AuthManager with database manager
        
        Args:
            db_manager: DatabaseManager instance for data access
        """
        self.db_manager = db_manager
    
    def register(self, username: str, password: str, role: str = "user") -> bool:
        """
        Register a new user
        
        Args:
            username: Desired username
            password: Plain text password
            role: User role (default: user)
            
        Returns:
            bool: True if registration successful
        """
        # Check if username already exists
        existing = self.db_manager.fetch_one(
            "SELECT id FROM users WHERE username = ?", 
            (username,)
        )
        if existing:
            return False
        
        # Create user object and hash password
        user = User(username=username, role=role)
        user.set_password(password)
        
        # Insert into database
        user_data = {
            'username': user.username,
            'password_hash': user._User__password_hash,  # Access private attribute
            'role': user.role
        }
        
        try:
            user_id = self.db_manager.insert('users', user_data)
            return user_id is not None
        except Exception as e:
            print(f"Registration error: {e}")
            return False
    
    def login(self, username: str, password: str) -> bool:
        """
        Authenticate a user
        
        Args:
            username: Username to authenticate
            password: Password to verify
            
        Returns:
            bool: True if authentication successful
        """
        # Get user from database
        user_data = self.db_manager.fetch_one(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        )
        
        if not user_data:
            return False
        
        # Create User object from database data
        user = User(
            id=user_data['id'],  # CHANGED: user_id → id
            username=user_data['username'],
            password_hash=user_data['password_hash'],
            role=user_data['role'],
            created_at=user_data['created_at']
        )
        
        # Verify password
        return user.verify_password(password)
    
    def get_user(self, username: str) -> Optional[User]:
        """
        Get User object by username
        
        Args:
            username: Username to look up
            
        Returns:
            Optional[User]: User object or None if not found
        """
        user_data = self.db_manager.fetch_one(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        )
        
        if not user_data:
            return None
        
        return User(
            id=user_data['id'],  # CHANGED: user_id → id
            username=user_data['username'],
            password_hash=user_data['password_hash'],
            role=user_data['role'],
            created_at=user_data['created_at']
        )
    
    def change_password(self, username: str, old_password: str, new_password: str) -> bool:
        """
        Change user password
        
        Args:
            username: Username
            old_password: Current password
            new_password: New password
            
        Returns:
            bool: True if password changed successfully
        """
        # First verify old password
        if not self.login(username, old_password):
            return False
        
        # Get user
        user = self.get_user(username)
        if not user:
            return False
        
        # Update password
        user.set_password(new_password)
        
        # Update in database
        return self.db_manager.update(
            'users',
            user.id,
            {'password_hash': user._User__password_hash}
        )
    
    def get_user_role(self, username: str) -> Optional[str]:
        """
        Get role of a user
        
        Args:
            username: Username
            
        Returns:
            Optional[str]: User role or None if not found
        """
        user_data = self.db_manager.fetch_one(
            "SELECT role FROM users WHERE username = ?",
            (username,)
        )
        return user_data['role'] if user_data else None
    
    def user_exists(self, username: str) -> bool:
        """
        Check if user exists
        
        Args:
            username: Username to check
            
        Returns:
            bool: True if user exists
        """
        user_data = self.db_manager.fetch_one(
            "SELECT id FROM users WHERE username = ?",
            (username,)
        )
        return user_data is not None