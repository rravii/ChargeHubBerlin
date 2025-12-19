from dataclasses import dataclass


@dataclass(frozen=True)
class IncidentDetails:
    description: str

    def __post_init__(self) -> None:
        if not self.description or not self.description.strip():
            raise ValueError("Incident description must not be empty")
