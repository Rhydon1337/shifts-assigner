from dataclasses import dataclass
from datetime import datetime, timedelta

from configuration.configuration_parser import Configuration
from configuration.Employee import Employee

WEEK_DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


@dataclass
class WorkDay:
    work_day: datetime
    employees: [Employee]
    number_of_shifts: int


def create_work_day(day: datetime, number_of_shifts_per_day: dict) -> WorkDay:
    day_name = WEEK_DAYS[day.weekday()]
    work_day = WorkDay(day, [], number_of_shifts_per_day[day_name])
    return work_day


def create_work_day_calendar(start_shift_date: datetime, end_shift_date: datetime, free_days: [str],
                             number_of_shifts_per_day: dict) -> [WorkDay]:
    delta = end_shift_date - start_shift_date
    work_days = []
    for i in range(delta.days + 1):
        day = start_shift_date + timedelta(days=i)
        if WEEK_DAYS[day.weekday()] in free_days:
            continue
        work_days.append(create_work_day(day, number_of_shifts_per_day))
    return work_days


def assign(configuration: Configuration) -> [WorkDay]:
    work_calendar = create_work_day_calendar(configuration.start_shift_date,
                                             configuration.end_shift_date,
                                             configuration.free_days,
                                             configuration.number_of_shifts_per_day)
    print(work_calendar)
