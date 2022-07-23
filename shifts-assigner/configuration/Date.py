from dataclasses import dataclass


@dataclass
class Date:
    day: int
    month: int
    year: int


def create_date(date: str):
    """
    Example - create_date("20.8.2022")
    """
    day, month, year = date.split(".")
    return Date(int(day), int(month), int(year))
