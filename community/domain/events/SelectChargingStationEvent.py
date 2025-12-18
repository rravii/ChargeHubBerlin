from dataclasses import dataclass
from datetime import datetime
from .DomainEvent import DomainEvent


@dataclass(frozen=True)
class SelectChargingStationEvent(DomainEvent):
    user_id: str
    station_id: str
