"""This is my submission for Assignment Five."""


class HistoricalTemps:
    """Create class with Historical Temperatures."""

    def __init__(self, zip_code: str, start="1950-08-13", end="2023-08-25"):
        """Use init method with 3 parameters."""
        self._zip_code = zip_code
        self._start = start
        self._end = end

    @property
    def start(self):
        """Run start getter here."""
        return self._start

    @start.setter
    def start(self, new_num):
        """Run start setter here."""
        self._start = new_num

    @property
    def end(self):
        """Run end getter here."""
        return self._end

    @end.setter
    def end(self, new_num):
        """Run end setter here."""
        self._end = new_num

    @property
    def zip_code(self):
        """Run zip_code getter here."""
        return self._zip_code


def create_dataset():
    """Prompt user to enter zip code."""
    zip_code = input("Please enter a zip code: ")
    hist_temp = HistoricalTemps(zip_code)
    return hist_temp


def main():
    """Prompt user to enter name, then greet them and state activity."""
    name = input("Please enter your name: ")
    print(f"Hi {name}, let's explore historical temperatures.\n")
    menu()


def menu():
    """Ask user for selection and provide appropriate output."""
    dataset_one = None
    dataset_two = None

    while True:
        print_menu()
        try:
            number = int(input("What is your choice? "))
        except ValueError:
            print("Please enter a number only")
            continue
        match number:
            case 1:
                dataset_one = create_dataset()
            case 2:
                dataset_two = create_dataset()
            case 3:
                print("selection three is not functional yet")
            case 4:
                print("selection four is not functional yet")
            case 5:
                print("selection five is not functional yet")
            case 6:
                print("selection six is not functional yet")
            case 7:
                print("selection seven is not functional yet")
            case 9:
                print("Goodbye!  Thank you for using the database")
                break
            case _:
                print("That's not a valid selection")


def print_menu():
    """Display Main Menu for user to select from."""
    print("Main Menu")
    print("1 - Load dataset one")
    print("2 - Load dataset two")
    print("3 - Compare average temperatures")
    print("4 - Dates above threshold temperature")
    print("5 - Highest historical dates")
    print("6 - Change start and end dates for dataset one")
    print("7 - Change start and end dates for dataset two")
    print("9 - Quit")


if __name__ == "__main__":
    main()
