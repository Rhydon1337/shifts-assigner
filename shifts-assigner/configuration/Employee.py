from dataclasses import dataclass
from datetime import datetime


@dataclass
class Employee:
    name: str
    number_of_shifts: int
    unavailable_dates: [datetime]
