"""
Database package for Multi-Domain Intelligence Platform
Contains database connection utilities and legacy compatibility functions
"""

# Import the main DatabaseManager from services for backward compatibility
from services.database_manager import DatabaseManager

# Legacy function for backward compatibility with Week 10 code
def connect_database(db_path: str = "database/platform.db"):
    """
    Legacy connection function for backward compatibility
    This maintains compatibility with old code that used connect_database()
    
    Args:
        db_path: Path to SQLite database file
        
    Returns:
        sqlite3.Connection: Database connection object
    """
    db_manager = DatabaseManager(db_path)
    return db_manager.connect()

# Export for public API
__all__ = ['DatabaseManager', 'connect_database']