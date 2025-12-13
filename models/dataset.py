"""
Dataset Entity Class
Represents a data science dataset
"""
from datetime import datetime

class Dataset:
    """Dataset domain entity for data science domain"""
    
    def __init__(self, id: int = None, name: str = "", source: str = "", 
                 category: str = "", size: int = 0, description: str = "",
                 created_at: str = None):
        """
        Initialize a Dataset object
        
        Args:
            id: Unique identifier
            name: Dataset name
            source: Data source
            category: Dataset category
            size: Size in bytes
            description: Dataset description
            created_at: Creation timestamp
        """
        self.__id = id
        self.__name = name
        self.__source = source
        self.__category = category
        self.__size = size if size is not None else 0  # Convert None to 0
        self.__description = description
        self.__created_at = created_at or datetime.now().isoformat()
    
    # Getter methods
    @property
    def id(self) -> int:
        return self.__id
    
    @property
    def name(self) -> str:
        return self.__name
    
    @property
    def source(self) -> str:
        return self.__source
    
    @property
    def category(self) -> str:
        return self.__category
    
    @property
    def size(self) -> int:
        return self.__size
    
    @property
    def description(self) -> str:
        return self.__description
    
    @property
    def created_at(self) -> str:
        return self.__created_at
    
    # Business logic methods
    def calculate_size_mb(self) -> float:
        """Calculate size in megabytes"""
        if self.__size is None or self.__size == 0:
            return 0.0
        return self.__size / (1024 * 1024)
    
    def calculate_size_gb(self) -> float:
        """Calculate size in gigabytes"""
        if self.__size is None or self.__size == 0:
            return 0.0
        return self.__size / (1024 * 1024 * 1024)
    
    def to_dict(self) -> dict:
        """Convert dataset object to dictionary"""
        return {
            'id': self.__id,
            'name': self.__name,
            'source': self.__source,
            'category': self.__category,
            'size': self.__size,
            'size_mb': self.calculate_size_mb(),
            'description': self.__description,
            'created_at': self.__created_at
        }
    
    def __str__(self) -> str:
        return f"Dataset(id={self.__id}, name='{self.__name}', category='{self.__category}', size={self.__size} bytes)"