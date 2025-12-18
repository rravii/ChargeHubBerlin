from dataclasses import dataclass
from datetime import datetime
from .DomainEvent import DomainEvent


@dataclass(frozen=True)
class RatingSubmittedEvent(DomainEvent):
    rating_id: str
    user_id: str
    station_id: str
