from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
from src.rating.domain.entities.Rating import Rating
from src.rating.domain.value_objects.UserId import UserId
from src.rating.domain.value_objects.StationId import StationId


class RatingRepositoryInterface(ABC):
    """Persistence abstraction for ratings."""

    @abstractmethod
    def upsert(self, rating: Rating) -> Rating:
        """Create or replace a rating record and return it."""

    @abstractmethod
    def get_by_station(self, station_id: StationId) -> List[Rating]:
        """Return all ratings for a station."""

    @abstractmethod
    def get_by_user_and_station(
        self, user_id: UserId, station_id: StationId
    ) -> Rating | None:
        """Return the single rating a user left for a station, if any."""

    @abstractmethod
    def get_average_for_station(self, station_id: StationId) -> float | None:
        """Return average stars for a station or None if no ratings exist."""
