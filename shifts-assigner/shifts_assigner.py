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
    """
    Create a work day from date and number of shifts that there are in the day
    :param day: the date of the work day
    :param number_of_shifts_per_day: the number of shifts that there are in this specific work day
    :return: WorkDay object
    """
    day_name = WEEK_DAYS[day.weekday()]
    work_day = WorkDay(day, [], number_of_shifts_per_day[day_name])
    return work_day


def create_work_day_calendar(start_shift_date: datetime, end_shift_date: datetime, free_days: [str],
                             number_of_shifts_per_day: dict) -> [WorkDay]:
    """
    Example:
        number_of_shifts_per_day = {"Sunday": 1, "Monday": 1, "Tuesday": 1, "Wednesday": 1, "Thursday": 1}
        create_work_day_calendar("1.8.2022", "31.8.2022", ["Friday", "Saturday"], number_of_shifts_per_day)

    Work day calendar it just a work day list, that list exclude "free days" like friday and saturday.
    :param start_shift_date: the first date in the work day calendar
    :param end_shift_date: the last date in the work day calendar
    :param free_days: days that aren't work day
    :param number_of_shifts_per_day: dict that represents the number of shifts each day
    :return: a work day list
    """
    delta = end_shift_date - start_shift_date
    work_days = []
    for i in range(delta.days + 1):
        day = start_shift_date + timedelta(days=i)
        if WEEK_DAYS[day.weekday()] in free_days:
            continue
        work_days.append(create_work_day(day, number_of_shifts_per_day))
    return work_days


def sort_available_employees_combination(available_employees_combination: [(Employee,)]):
    """

    Sort all the available employees by the number of shifts that they currently have.
    The order is from the maximum to the minimum, because we want to assign to shift to someone that has more
    shifts available.

    :param available_employees_combination: all available shifts combinations
    example:
    [('Adir', 'Dan'), ('Adir', 'Yohai'), ('Adir', 'John'), ('Dan', 'Yohai'), ('Dan', 'John'), ('Yohai', 'John')]

    :return: the sorted list
    """

    def sum_employees_number_of_shifts(employees: (Employee,)):
        overall_number_of_shifts = 0

        for employee in employees:
            overall_number_of_shifts += employee.number_of_shifts

        return overall_number_of_shifts

    return sorted(available_employees_combination, key=lambda employees: sum_employees_number_of_shifts(employees),
                  reverse=True)


def get_available_employees_for_shift(work_day: WorkDay, all_employees: [Employee]):
    """
    Get a workday and all employees and return all employees that are available on that work day
    """
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
        """
        Get the workday calendar, a day in the calendar and all employees
        Using backtrace algorithm we try to assign all available employees to shifts
        """

        # If we reached the last day then return the assigned workday calendar
        if day_index == (len(work_day_calendar)):
            return work_day_calendar

        work_day = work_day_calendar[day_index]

        """
        Get all the available employees from the employee list for this work day, because every employee has unavailable
        days that he can not work on.
        """
        available_employees = get_available_employees_for_shift(work_day, all_employees)

        # If we couldn't find any or enough available employees then return
        if work_day.number_of_shifts > len(available_employees):
            return None

        """
        We need all available employee combination for every shift.
        For Example:
        available_employees = ["Adir", "Dan", "Yohai", "John"]
        Today workday number of shifts is 2.
        It means that we need for today shifts:
        [('Adir', 'Dan'), ('Adir', 'Yohai'), ('Adir', 'John'), ('Dan', 'Yohai'), ('Dan', 'John'), ('Yohai', 'John')]
        And if the number of shifts is 3.
        [('Adir', 'Dan', 'Yohai'), ('Adir', 'Dan', 'John'), ('Adir', 'Yohai', 'John'), ('Dan', 'Yohai', 'John')]
        """
        possible_employees_shifts_positions_from_all_available_employees = list(
            combinations(available_employees, work_day.number_of_shifts))

        # We want that each employee will get equal amount of shifts.
        # Then, we sort the combination by the overall number of shifts
        possible_employees_shifts_positions_from_all_available_employees = \
            sort_available_employees_combination(possible_employees_shifts_positions_from_all_available_employees)

        for possible_employees_shifts_position in possible_employees_shifts_positions_from_all_available_employees:
            # For each combination assign the employees for the workday
            for available_employee in possible_employees_shifts_position:
                available_employee.number_of_shifts -= 1
                work_day.employees.append(available_employee)

            # Call the function with the next workday again after today workday already assigned
            result = assign_shifts(work_day_calendar, day_index + 1, all_employees)

            """
            If you look at the function you will find out that the only way for result not to be None
            it is if we assigned all the employees for every workday and reached the last day. Then, we can finish and
            return the calendar.
            """
            if result is not None:
                return result

            """
            If we reached here, it means that we couldn't found any possible solution for our workday calendar when
            possible_employees_shifts_position is the current. Therefore, we need to restore the current workday and 
            try the next possible_employees_shifts_position
            """
            for available_employee in possible_employees_shifts_position:
                available_employee.number_of_shifts += 1
                work_day.employees.remove(available_employee)

        """
        The function reach here if could find *any* possible_employees_shifts_position for the current workday. Then,
        we need to backtrace by return None and the mention above "result" will get back and hopefully find another 
        possible option.
        """
        return None

    return assign_shifts(work_day_calendar=work_calendar, day_index=0, all_employees=configuration.employees)
