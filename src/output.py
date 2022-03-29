import os


class Output:
    def __init__(self) -> None:
        self.clear_console()

    @staticmethod
    def clear_console():
        '''clears the console'''
        os.system('cls' if os.name in ('nt', 'dos') else 'clear')

    @staticmethod
    def print(str: str = ''):
        '''prints the passed string'''
        print(str)

    def print_red(self, str: str = ''):
        '''prints the passed string in red'''
        self.print(f'\033[91m{str}\033[00m')

    def print_cyan(self, str: str = ''):
        '''prints the passed string in cyan'''
        self.print(f'\033[96m{str}\033[00m')

    @staticmethod
    def print_numbered_list(elements: list, start: int = 1):
        '''prints a list of elements by line'''
        for counter, element in enumerate(elements, start=start):
            print(f'{counter}) {element}')

    def print_and_selection_input(
        self, title: str, elements: list, start: int = 1
    ) -> str:
        '''prints a title, a numbered list and waits for user input'''
        self.print_cyan(title)
        self.print_numbered_list(elements, start)
        return input()

    def print_and_single_selection(
        self, title: str, elements: list, start: int = 1
    ) -> int:
        '''prints a title, a numbered list, waits for user input
        and returns the input number'''
        while True:
            user_input = self.print_and_selection_input(title, elements, start)

            try:
                user_input = int(user_input)
                if 0 < user_input <= len(elements):
                    return user_input
                raise ValueError

            except ValueError:
                self.clear_console()
                self.print_red('Input non valido, riprova')

    def print_and_multi_selection(
        self, title: str, elements: list, start: int = 1
    ) -> list:
        '''prints a title, a numbered list, waits for user input
        and returns the input numbers. If the user input is none, everthing will be selected.
        Enter selects all the elements in the list'''
        while True:
            user_input = self.print_and_selection_input(title, elements, start)

            try:
                if user_input == '':
                    return [counter for counter, _ in enumerate(elements, start=start)]
                inputs = [int(element.strip()) for element in user_input.split(',')]
                if all(x <= len(elements) and x > 0 for x in inputs):
                    return inputs
                raise ValueError

            except ValueError:
                self.clear_console()
                self.print_red('Input non valido, riprova')
