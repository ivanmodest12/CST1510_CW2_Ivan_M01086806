"""
SecurityIncident Entity Class
Represents a cybersecurity incident
"""
from datetime import datetime

class SecurityIncident:
    """Cybersecurity incident domain entity"""
    
    SEVERITY_LEVELS = ['Low', 'Medium', 'High', 'Critical']
    STATUS_VALUES = ['Open', 'In Progress', 'Resolved', 'Closed']
    
    def __init__(self, id: int = None, title: str = "", severity: str = "Medium",
                 status: str = "Open", description: str = "", reported_by: str = "",
                 date: str = None, created_at: str = None):
        """
        Initialize a SecurityIncident object
        
        Args:
            id: Unique identifier
            title: Incident title
            severity: Severity level (Low/Medium/High/Critical)
            status: Current status (Open/In Progress/Resolved/Closed)
            description: Detailed description
            reported_by: Who reported the incident
            date: Incident date
            created_at: Creation timestamp
        """
        self.__id = id
        self.__title = title
        self.__severity = severity if severity in self.SEVERITY_LEVELS else "Medium"
        self.__status = status if status in self.STATUS_VALUES else "Open"
        self.__description = description
        self.__reported_by = reported_by
        self.__date = date or datetime.now().strftime("%Y-%m-%d")
        self.__created_at = created_at or datetime.now().isoformat()
    
    # Getter methods
    @property
    def id(self) -> int:
        return self.__id
    
    @property
    def title(self) -> str:
        return self.__title
    
    @property
    def severity(self) -> str:
        return self.__severity
    
    @property
    def status(self) -> str:
        return self.__status
    
    @property
    def description(self) -> str:
        return self.__description
    
    @property
    def reported_by(self) -> str:
        return self.__reported_by
    
    @property
    def date(self) -> str:
        return self.__date
    
    # Setter methods
    def update_status(self, new_status: str) -> None:
        """Update incident status"""
        if new_status in self.STATUS_VALUES:
            self.__status = new_status
    
    def get_severity_level(self) -> int:
        """Get numeric severity level (1-4)"""
        return self.SEVERITY_LEVELS.index(self.__severity) + 1 if self.__severity in self.SEVERITY_LEVELS else 2
    
    def to_dict(self) -> dict:
        """Convert incident object to dictionary"""
        return {
            'id': self.__id,
            'title': self.__title,
            'severity': self.__severity,
            'status': self.__status,
            'description': self.__description,
            'reported_by': self.__reported_by,
            'date': self.__date,
            'created_at': self.__created_at
        }
    
    def __str__(self) -> str:
        return f"SecurityIncident(id={self.__id}, title='{self.__title}', severity='{self.__severity}', status='{self.__status}')"