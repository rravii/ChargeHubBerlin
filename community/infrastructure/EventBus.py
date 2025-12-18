from __future__ import annotations
from collections import defaultdict
from typing import Callable, Type, Dict, List

from community.domain.events.DomainEvent import DomainEvent

EventHandler = Callable[[DomainEvent], None]


class InMemoryEventBus:
    def __init__(self) -> None:
        self._handlers: Dict[Type[DomainEvent], List[EventHandler]] = defaultdict(list)
        self.published: list[DomainEvent] = []

    def subscribe(self, event_type: Type[DomainEvent], handler: EventHandler) -> None:
        self._handlers[event_type].append(handler)

    def publish(self, event: DomainEvent) -> None:
        self.published.append(event)
        for handler in self._handlers[type(event)]:
            handler(event)
