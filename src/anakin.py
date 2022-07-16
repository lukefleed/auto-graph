'''main program'''
import os
import sys
import pandas as pd
import argparse
from pathlib import Path
from tqdm import tqdm

from plotting.graph_generator import Plot
from utils.output import Output


INPUT_DIR = 'input'
OUTPUT_DIR = 'output'


def main():
    '''main function'''

    parser = argparse.ArgumentParser()
    parser.add_argument("-file", help="Inserisci il nome file da convertire in grafico", required=True)
    parser.add_argument("-sheets", help="Inserisci i fogli da convertire in grafico, separati da virgola, 'all' per convertirli tutti",required=True)
    
    args = parser.parse_args()

    file_name = args.file
    sheets = args.sheets
    out = Output()

    # Create the input folder if it does not exist
    Path(INPUT_DIR).mkdir(parents=True, exist_ok=True)
    
    file_path = Path(os.path.join(INPUT_DIR,file_name))
    print(file_path)
    if(not os.path.exists(file_path)):
        print("Inserire un file valido")
        exit()

    excel_file = pd.ExcelFile(file_path)

    if sheets == "all":
        sheets = list(range(0,len(excel_file.sheet_names)-1))
    else:
        sheets = sheets.split(",")
        sheets = [int(i) for i in sheets]
        for elem in sheets:
            if elem > len(excel_file.sheet_names) or elem < 0:
                print("Inserire indici validi")
                exit()

    excel_data = pd.read_excel(excel_file, sheet_name=sheets, header=None, index_col=None)

    output_dir = Path(OUTPUT_DIR).joinpath(os.path.splitext(file_path)[0].split(os.path.sep)[1])
    plt = Plot(output_dir)

    out.print('Conversione in corso...\n')

    for sheet in tqdm(excel_data):
        print(sheet)
        plt.plot_graph(excel_data[sheet], excel_file.sheet_names[sheet])

    out.print(f'\nImmagini salvate in "{output_dir}".', Output.Color.GREEN)


if __name__ == '__main__':
    main()
