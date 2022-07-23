import json
from dataclasses import dataclass

from configuration.Employee import Employee
from configuration.Date import create_date


@dataclass
class Configuration:
    employers: [Employee]
    max_number_of_shifts_per_employee: int
    free_days: [str]


def validate_configuration(configuration: dict):
    pass


def parse_employers(employers: dict, default_max_number_of_shifts_per_employee: int) -> [Employee]:
    employers_list = []
    for employee in employers:
        max_number_of_shifts = default_max_number_of_shifts_per_employee
        if "max_number_of_shifts" in employee:
            max_number_of_shifts = employee["max_number_of_shifts"]
        unavailable_dates = []
        for unavailable_date in employee["unavailable_dates"]:
            unavailable_dates.append(create_date(unavailable_date))

        employers_list.append(Employee(employee["name"], max_number_of_shifts, unavailable_dates))
    return employers_list


def parse(configuration_path):
    with open(configuration_path, "r") as configuration_file:
        configuration_file_json_parsed = json.load(configuration_file)
        validate_configuration(configuration_file_json_parsed)
        default_max_number_of_shifts_per_employee = configuration_file_json_parsed[
            "default_max_number_of_shifts_per_employee"]
        employers = parse_employers(configuration_file_json_parsed["employers"],
                                    default_max_number_of_shifts_per_employee)
        return Configuration(employers,
                             default_max_number_of_shifts_per_employee,
                             configuration_file_json_parsed["free_days"])
