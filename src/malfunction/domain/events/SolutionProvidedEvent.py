from dataclasses import dataclass
from datetime import datetime
from src.common.domain.DomainEvent import DomainEvent


@dataclass(frozen=True)
class SolutionProvidedEvent(DomainEvent):
    incident_id: str
    solution_description: str
