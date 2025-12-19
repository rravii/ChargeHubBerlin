from __future__ import annotations

from typing import Dict

from src.malfunction.domain.entities.Incident import Incident
from src.malfunction.domain.value_objects.IncidentId import IncidentId
from .IncidentRepositoryInterface import IncidentRepositoryInterface


class InMemoryIncidentRepository(IncidentRepositoryInterface):
    """In-memory incident store for tests and demos."""

    def __init__(self) -> None:
        self._incidents: Dict[str, Incident] = {}

    def add(self, incident: Incident) -> Incident:
        """Insert or replace an incident and return it."""
        self._incidents[incident.id] = incident
        return incident

    def get_by_id(self, incident_id: IncidentId | str) -> Incident | None:
        """Fetch an incident by id (accepts IncidentId or raw string)."""
        key = incident_id.value if isinstance(incident_id, IncidentId) else incident_id
        return self._incidents.get(key)
