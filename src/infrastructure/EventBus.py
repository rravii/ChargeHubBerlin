from __future__ import annotations
from collections import defaultdict
from typing import Callable, Type, Dict, List

from src.common.domain.DomainEvent import DomainEvent

EventHandler = Callable[[DomainEvent], None]


class InMemoryEventBus:
    """Minimal pub/sub bus that records published events for inspection in tests."""

    def __init__(self) -> None:
        self._handlers: Dict[Type[DomainEvent], List[EventHandler]] = defaultdict(list)
        self.published: list[DomainEvent] = []

    def subscribe(self, event_type: Type[DomainEvent], handler: EventHandler) -> None:
        """Register a handler for a specific DomainEvent subclass."""
        self._handlers[event_type].append(handler)

    def publish(self, event: DomainEvent) -> None:
        """Record an event and invoke subscribed handlers synchronously."""
        self.published.append(event)
        for handler in self._handlers[type(event)]:
            handler(event)
