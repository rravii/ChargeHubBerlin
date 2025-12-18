from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
from community.domain.entities.Rating import Rating
from community.domain.value_objects.UserId import UserId
from community.domain.value_objects.StationId import StationId


class RatingRepositoryInterface(ABC):
    @abstractmethod
    def upsert(self, rating: Rating) -> Rating: ...

    @abstractmethod
    def get_by_station(self, station_id: StationId) -> List[Rating]: ...

    @abstractmethod
    def get_by_user_and_station(
        self, user_id: UserId, station_id: StationId
    ) -> Rating | None: ...

    @abstractmethod
    def get_average_for_station(self, station_id: StationId) -> float | None: ...
