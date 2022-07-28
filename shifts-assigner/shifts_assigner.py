import copy
from dataclasses import dataclass
from datetime import datetime, timedelta
from itertools import combinations

from configuration.configuration_parser import Configuration
from configuration.Employee import Employee

WEEK_DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


@dataclass
class WorkDay:
    date: datetime
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


def get_available_employees_for_shift(work_day: WorkDay, all_employees: [Employee]):
    available_employees = []

    for employee in all_employees:
        if employee.number_of_shifts > 0 and (work_day.date not in employee.unavailable_dates):
            available_employees.append(employee)

    return available_employees


def assign(configuration: Configuration) -> [WorkDay]:
    work_calendar = create_work_day_calendar(configuration.start_shift_date,
                                             configuration.end_shift_date,
                                             configuration.free_days,
                                             configuration.number_of_shifts_per_day)

    def assign_shifts(work_day_calendar: [WorkDay], day_index: int, all_employees: [Employee]):
        if day_index == (len(work_day_calendar)):
            return work_day_calendar

        assigned_work_calendar_copy = copy.deepcopy(work_day_calendar)
        all_employees_copy = copy.deepcopy(all_employees)

        work_day = assigned_work_calendar_copy[day_index]
        available_employees = get_available_employees_for_shift(work_day, all_employees_copy)

        if work_day.number_of_shifts > len(available_employees):
            return None

        possible_employees_shifts_positions_from_all_available_employees = list(
            combinations(available_employees, work_day.number_of_shifts))

        for possible_employees_shifts_position in possible_employees_shifts_positions_from_all_available_employees:
            for available_employee in possible_employees_shifts_position:
                available_employee.number_of_shifts -= 1
                work_day.employees.append(available_employee)

            result = assign_shifts(assigned_work_calendar_copy, day_index + 1, all_employees_copy)
            if result is not None:
                return result

            # Restore
            for available_employee in possible_employees_shifts_position:
                available_employee.number_of_shifts += 1
                work_day.employees.remove(available_employee)

        return None

    return assign_shifts(work_day_calendar=work_calendar, day_index=0, all_employees=configuration.employees)
