import os
from enum import Enum


class Output:
    def __init__(self) -> None:
        self.clear()

    class Color(Enum):
        RED = '\033[91m<STR>\033[00m'
        CYAN = '\033[96m<STR>\033[00m'

    def clear(self):
        '''clears the console'''
        os.system('cls' if os.name in ('nt', 'dos') else 'clear')

    def print(self, str: str = '', color: Color = None):
        '''prints the passed string'''
        print(str if color == None else color.value.replace('<STR>', str))

    def print_numbered_list(self, elements: list):
        '''prints a list of elements by line'''
        for counter, element in enumerate(elements, start=1):
            print(f'  {counter}. {element}')

    def print_and_read_input(self, title: str, elements: list) -> str:
        '''prints a title, a numbered list and waits for user input'''
        self.print(title, self.Color.CYAN)
        self.print_numbered_list(elements)
        return input()

    def print_and_select(self, title: str, elements: list, multi=False) -> list:
        while True:
            user_input = self.print_and_read_input(title, elements)

            try:
                if multi == False:
                    user_input = int(user_input) - 1
                    if 0 <= user_input < len(elements):
                        return user_input
                    raise ValueError
                else:
                    if user_input == '':
                        return [counter for counter, _ in enumerate(elements)]
                    inputs = [int(element.strip()) - 1 for element in user_input.split(',')]
                    if all(x >= 0 and x < len(elements) for x in inputs):
                        return inputs
                    raise ValueError

            except ValueError:
                self.clear()
                self.print('Input non valido, riprova', self.Color.RED)
