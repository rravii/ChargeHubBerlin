from dataclasses import dataclass
from datetime import datetime
from src.common.domain.DomainEvent import DomainEvent


@dataclass(frozen=True)
class ReportValidatedAndSubmittedEvent(DomainEvent):
    incident_id: str
    is_valid: bool
    reason: str | None = None
