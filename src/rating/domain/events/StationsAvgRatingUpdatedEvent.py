from dataclasses import dataclass
from datetime import datetime
from src.common.domain.DomainEvent import DomainEvent


@dataclass(frozen=True)
class StationsAvgRatingUpdatedEvent(DomainEvent):
    station_id: str
    new_average: float
