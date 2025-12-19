from dataclasses import dataclass
from datetime import datetime
from src.rating.domain.value_objects.UserId import UserId
from src.rating.domain.value_objects.StationId import StationId
from src.rating.domain.value_objects.StarRating import StarRating


@dataclass
class Rating:
    id: str
    user_id: UserId
    station_id: StationId
    stars: StarRating
    text: str | None
    created_at: datetime
