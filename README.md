# shifts-assigner
Assign shifts to employees while considering:
1. Work week free days
2. Number of shifts per day
3. Max number of shifts per employee
4. Unavailable dates for every employee
5. Split the shifts equally between the employees

The assignment is backtrack algorithm.

JSON Configuration example:
```
{
  "employees": [
    {
      "name": "Bill",
      "max_number_of_shifts": 1,
      "unavailable_dates": [
        "28/8/2022",
        "12/8/2022"
      ]
    },
    {
      "name": "Yohai",
      "unavailable_dates": [
        "28/08/2022"
      ]
    },
    {
      "name": "John",
      "unavailable_dates": [
      ]
    },
    {
      "name": "David",
      "max_number_of_shifts": 1,
      "unavailable_dates": [
      ]
    },
    {
      "name": "Adir",
      "unavailable_dates": [
      ]
    },
    {
      "name": "Greg",
      "unavailable_dates": [
      ]
    }
  ],
  "default_max_number_of_shifts_per_employee": 20,
  "free_days": [
    "Friday",
    "Saturday"
  ],
  "start_shift_date": "28/8/2022",
  "end_shift_date": "31/8/2022",
  "number_of_shifts_per_day": {
    "Sunday": 3,
    "Monday": 1,
    "Tuesday": 1,
    "Wednesday": 1,
    "Thursday": 1
  }
}
```

DONE!!!
