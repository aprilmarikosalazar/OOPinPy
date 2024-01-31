"""This is my submission for Assignment One."""


def main():
    """Prompt user to enter name, then greet user and state activity."""
    name = input("Please enter your name: ")
    first_string = "Hi "
    second_string = ", let's explore some historical temperatures."
    complete_string = first_string + name + second_string
    print(complete_string)


if __name__ == "__main__":
    main()
