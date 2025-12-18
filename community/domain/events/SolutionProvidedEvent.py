from dataclasses import dataclass
from datetime import datetime
from .DomainEvent import DomainEvent


@dataclass(frozen=True)
class SolutionProvidedEvent(DomainEvent):
    incident_id: str
    solution_description: str
