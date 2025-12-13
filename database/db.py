"""
Database utilities (legacy - for backward compatibility)
New code should use DatabaseManager from services
"""
from services.database_manager import DatabaseManager

# For backward compatibility with existing code
def connect_database(db_path: str = "database/platform.db"):
    """
    Legacy function to connect to database
    
    Args:
        db_path: Path to database file
        
    Returns:
        sqlite3.Connection: Database connection
    """
    db_manager = DatabaseManager(db_path)
    return db_manager.connect()