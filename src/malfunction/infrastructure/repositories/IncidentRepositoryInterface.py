"""Repository interface for Incident persistence."""

from abc import ABC, abstractmethod
from typing import Iterable, Optional
from uuid import UUID

from src.malfunction.domain.entities.Incident import Incident


class IncidentRepositoryInterface(ABC):
    """Abstract interface for Incident repository operations."""

    @abstractmethod
    def save(self, incident: Incident) -> None:
        """Persist an incident to storage."""
        ...

    @abstractmethod
    def get_by_id(self, id_: UUID) -> Optional[Incident]:
        """Retrieve incident by its unique ID."""
        ...

    @abstractmethod
    def list_pending(self) -> Iterable[Incident]:
        """Return all incidents with PENDING status."""
        ...

    @abstractmethod
    def get_by_station(self, station_label: str) -> list:
        """Return all incidents for a specific charging station."""
        ...

    @abstractmethod
    def update_status(self, incident_id: str, is_valid: bool, is_solved: bool) -> None:
        """Update the validation and resolution status of an incident."""
        ...

    @abstractmethod
    def get_all(self) -> Iterable[Incident]:
        """Fetch all incidents for admin view."""
        ...
