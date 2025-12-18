from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Protocol

from community.domain.entities.Incident import Incident
from community.domain.value_objects.IncidentId import IncidentId


class IncidentRepositoryInterface(ABC):
    """
    Abstraction over incident persistence.

    Allows the domain/application layer to work with Incident objects
    without knowing if they are stored in memory, a database, etc.
    """

    @abstractmethod
    def add(self, incident: Incident) -> Incident:
        """Persist a new or updated incident and return it."""
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, incident_id: IncidentId) -> Incident | None:
        """Return the incident with the given id, or None if not found."""
        raise NotImplementedError
