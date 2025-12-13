"""
User Entity Class
Represents a user in the system with authentication capabilities
"""
import bcrypt
from datetime import datetime

class User:
    """User domain entity with authentication methods"""
    
    def __init__(self, id: int = None, username: str = "", password_hash: str = "", 
                 role: str = "user", created_at: str = None):
        """
        Initialize a User object
        
        Args:
            id: Unique identifier
            username: User's login name
            password_hash: Hashed password
            role: User role (admin/user)
            created_at: Account creation timestamp
        """
        self.__id = id
        self.__username = username
        self.__password_hash = password_hash
        self.__role = role
        self.__created_at = created_at or datetime.now().isoformat()
    
    # Getter methods
    @property
    def id(self) -> int:
        return self.__id
    
    @property
    def username(self) -> str:
        return self.__username
    
    @property
    def role(self) -> str:
        return self.__role
    
    @property
    def created_at(self) -> str:
        return self.__created_at
    
    # Authentication methods
    def verify_password(self, plain_password: str) -> bool:
        """
        Verify if plain password matches the stored hash
        
        Args:
            plain_password: Password to verify
            
        Returns:
            bool: True if password matches
        """
        if not self.__password_hash:
            return False
        try:
            return bcrypt.checkpw(
                plain_password.encode('utf-8'),
                self.__password_hash.encode('utf-8')
            )
        except:
            return False
    
    def set_password(self, plain_password: str) -> None:
        """
        Hash and set password
        
        Args:
            plain_password: Plain text password to hash
        """
        salt = bcrypt.gensalt()
        self.__password_hash = bcrypt.hashpw(
            plain_password.encode('utf-8'),
            salt
        ).decode('utf-8')
    
    def to_dict(self) -> dict:
        """Convert user object to dictionary (excluding password)"""
        return {
            'id': self.__id,
            'username': self.__username,
            'role': self.__role,
            'created_at': self.__created_at
        }
    
    def __str__(self) -> str:
        return f"User(id={self.__id}, username='{self.__username}', role='{self.__role}')"