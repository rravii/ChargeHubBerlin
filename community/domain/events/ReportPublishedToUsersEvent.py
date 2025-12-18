from dataclasses import dataclass
from datetime import datetime
from .DomainEvent import DomainEvent


@dataclass(frozen=True)
class ReportPublishedToUsersEvent(DomainEvent):
    incident_id: str
