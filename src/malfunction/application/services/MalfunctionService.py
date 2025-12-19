from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from src.malfunction.domain.entities.Incident import Incident
from src.malfunction.domain.value_objects.IncidentId import IncidentId
from src.malfunction.domain.value_objects.ReporterId import ReporterId
from src.malfunction.domain.value_objects.StationId import StationId
from src.malfunction.domain.value_objects.IncidentDetails import IncidentDetails
from src.malfunction.domain.events.MalfunctionReportOpenedEvent import (
    MalfunctionReportOpenedEvent,
)
from src.malfunction.domain.events.DetailsEnteredEvent import DetailsEnteredEvent
from src.malfunction.domain.events.ReportValidatedAndSubmittedEvent import (
    ReportValidatedAndSubmittedEvent,
)
from src.malfunction.domain.events.ReportNotifiedToAdminAndOperatorEvent import (
    ReportNotifiedToAdminAndOperatorEvent,
)
from src.malfunction.domain.events.ReportPublishedToUsersEvent import (
    ReportPublishedToUsersEvent,
)
from src.malfunction.domain.events.WarningDisplayedToAllUsersEvent import (
    WarningDisplayedToAllUsersEvent,
)
from src.malfunction.domain.events.PointsAwardedToReporterEvent import (
    PointsAwardedToReporterEvent,
)
from src.malfunction.domain.events.SolutionProvidedEvent import SolutionProvidedEvent
from src.malfunction.domain.events.IssuesStatusUpdateReportEvent import (
    IssuesStatusUpdateReportEvent,
)
from src.malfunction.infrastructure.repositories.IncidentRepositoryInterface import (
    IncidentRepositoryInterface,
)
from src.infrastructure.EventBus import InMemoryEventBus


class MalfunctionService:
    """Application service for the malfunction report flow."""

    def __init__(
        self,
        repository: IncidentRepositoryInterface,
        event_bus: InMemoryEventBus,
    ) -> None:
        self._repo = repository
        self._events = event_bus

    def open_report(
        self,
        reporter_id: ReporterId,
        station_id: StationId,
        details: IncidentDetails,
        reporter_is_resident: bool,
    ) -> Incident:
        """Persist a new incident and emit all events for opening a report."""
        now = datetime.utcnow()
        incident_id = IncidentId(str(uuid4()))

        incident = Incident(
            id=incident_id.value,
            reporter_id=reporter_id,
            station_id=station_id,
            details=details,
            status="OPEN",
            created_at=now,
        )
        self._repo.add(incident)

        # Event: report opened
        self._events.publish(
            MalfunctionReportOpenedEvent(
                occurred_at=now,
                incident_id=incident.id,
                reporter_id=reporter_id.value,
                station_id=station_id.value,
            )
        )

        # Event: details entered
        self._events.publish(
            DetailsEnteredEvent(
                occurred_at=now,
                incident_id=incident.id,
                description=details.description,
            )
        )

        # Simple validation: if we are here, it is considered valid
        self._events.publish(
            ReportValidatedAndSubmittedEvent(
                occurred_at=now,
                incident_id=incident.id,
                is_valid=True,
                reason=None,
            )
        )

        # Notify admin and operator (ids are hard-coded placeholders)
        self._events.publish(
            ReportNotifiedToAdminAndOperatorEvent(
                occurred_at=now,
                incident_id=incident.id,
                admin_id="admin-1",
                operator_id="operator-1",
            )
        )

        # Publish to users and show warning
        self._events.publish(
            ReportPublishedToUsersEvent(
                occurred_at=now,
                incident_id=incident.id,
            )
        )
        self._events.publish(
            WarningDisplayedToAllUsersEvent(
                occurred_at=now,
                incident_id=incident.id,
            )
        )

        # Optional: award points to resident reporters
        if reporter_is_resident:
            self._events.publish(
                PointsAwardedToReporterEvent(
                    occurred_at=now,
                    incident_id=incident.id,
                    reporter_id=reporter_id.value,
                    points=10,
                )
            )

        return incident

    def provide_solution(self, incident_id: str, solution: str) -> None:
        """Mark an incident as resolved, persist it, and emit resolution events."""
        incident = self._repo.get_by_id(IncidentId(incident_id))
        if incident is None:
            return

        now = datetime.utcnow()
        incident.status = "RESOLVED"
        incident.resolved_at = now
        incident.solution = solution
        self._repo.add(incident)

        self._events.publish(
            SolutionProvidedEvent(
                occurred_at=now,
                incident_id=incident.id,
                solution_description=solution,
            )
        )
        self._events.publish(
            IssuesStatusUpdateReportEvent(
                occurred_at=now,
                incident_id=incident.id,
                new_status=incident.status,
            )
        )
