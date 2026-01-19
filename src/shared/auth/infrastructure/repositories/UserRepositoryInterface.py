"""Repository interface for User persistence."""

from abc import ABC, abstractmethod
from typing import Optional, List

from src.shared.auth.domain.entities.User import User
from src.shared.auth.domain.value_objects.Email import Email


class UserRepositoryInterface(ABC):
    """Abstract interface for User repository operations."""
    
    @abstractmethod
    def save(self, user: User) -> None:
        """Persist user to storage."""
        ...
    
    @abstractmethod
    def find_by_email(self, email: Email) -> Optional[User]:
        """Retrieve user by email."""
        ...
    
    @abstractmethod
    def get_pending_operators(self) -> List[tuple]:
        """Get all operators awaiting approval."""
        ...
    
    @abstractmethod
    def approve_operator(self, email: Email) -> bool:
        """Approve operator account."""
        ...
    
    @abstractmethod
    def delete_user(self, email: Email) -> bool:
        """Delete user account."""
        ...
