"""
Settings for limits

Raise in min_delay_sec > max_delay_sec
"""
from pydantic import BaseModel, model_validator


class LimitsSettings(BaseModel):
    """Settings for limits"""
    min_delay_sec: float = 1
    max_delay_sec: float = 2

    @model_validator(mode="after")
    def check_limits(self):
        if self.min_delay_sec >= self.max_delay_sec:
            raise ValueError(
                f"ERROR: min_delay_sec > max_delay_sec "
                f"({self.min_delay_sec} > {self.max_delay_sec})"
            )
        return self

    def __str__(self):
        """Show settings"""
        str_list = [
            "",
            "Limits",
            f" - min_delay_sec: {self.min_delay_sec}",
            f" - max_delay_sec: {self.max_delay_sec}"
        ]
        return "\n".join(str_list)
