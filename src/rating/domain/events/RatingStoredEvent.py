from dataclasses import dataclass
from datetime import datetime
from src.common.domain.DomainEvent import DomainEvent


@dataclass(frozen=True)
class RatingStoredEvent(DomainEvent):
    rating_id: str
    station_id: str
