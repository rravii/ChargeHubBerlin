from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Protocol

from src.malfunction.domain.entities.Incident import Incident
from src.malfunction.domain.value_objects.IncidentId import IncidentId


class IncidentRepositoryInterface(ABC):
    """Persistence abstraction for malfunction incidents."""

    @abstractmethod
    def add(self, incident: Incident) -> Incident:
        """Persist a new or updated incident and return it."""
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, incident_id: IncidentId) -> Incident | None:
        """Return the incident with the given id, or None if not found."""
        raise NotImplementedError
