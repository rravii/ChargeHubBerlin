from dataclasses import dataclass
from datetime import datetime
from .DomainEvent import DomainEvent


@dataclass(frozen=True)
class DetailsEnteredEvent(DomainEvent):
    incident_id: str
    description: str
