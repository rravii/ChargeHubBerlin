from __future__ import annotations

from typing import Dict

from community.domain.entities.Incident import Incident
from community.domain.value_objects.IncidentId import IncidentId
from .IncidentRepositoryInterface import IncidentRepositoryInterface


class InMemoryIncidentRepository(IncidentRepositoryInterface):
    """
    Simple in-memory implementation of IncidentRepositoryInterface.

    Intended for TDD, demos, and tests. Data is lost when the process exits.
    """

    def __init__(self) -> None:
        self._incidents: Dict[str, Incident] = {}

    def add(self, incident: Incident) -> Incident:
        self._incidents[incident.id] = incident
        return incident

    def get_by_id(self, incident_id: IncidentId | str) -> Incident | None:
        key = incident_id.value if isinstance(incident_id, IncidentId) else incident_id
        return self._incidents.get(key)
