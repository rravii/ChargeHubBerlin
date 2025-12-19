from dataclasses import dataclass
from datetime import datetime
from src.common.domain.DomainEvent import DomainEvent


@dataclass(frozen=True)
class ReportNotifiedToAdminAndOperatorEvent(DomainEvent):
    incident_id: str
    admin_id: str | None
    operator_id: str | None
