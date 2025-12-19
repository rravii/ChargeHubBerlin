"""Validation tests for malfunction value objects."""

import pytest
from src.malfunction.domain.value_objects import (
    IncidentId,
    ReporterId,
    StationId,
    IncidentDetails,
)


def test_incident_id_not_empty():
    with pytest.raises(ValueError):
        IncidentId("")


def test_reporter_id_not_empty():
    with pytest.raises(ValueError):
        ReporterId("")


def test_incident_details_must_have_description():
    with pytest.raises(ValueError):
        IncidentDetails(description="")


def test_incident_details_accepts_valid_description():
    details = IncidentDetails(description="Charger not working")
    assert "Charger" in details.description
