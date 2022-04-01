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
        out.print("Metti i file excel nella cartella input, grazie fra", Output.Color.RED)
        sys.exit(1)

    file_index = out.print_and_select('Seleziona il file', excel_files)
    out.clear()

    excel_file_path = excel_files[file_index]
    excel_file = pd.ExcelFile(excel_file_path)

    sheets_indexes = out.print_and_select(
        'Inserisci i benchmark da graficare, separati da virgola [ENTER per selezionarli tutti]',
        excel_file.sheet_names,
        multi=True
    )
    out.clear()

    excel_data = pd.read_excel(excel_file_path, sheet_name=sheets_indexes)

    output_dir = Path(OUTPUT_DIR).joinpath(os.path.splitext(excel_file_path)[0].split('/')[1])
    plt = Plot(output_dir)
    colors = [Plot.Color.GRAY_100.value, Plot.Color.ORANGE.value]

    for sheet in tqdm(excel_data):
        plt.plot_graph(excel_data[sheet], False, colors, excel_file.sheet_names[sheet], True)

    out.print(f'\nImmagini salvate in "{output_dir}".', Output.Color.GREEN)


if __name__ == '__main__':
    main()
