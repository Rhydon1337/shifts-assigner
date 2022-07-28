import argparse

import shifts_assigner
from configuration import configuration_parser


def main():
    parser = argparse.ArgumentParser(description="Assign shifts to every employee in the configuration")
    parser.add_argument("configuration", type=str, help="path to the shift assigner configuration")
    parser.add_argument("results_dir", type=str, help="path to the results dir")
    args = parser.parse_args()

    print("Parsing the configuration")
    configuration = configuration_parser.parse(args.configuration)
    print("Start assigning the shifts")
    work_calendar = shifts_assigner.assign(configuration)
    for work_day in work_calendar:
        print(f"Date: {work_day.date}")
        for employee in work_day.employees:
            print(f"Employee name: {employee.name}")
        print(f"Number of shifts: {work_day.number_of_shifts}")


if __name__ == "__main__":
    main()
