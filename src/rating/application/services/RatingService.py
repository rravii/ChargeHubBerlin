from __future__ import annotations
from datetime import datetime
from uuid import uuid4

from src.rating.domain.entities.Rating import Rating
from src.rating.domain.value_objects.UserId import UserId
from src.rating.domain.value_objects.StationId import StationId
from src.rating.domain.value_objects.StarRating import StarRating
from src.rating.domain.events.SelectChargingStationEvent import SelectChargingStationEvent
from src.rating.domain.events.NewRatingCreatedEvent import NewRatingCreatedEvent
from src.rating.domain.events.RatingValidatedEvent import RatingValidatedEvent
from src.rating.domain.events.RatingSubmittedEvent import RatingSubmittedEvent
from src.rating.domain.events.RatingStoredEvent import RatingStoredEvent
from src.rating.domain.events.StationsAvgRatingUpdatedEvent import (
    StationsAvgRatingUpdatedEvent,
)
from src.rating.domain.events.ReviewPublishedEvent import ReviewPublishedEvent
from src.rating.domain.events.RatingMadeVisibleToUsersEvent import (
    RatingMadeVisibleToUsersEvent,
)
from src.rating.infrastructure.repositories.RatingRepositoryInterface import (
    RatingRepositoryInterface,
)
from src.infrastructure.EventBus import InMemoryEventBus


class RatingService:
    """Application service to create or update ratings and emit domain events."""

    def __init__(
        self,
        repository: RatingRepositoryInterface,
        event_bus: InMemoryEventBus,
    ) -> None:
        """Wire up repository and event bus dependencies."""
        self._repo = repository
        self._events = event_bus

    def add_or_update_rating(
        self,
        user_id: UserId,
        station_id: StationId,
        stars: StarRating,
        text: str | None = None,
    ) -> Rating:
        """
        Upsert a rating for a user/station, publish the rating lifecycle events,
        and return the persisted rating.
        """
        now = datetime.utcnow()

        self._events.publish(
            SelectChargingStationEvent(now, user_id.value, station_id.value)
        )

        self._events.publish(
            RatingValidatedEvent(now, "pending", True, None)
        )

        existing = self._repo.get_by_user_and_station(user_id, station_id)

        if existing:
            rating_id = existing.id
            rating = Rating(
                id=rating_id,
                user_id=user_id,
                station_id=station_id,
                stars=stars,
                text=text,
                created_at=existing.created_at,
            )
        else:
            rating_id = str(uuid4())
            rating = Rating(
                id=rating_id,
                user_id=user_id,
                station_id=station_id,
                stars=stars,
                text=text,
                created_at=now,
            )
            self._events.publish(
                NewRatingCreatedEvent(
                    now,
                    rating_id=rating_id,
                    user_id=user_id.value,
                    station_id=station_id.value,
                    stars=stars.value,
                )
            )

        self._events.publish(
            RatingSubmittedEvent(now, rating_id, user_id.value, station_id.value)
        )

        saved = self._repo.upsert(rating)
        self._events.publish(
            RatingStoredEvent(now, saved.id, station_id.value)
        )

        avg = self._repo.get_average_for_station(station_id) or stars.value
        self._events.publish(
            StationsAvgRatingUpdatedEvent(now, station_id.value, avg)
        )

        self._events.publish(ReviewPublishedEvent(now, saved.id, station_id.value))
        self._events.publish(
            RatingMadeVisibleToUsersEvent(now, saved.id, station_id.value)
        )
        return saved
