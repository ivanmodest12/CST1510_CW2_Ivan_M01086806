"""
Database Manager Service Class
Handles all database operations following Single Responsibility Principle
Refactored from procedural db.py to OOP
"""
import sqlite3
import os
from typing import Optional, List, Dict, Any

class DatabaseManager:
    """Manages database connections and operations for the multi-domain platform"""
    
    def __init__(self, db_path: str = "database/platform.db"):
        """
        Initialize DatabaseManager with database path
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.connection: Optional[sqlite3.Connection] = None
        self._ensure_data_dir()
        self._create_tables()
    
    def _ensure_data_dir(self) -> None:
        """Ensure database directory exists"""
        data_dir = os.path.dirname(self.db_path)
        os.makedirs(data_dir, exist_ok=True)
    
    def connect(self) -> sqlite3.Connection:
        """
        Establish database connection
        
        Returns:
            sqlite3.Connection: Database connection object
        """
        if self.connection is None:
            self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
            self.connection.row_factory = sqlite3.Row
        return self.connection
    
    def _create_tables(self) -> None:
        """Create database tables if they don't exist"""
        conn = self.connect()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT DEFAULT 'user',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Cyber incidents table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cyber_incidents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                severity TEXT NOT NULL,
                status TEXT DEFAULT 'Open',
                description TEXT,
                reported_by TEXT,
                date TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Datasets metadata table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS datasets_metadata (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                source TEXT,
                category TEXT,
                size INTEGER,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # IT tickets table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS it_tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                priority TEXT NOT NULL,
                status TEXT DEFAULT 'Open',
                assigned_to TEXT,
                description TEXT,
                created_date TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
    
    def execute_query(self, sql: str, params: tuple = None) -> sqlite3.Cursor:
        """
        Execute a SQL query
        
        Args:
            sql: SQL query string
            params: Query parameters
            
        Returns:
            sqlite3.Cursor: Database cursor
        """
        conn = self.connect()
        cursor = conn.cursor()
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        return cursor
    
    def fetch_one(self, sql: str, params: tuple = None) -> Optional[Dict[str, Any]]:
        """
        Fetch a single row from database
        
        Args:
            sql: SQL query string
            params: Query parameters
            
        Returns:
            Optional[Dict]: Row as dictionary or None
        """
        cursor = self.execute_query(sql, params)
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def fetch_all(self, sql: str, params: tuple = None) -> List[Dict[str, Any]]:
        """
        Fetch all rows from database
        
        Args:
            sql: SQL query string
            params: Query parameters
            
        Returns:
            List[Dict]: List of rows as dictionaries
        """
        cursor = self.execute_query(sql, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    
    def insert(self, table: str, data: Dict[str, Any]) -> int:
        """
        Insert a record into a table
        
        Args:
            table: Table name
            data: Dictionary of column-value pairs
            
        Returns:
            int: ID of inserted record
        """
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        
        cursor = self.execute_query(sql, tuple(data.values()))
        self.connection.commit()
        return cursor.lastrowid
    
    def update(self, table: str, record_id: int, data: Dict[str, Any]) -> bool:
        """
        Update a record in a table
        
        Args:
            table: Table name
            record_id: ID of record to update
            data: Dictionary of column-value pairs to update
            
        Returns:
            bool: True if update successful
        """
        set_clause = ', '.join([f"{key} = ?" for key in data.keys()])
        sql = f"UPDATE {table} SET {set_clause} WHERE id = ?"
        
        params = tuple(data.values()) + (record_id,)
        cursor = self.execute_query(sql, params)
        self.connection.commit()
        return cursor.rowcount > 0
    
    def delete(self, table: str, record_id: int) -> bool:
        """
        Delete a record from a table
        
        Args:
            table: Table name
            record_id: ID of record to delete
            
        Returns:
            bool: True if deletion successful
        """
        sql = f"DELETE FROM {table} WHERE id = ?"
        cursor = self.execute_query(sql, (record_id,))
        self.connection.commit()
        return cursor.rowcount > 0
    
    def close(self) -> None:
        """Close database connection"""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def __enter__(self):
        """Context manager entry"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()