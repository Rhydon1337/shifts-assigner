import argparse

from configuration import configuration_parser


def main():
    parser = argparse.ArgumentParser(description="Assign shifts to every employee in the configuration")
    parser.add_argument("configuration", type=str, help="path to the shift assigner configuration")
    parser.add_argument("results_dir", type=str, help="path to the results dir")
    args = parser.parse_args()

    print("Parsing the configuration")
    configuration = configuration_parser.parse(args.configuration)
    print("Start assigning the shifts")


if __name__ == "__main__":
    main()
