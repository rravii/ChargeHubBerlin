from dataclasses import dataclass
from datetime import datetime
from .DomainEvent import DomainEvent


@dataclass(frozen=True)
class PointsAwardedToReporterEvent(DomainEvent):
    incident_id: str
    reporter_id: str
    points: int
