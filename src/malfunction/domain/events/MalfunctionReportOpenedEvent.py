from dataclasses import dataclass
from datetime import datetime
from src.common.domain.DomainEvent import DomainEvent


@dataclass(frozen=True)
class MalfunctionReportOpenedEvent(DomainEvent):
    incident_id: str
    reporter_id: str
    station_id: str
