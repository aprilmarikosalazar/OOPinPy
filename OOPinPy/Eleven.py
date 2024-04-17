"""This is the main script for the 'Air Quality Analyses' tool."""


import pgeocode
import math
import requests
import json


request_url = "https://archive-api.open-meteo.com/v1/archive"


class HistoricalTemps:
    """Create class with Historical Temperatures."""

    def __init__(self, zip_code: str, start="1950-08-13", end="2023-08-25"):
        """Use 3 parameters in init method, return tuple, and validate lat."""
        self._zip_code = zip_code
        self._start = start
        self._end = end
        self._lat, self._lon, self._loc_name = (
            HistoricalTemps.zip_to_loc_info(zip_code))
        self._temp_list = None
        self._load_temps()

    @staticmethod
    def _convert_json_to_list(data):
        """Convert open-meteo json string to dict, then print dates/temps."""
        data_dict = json.loads(data)
        return list(zip(data_dict["daily"]["time"],
                        data_dict["daily"]["temperature_2m_max"]))

    @staticmethod
    def zip_to_loc_info(zip_code):
        """Use static method by passing zip to return location details."""
        geocoder = pgeocode.Nominatim('us')
        result = geocoder.query_postal_code(zip_code)
        lat = result['latitude']
        lon = result['longitude']
        loc_name = result['place_name']
        if math.isnan(lat):
            raise LookupError
        return lat, lon, loc_name

    @property
    def start(self):
        """Run start getter here."""
        return self._start

    @start.setter
    def start(self, new_start):
        """Run start setter here."""
        initial_start = self._start
        self._start = new_start
        try:
            self._load_temps()
        except LookupError:
            self._start = initial_start
            raise LookupError

    @property
    def end(self):
        """Run end getter here."""
        return self._end

    @end.setter
    def end(self, new_end):
        """Run end setter here."""
        initial_end = self._end
        self._end = new_end
        try:
            self._load_temps()
        except LookupError:
            self._end = initial_end
            raise LookupError

    @property
    def zip_code(self):
        """Run zip_code getter here."""
        return self._zip_code

    @property
    def loc_name(self):
        """Run loc_name getter here."""
        return self._loc_name

    def _load_temps(self):
        """Call open-meteo API // maintain hardcoded historical temp data."""
        parameters = {"latitude": self._lat,
                      "longitude": self._lon,
                      "start_date": self._start,
                      "end_date": self._end,
                      "daily": "temperature_2m_max",
                      "timezone": "America/Los_Angeles"
                      }
        data = requests.get(request_url, params=parameters)
        self._temp_list = self._convert_json_to_list(data.text)

    def average_temp(self):
        """Compute average temp, then print."""
        return sum(item[1] for item in self._temp_list) / len(self._temp_list)

    def extreme_days(self, threshold: float):
        """Extract date/temp tuples using list comprehension."""
        return [item for item in self._temp_list if item[1] > threshold]

    def top_x_days(self, num_days=10):
        """Return tuples list of set days with the highest temperatures."""
        return sorted(self._temp_list, reverse=True,
                      key=lambda item: item[1])[:num_days]


def create_dataset():
    """Prompt user for zip and use builtin LookupError to validate it."""
    zip_code = input("Please enter a zip code: ")
    try:
        hist_temp = HistoricalTemps(zip_code)
    except LookupError:
        hist_temp = None
        print("Data could not be loaded. Please check that the zip code is "
              "correct and that you have a working internet connection")
    return hist_temp


def compare_average_temps(dataset_one: HistoricalTemps,
                          dataset_two: HistoricalTemps):
    """Once loaded, compare average temps of both datasets."""
    if dataset_one is None or dataset_two is None:
        print("Please load two datasets first")
    else:
        print(f"The average maximum temperature for {dataset_one.loc_name} "
              f"was{dataset_one.average_temp(): .2f} degrees Celsius")
        print(f"The average maximum temperature for {dataset_two.loc_name} "
              f"was{dataset_two.average_temp(): .2f} degrees Celsius")


def print_extreme_days(dataset: HistoricalTemps):
    """Check if dataset is loaded, then prompt user for threshold temp."""
    if dataset is None:
        print("Please load this dataset first")
        return
    try:
        threshold = float(input("List days above what temperature? "))
    except ValueError:
        print("Please enter a valid temperature")
        return
    extdays_lc = dataset.extreme_days(threshold)
    print(f"There are {len(extdays_lc)} days above {threshold} degrees in "
          f"{dataset.loc_name}")
    for item in extdays_lc:
        print(f"{item[0]}: {item[1]}")


def print_top_five_days(dataset: HistoricalTemps):
    """Check if dataset is loaded, then show top 5 hottest days from data."""
    if dataset is None:
        print("Please load this dataset first")
        return
    top_five = dataset.top_x_days(num_days=5)
    print(f"Following are the hottest five days in {dataset.loc_name} on "
          f"record from {dataset.start} to {dataset.end}")
    for item in top_five:
        print(f"Date {item[0]}: {item[1]}")


def change_dates(dataset: HistoricalTemps):
    """Ask user to set and modify dataset start/end dates."""
    if dataset is None:
        print("Please load this dataset first")
        return
    try:
        dataset.start = input("Please enter a new start date (YYYY-MM-DD): ")
    except LookupError:
        print(f"Start date could not be changed.  Please check that the "
              f"start date is in the correct format and is before the "
              f"current end date of {dataset.end}")
        return
    try:
        dataset.end = input("Please enter a new end date (YYYY-MM-DD): ")
    except LookupError:
        print(f"End date could not be changed.  Please check that the "
              f"end date is in the correct format and is after the "
              f"current start date of {dataset.start}")


def main():
    """Prompt user for name, then greet them and state activity."""
    name = input("Please enter your name: ")
    print(f"Hi {name}, let's explore historical temperatures.\n")
    menu()


def menu():
    """Ask user to select item to get output. Pass in dataset arguments."""
    dataset_one = None
    dataset_two = None
    while True:
        print_menu(dataset_one, dataset_two)
        try:
            number = int(input("What is your choice? "))
        except ValueError:
            print("Please enter a number only")
            continue
        match number:
            case 1:
                dataset_one = create_dataset()
                continue
            case 2:
                dataset_two = create_dataset()
                continue
            case 3:
                compare_average_temps(dataset_one, dataset_two)
            case 4:
                print_extreme_days(dataset_one)
            case 5:
                print_top_five_days(dataset_one)
            case 6:
                change_dates(dataset_one)
            case 7:
                change_dates(dataset_two)
            case 9:
                print("Goodbye!  Thank you for using the database")
                break
            case _:
                print("That's not a valid selection")


def print_menu(dataset_one: HistoricalTemps, dataset_two: HistoricalTemps):
    """Display Main Menu for user selection, and include two parameters."""
    print("Main Menu")
    if dataset_one is None:
        print("1 - Load dataset one")
    else:
        print(f"1 - Replace {dataset_one.loc_name}")
    if dataset_two is None:
        print("2 - Load dataset two")
    else:
        print(f"2 - Replace {dataset_two.loc_name}")
    print("3 - Compare average temperatures")
    print("4 - Dates above threshold temperature")
    print("5 - Highest historical dates")
    print("6 - Change start and end dates for dataset one")
    print("7 - Change start and end dates for dataset two")
    print("9 - Quit")


if __name__ == "__main__":
    main()
