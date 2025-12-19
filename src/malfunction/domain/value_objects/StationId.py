from dataclasses import dataclass


@dataclass(frozen=True)
class StationId:
    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise ValueError("StationId must not be empty")
