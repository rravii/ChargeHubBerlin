from dataclasses import dataclass
from datetime import datetime
from src.malfunction.domain.value_objects.ReporterId import ReporterId
from src.malfunction.domain.value_objects.StationId import StationId
from src.malfunction.domain.value_objects.IncidentDetails import IncidentDetails


@dataclass
class Incident:
    id: str
    reporter_id: ReporterId
    station_id: StationId
    details: IncidentDetails
    status: str
    created_at: datetime
    resolved_at: datetime | None = None
    solution: str | None = None
