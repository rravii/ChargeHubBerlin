from dataclasses import dataclass


@dataclass(frozen=True)
class StarRating:
    value: int

    def __post_init__(self) -> None:
        if not isinstance(self.value, int):
            raise ValueError("StarRating must be int")
        if not (1 <= self.value <= 5):
            raise ValueError("StarRating must be between 1 and 5")
