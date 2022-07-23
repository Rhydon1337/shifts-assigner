from dataclasses import dataclass

from Date import Date


@dataclass
class Employee:
    name: str
    max_number_of_shifts: int
    unavailable_dates: [Date]
