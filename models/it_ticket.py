"""
ITTicket Entity Class
Represents an IT support ticket
"""
from datetime import datetime

class ITTicket:
    """IT support ticket domain entity"""
    
    PRIORITY_LEVELS = ['Low', 'Medium', 'High', 'Critical']
    STATUS_VALUES = ['Open', 'In Progress', 'Resolved', 'Closed']
    
    def __init__(self, id: int = None, title: str = "", priority: str = "Medium",
                 status: str = "Open", assigned_to: str = "", description: str = "",
                 created_date: str = None, created_at: str = None):
        """
        Initialize an ITTicket object
        
        Args:
            id: Unique identifier
            title: Ticket title
            priority: Priority level (Low/Medium/High/Critical)
            status: Current status (Open/In Progress/Resolved/Closed)
            assigned_to: Staff member assigned
            description: Ticket description
            created_date: Ticket creation date
            created_at: Creation timestamp
        """
        self.__id = id
        self.__title = title
        self.__priority = priority if priority in self.PRIORITY_LEVELS else "Medium"
        self.__status = status if status in self.STATUS_VALUES else "Open"
        self.__assigned_to = assigned_to
        self.__description = description
        self.__created_date = created_date or datetime.now().strftime("%Y-%m-%d")
        self.__created_at = created_at or datetime.now().isoformat()
    
    # Getter methods
    @property
    def id(self) -> int:
        return self.__id
    
    @property
    def title(self) -> str:
        return self.__title
    
    @property
    def priority(self) -> str:
        return self.__priority
    
    @property
    def status(self) -> str:
        return self.__status
    
    @property
    def assigned_to(self) -> str:
        return self.__assigned_to
    
    @property
    def description(self) -> str:
        return self.__description
    
    @property
    def created_date(self) -> str:
        return self.__created_date
    
    @property
    def created_at(self) -> str:
        return self.__created_at
    
    # Business logic methods
    def assign_to(self, staff_name: str) -> None:
        """Assign ticket to a staff member"""
        self.__assigned_to = staff_name
    
    def close_ticket(self) -> None:
        """Close the ticket"""
        self.__status = "Closed"
    
    def update_status(self, new_status: str) -> None:
        """Update ticket status"""
        if new_status in self.STATUS_VALUES:
            self.__status = new_status
    
    def get_priority_level(self) -> int:
        """Get numeric priority level (1-4)"""
        return self.PRIORITY_LEVELS.index(self.__priority) + 1 if self.__priority in self.PRIORITY_LEVELS else 2
    
    def to_dict(self) -> dict:
        """Convert ticket object to dictionary"""
        return {
            'id': self.__id,
            'title': self.__title,
            'priority': self.__priority,
            'status': self.__status,
            'assigned_to': self.__assigned_to,
            'description': self.__description,
            'created_date': self.__created_date,
            'created_at': self.__created_at
        }
    
    def __str__(self) -> str:
        return f"ITTicket(id={self.__id}, title='{self.__title}', priority='{self.__priority}', status='{self.__status}')"