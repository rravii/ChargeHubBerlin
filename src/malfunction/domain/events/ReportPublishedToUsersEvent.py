from dataclasses import dataclass
from datetime import datetime
from src.common.domain.DomainEvent import DomainEvent


@dataclass(frozen=True)
class ReportPublishedToUsersEvent(DomainEvent):
    incident_id: str
