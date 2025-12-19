"""Integration-style tests for RatingService event flow and persistence."""

import pytest
from datetime import datetime

from src.rating.domain.value_objects import UserId, StationId, StarRating
from src.rating.infrastructure.repositories import InMemoryRatingRepository
from src.infrastructure.EventBus import InMemoryEventBus
from src.rating.application.services import RatingService
from src.rating.domain.events import (
    SelectChargingStation,
    NewRatingCreated,
    RatingSubmitted,
    RatingStored,
    StationsAvgRatingUpdated,
    ReviewPublished,
    RatingMadeVisibleToUsers,
)


def _find(events, event_type):
    return [e for e in events if isinstance(e, event_type)]


def test_add_first_rating_happy_path_emits_full_flow():
    repo = InMemoryRatingRepository()
    bus = InMemoryEventBus()
    service = RatingService(repo, bus)

    user = UserId("user-1")
    station = StationId("station-1")

    service.add_or_update_rating(
        user_id=user,
        station_id=station,
        stars=StarRating(4),
        text="Good station",
    )

    # domain result
    assert repo.get_average_for_station(station) == 4.0

    # events
    assert _find(bus.published, SelectChargingStation)
    assert _find(bus.published, NewRatingCreated)
    assert _find(bus.published, RatingSubmitted)
    assert _find(bus.published, RatingStored)
    assert _find(bus.published, StationsAvgRatingUpdated)
    assert _find(bus.published, ReviewPublished)
    assert _find(bus.published, RatingMadeVisibleToUsers)


def test_update_rating_same_user_station_keeps_single_rating_and_updates_average():
    repo = InMemoryRatingRepository()
    bus = InMemoryEventBus()
    service = RatingService(repo, bus)

    user = UserId("user-1")
    station = StationId("station-1")

    service.add_or_update_rating(user, station, StarRating(3), "ok")
    service.add_or_update_rating(user, station, StarRating(5), "great")

    ratings = repo.get_by_station(station)
    assert len(ratings) == 1
    assert ratings[0].stars.value == 5
    assert repo.get_average_for_station(station) == 5.0
