'''main program'''
import os
import sys
import pandas as pd
from pathlib import Path
from tqdm import tqdm

from plotting.graph_generator import Plot
from utils.output import Output


INPUT_DIR = 'input'
OUTPUT_DIR = 'output'


def main():
    '''main function'''

    out = Output()

    # Create the input folder if it does not exist
    Path(INPUT_DIR).mkdir(parents=True, exist_ok=True)
    excel_files = [excel_file for excel_file in Path(INPUT_DIR).glob('**/*') if excel_file.is_file()]

    if not excel_files:
        out.print('La cartella "input" non contiene file Excel', Output.Color.RED)
        sys.exit(1)

    file_index = out.print_and_select('Seleziona il file', excel_files)
    out.clear()

    excel_file_path = excel_files[file_index]
    excel_file = pd.ExcelFile(excel_file_path)

    sheets_indexes = out.print_and_select(
        'Inserisci i fogli da convertire in grafico, separati da virgola [ENTER per selezionarli tutti]',
        excel_file.sheet_names,
        multi=True
    )
    out.clear()

    excel_data = pd.read_excel(excel_file_path, sheet_name=sheets_indexes, header=None, index_col=None)

    output_dir = Path(OUTPUT_DIR).joinpath(os.path.splitext(excel_file_path)[0].split(os.path.sep)[1])
    plt = Plot(output_dir)

    out.print('Conversione in corso...\n')

    for sheet in tqdm(excel_data):
        plt.plot_graph(excel_data[sheet], excel_file.sheet_names[sheet])

    out.print(f'\nImmagini salvate in "{output_dir}".', Output.Color.GREEN)


if __name__ == '__main__':
    main()
