from dataclasses import dataclass
from datetime import datetime
from .DomainEvent import DomainEvent


@dataclass(frozen=True)
class NewRatingCreatedEvent(DomainEvent):
    rating_id: str
    user_id: str
    station_id: str
    stars: int
