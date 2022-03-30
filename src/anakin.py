'''main program'''
import pathlib
import sys
import pandas as pd
from tqdm import tqdm

from plotting.graph_generator import Plot
from utils.output import Output


INPUT_DIR = 'input'
OUTPUT_DIR = 'output'


def main():
    '''main function'''

    out = Output()

    # Create the input folder if it does not exist
    pathlib.Path(INPUT_DIR).mkdir(parents=True, exist_ok=True)
    excel_files = [excel_file for excel_file in pathlib.Path(INPUT_DIR).glob('**/*') if excel_file.is_file()]

    if not excel_files:
        out.print("Metti i file excel nella cartella input, grazie fra", Output.Color.RED)
        sys.exit(1)

    file_index = out.print_and_select('Seleziona il file', excel_files)
    excel_file_path = excel_files[file_index]
    excel_file = pd.ExcelFile(excel_file_path)

    out.clear()

    sheets_indexes = out.print_and_select(
        'Inserisci i benchmark da graficare, separati da virgola [ENTER per selezionarli tutti]',
        excel_file.sheet_names,
        multi=True
    )
    excel_data = pd.read_excel(excel_file_path, sheet_name=sheets_indexes)

    plt = Plot(OUTPUT_DIR)
    colors = [Plot.Color.ORANGE.value, Plot.Color.DARK_GRAY.value]
    for sheet in excel_data:
        plt.plot_graph(excel_data[sheet], True, colors, title=excel_file.sheet_names[sheet])


if __name__ == '__main__':
    main()
