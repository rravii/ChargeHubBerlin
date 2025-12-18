from dataclasses import dataclass


@dataclass(frozen=True)
class ReporterId:
    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise ValueError("ReporterId must not be empty")
