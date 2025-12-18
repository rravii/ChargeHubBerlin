from dataclasses import dataclass


@dataclass(frozen=True)
class UserId:
    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise ValueError("UserId must not be empty")
