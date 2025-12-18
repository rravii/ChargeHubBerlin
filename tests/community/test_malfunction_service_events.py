import pytest
from community.domain.value_objects import (
    IncidentId,
    ReporterId,
    StationId,
    IncidentDetails,
)
from community.infrastructure.malfunction_repositories import (
    InMemoryIncidentRepository,
)
from community.infrastructure.event_bus import InMemoryEventBus
from community.application.malfunction_service import MalfunctionService
from community.domain.events import (
    MalfunctionReportOpened,
    DetailsEntered,
    ReportValidatedAndSubmitted,
    ReportNotifiedToAdminAndOperator,
    ReportPublishedToUsers,
    WarningDisplayedToAllUsers,
    PointsAwardedToReporter,
    SolutionProvided,
    IssuesStatusUpdateReport,
)


def _find(events, event_type):
    return [e for e in events if isinstance(e, event_type)]


def test_open_malfunction_report_happy_path_resident():
    repo = InMemoryIncidentRepository()
    bus = InMemoryEventBus()
    service = MalfunctionService(repo, bus)

    reporter = ReporterId("resident-1")
    station = StationId("station-1")
    details = IncidentDetails("Cable broken")

    incident = service.open_report(
        reporter_id=reporter,
        station_id=station,
        details=details,
        reporter_is_resident=True,
    )

    assert incident is not None
    assert incident.status == "OPEN"

    events = bus.published
    assert _find(events, MalfunctionReportOpened)
    assert _find(events, DetailsEntered)
    assert _find(events, ReportValidatedAndSubmitted)
    assert _find(events, ReportNotifiedToAdminAndOperator)
    assert _find(events, ReportPublishedToUsers)
    assert _find(events, WarningDisplayedToAllUsers)
    assert _find(events, PointsAwardedToReporter)


def test_provide_solution_updates_status_and_emits_events():
    repo = InMemoryIncidentRepository()
    bus = InMemoryEventBus()
    service = MalfunctionService(repo, bus)

    reporter = ReporterId("resident-1")
    station = StationId("station-1")
    details = IncidentDetails("Screen off")

    incident = service.open_report(
        reporter_id=reporter,
        station_id=station,
        details=details,
        reporter_is_resident=True,
    )

    bus.published.clear()

    service.provide_solution(
        incident_id=incident.id,
        solution="Rebooted charger",
    )

    assert repo.get_by_id(incident.id).status == "RESOLVED"
    events = bus.published
    assert _find(events, SolutionProvided)
    assert _find(events, IssuesStatusUpdateReport)
