from dataclasses import dataclass
from datetime import datetime
from .DomainEvent import DomainEvent


@dataclass(frozen=True)
class RatingMadeVisibleToUsersEvent(DomainEvent):
    rating_id: str
    station_id: str
