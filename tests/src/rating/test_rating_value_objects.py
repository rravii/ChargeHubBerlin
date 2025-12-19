"""Validation tests for rating-related value objects."""

import pytest
from src.rating.domain.value_objects import StarRating, UserId, StationId


def test_user_id_must_not_be_empty():
    with pytest.raises(ValueError):
        UserId("")


def test_station_id_must_not_be_empty():
    with pytest.raises(ValueError):
        StationId("")


def test_star_rating_accepts_values_1_to_5():
    for v in range(1, 6):
        r = StarRating(v)
        assert r.value == v


@pytest.mark.parametrize("value", [0, 6, -1, 10])
def test_star_rating_rejects_out_of_range_values(value):
    with pytest.raises(ValueError):
        StarRating(value)
