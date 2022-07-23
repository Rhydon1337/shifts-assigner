import json
from dataclasses import dataclass
from datetime import datetime

from configuration.Employee import Employee


@dataclass
class Configuration:
    employees: [Employee]
    max_number_of_shifts_per_employee: int
    free_days: [str]
    start_shift_date: datetime
    end_shift_date: datetime
    number_of_shifts_per_day: dict


def validate_configuration(configuration: dict):
    pass


def parse_employees(employees: dict, default_max_number_of_shifts_per_employee: int) -> [Employee]:
    employees_list = []
    for employee in employees:
        max_number_of_shifts = default_max_number_of_shifts_per_employee
        if "max_number_of_shifts" in employee:
            max_number_of_shifts = employee["max_number_of_shifts"]
        unavailable_dates = []
        for unavailable_date in employee["unavailable_dates"]:
            unavailable_dates.append(datetime.strptime(unavailable_date, "%d/%m/%Y"))

        employees_list.append(Employee(employee["name"], max_number_of_shifts, unavailable_dates))
    return employees_list


def parse(configuration_path) -> Configuration:
    with open(configuration_path, "r") as configuration_file:
        configuration_file_json_parsed = json.load(configuration_file)
        validate_configuration(configuration_file_json_parsed)
        default_max_number_of_shifts_per_employee = configuration_file_json_parsed[
            "default_max_number_of_shifts_per_employee"]
        employees = parse_employees(configuration_file_json_parsed["employees"],
                                    default_max_number_of_shifts_per_employee)

        return Configuration(employees=employees,
                             max_number_of_shifts_per_employee=default_max_number_of_shifts_per_employee,
                             free_days=configuration_file_json_parsed["free_days"],
                             start_shift_date=datetime.strptime(configuration_file_json_parsed["start_shift_date"],
                                                                "%d/%m/%Y"),
                             end_shift_date=datetime.strptime(configuration_file_json_parsed["end_shift_date"],
                                                              "%d/%m/%Y"),
                             number_of_shifts_per_day=configuration_file_json_parsed["number_of_shifts_per_day"])
