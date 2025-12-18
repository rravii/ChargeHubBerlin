from __future__ import annotations
from collections import defaultdict
from typing import Dict, List

from .RatingRepositoryInterface import RatingRepositoryInterface
from community.domain.entities.Rating import Rating
from community.domain.value_objects.UserId import UserId
from community.domain.value_objects.StationId import StationId


class InMemoryRatingRepository(RatingRepositoryInterface):
    def __init__(self) -> None:
        self._ratings: Dict[str, Rating] = {}
        self._by_station: Dict[str, list[str]] = defaultdict(list)
        self._by_user_station: Dict[tuple[str, str], str] = {}

    def upsert(self, rating: Rating) -> Rating:
        key = (rating.user_id.value, rating.station_id.value)
        existing_id = self._by_user_station.get(key)

        if existing_id:
            rating.id = existing_id
        else:
            self._by_station[rating.station_id.value].append(rating.id)
            self._by_user_station[key] = rating.id

        self._ratings[rating.id] = rating
        return rating

    def get_by_station(self, station_id: StationId) -> list[Rating]:
        ids = self._by_station.get(station_id.value, [])
        return [self._ratings[i] for i in ids]

    def get_by_user_and_station(
        self, user_id: UserId, station_id: StationId
    ) -> Rating | None:
        key = (user_id.value, station_id.value)
        rating_id = self._by_user_station.get(key)
        if not rating_id:
            return None
        return self._ratings[rating_id]

    def get_average_for_station(self, station_id: StationId) -> float | None:
        ratings = self.get_by_station(station_id)
        if not ratings:
            return None
        return sum(r.stars.value for r in ratings) / len(ratings)
