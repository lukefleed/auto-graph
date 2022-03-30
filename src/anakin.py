'''main program'''
from enum import Enum
import pathlib
import sys
import pandas as pd
from tqdm import tqdm

from plotting.graph_generator import Plot
from utils.output import Output


INPUT_DIR = 'input'
OUTPUT_DIR = 'output'


class ChartColor(Enum):
    CYAN = '#82B1FF'
    GRAY = '#303030'
    ORANGE = '#FFAB40'


def main():
    '''main function'''

    out = Output()

    # Create the input folder if it does not exist
    pathlib.Path(INPUT_DIR).mkdir(parents=True, exist_ok=True)
    tests = [test for test in pathlib.Path(INPUT_DIR).glob('**/*') if test.is_file()]

    if not tests:
        out.print("Metti i file excel nella cartella input, grazie fra", Output.Color.RED)
        sys.exit(1)

    test_input = out.print_and_select('Seleziona il file', tests)
    excel_file = tests[test_input - 1]
    xl_dataframe = pd.ExcelFile(excel_file)

    out.clear()

    categorie = out.print_and_select(
        'Inserisci i benchmark da graficare, separati da virgola [ENTER per selezionarli tutti]',
        xl_dataframe.sheet_names[1:],
        multi=True
    )

    excel_data = pd.read_excel(excel_file, sheet_name=categorie)

    colors = [ChartColor.ORANGE.value, ChartColor.GRAY.value]
    for bench in excel_data:
        df = excel_data[bench]
        plt = Plot()
        plt.plot_graph(df, True, colors)


if __name__ == '__main__':
    main()
