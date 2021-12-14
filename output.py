import os
from typing import Union
class Output:

    def __init__(self) -> None:
        self.clear_console()

    @staticmethod
    def clear_console():
        os.system('cls' if os.name in ('nt', 'dos') else 'clear')

    @staticmethod
    def print(str: str=""):
        print(str)

    def print_red(self, str: str=''):
        self.print(f"\033[91m{str}\033[00m")

    @staticmethod
    def print_numbered_list(elements: list, start: int=1):
        '''prints a list of elements in each line'''
        for counter, element in enumerate(elements, start=start):
            print(f"{counter}) {element}")

    def print_and_selection_input(self, title: str, elements:list) -> str:
        self.print(title)
        self.print_numbered_list(elements)
        return input()

    def print_and_single_selection(self, title: str, elements:list) -> int:
        while True:
            user_input = self.print_and_selection_input(title, elements)

            try:
                user_input = int(user_input)
                if 0 < user_input <= len(elements):
                    return user_input
                raise ValueError

            except ValueError:
                self.clear_console()
                self.print_red('Input non valido, riprova')

    def print_and_multi_selection(self, title: str, elements:list) -> list:
        while True:
            user_input = self.print_and_selection_input(title, elements)

            try:
                inputs = [int(element.strip()) for element in user_input.split(',')]
                if all(x<=len(elements) and x>0 for x in inputs):
                    return inputs
                raise ValueError

            except ValueError:
                self.clear_console()
                self.print_red('Input non valido, riprova')
    
