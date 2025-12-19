from dataclasses import dataclass
from datetime import datetime
from src.common.domain.DomainEvent import DomainEvent


@dataclass(frozen=True)
class RatingValidatedEvent(DomainEvent):
    rating_id: str
    is_valid: bool
    reason: str | None = None
