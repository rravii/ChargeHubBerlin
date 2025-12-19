from dataclasses import dataclass


@dataclass(frozen=True)
class IncidentId:
    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise ValueError("IncidentId must not be empty")
