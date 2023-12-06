"""This is my submission for Assignment Four."""


def main():
    """Prompt user to enter name, then greet them and state activity."""
    name = input("Please enter your name: ")
    print(f"Hi {name}, let's explore historical temperatures.\n")
    menu()


def menu():
    """Ask user for selection and provide appropriate output."""
    while True:
        print_menu()
        try:
            number = int(input("What is your choice? "))
        except ValueError:
            print("Please enter a number only")
            continue
        match number:
            case 1:
                print("selection one is not functional yet")
            case 2:
                print("selection two is not functional yet")
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
