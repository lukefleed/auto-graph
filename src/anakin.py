'''main program'''
import pandas as pd
from output import Output
from tqdm import tqdm
from plotting.plotting import Plot
from plotting.graph_generator import Plot
from plotting.tiltes import PlotTitles, Suptitle, Title, Xlabel, Ylabel
import pathlib
import sys
import plotly.express as px
from plotly.subplots import make_subplots
from plotly import graph_objects as go

ARANCIONE = '#F39200'
GRIGIO_SCURO = '#303030'


def main():
    '''main function'''
    out = Output()
    # creo la cartella input se non è presente
    pathlib.Path('input').mkdir(parents=True, exist_ok=True)
    tests = [test for test in pathlib.Path('input').glob('**/*') if test.is_file()]

    if not tests:
        out.print_red("Metti i file excel nella cartella input, grazie fra")
        sys.exit(1)

    test_input = out.print_and_single_selection('Quali test vuoi guardare?', tests)
    excel_file = tests[test_input - 1]
    xl_dataframe = pd.ExcelFile(excel_file)

    categorie = out.print_and_multi_selection(
        'Digita i benchmark che vuoi graficare, separati da virgola [ENTER per selezionarli tutti]',
        xl_dataframe.sheet_names[1:],
    )

    excel_data = pd.read_excel(excel_file, sheet_name=categorie)

    colors = [ARANCIONE, GRIGIO_SCURO]
    for bench in excel_data:
        df = excel_data[bench]
        plt = Plot()
        plt.plot_graph(df, True, colors)


    

if __name__ == '__main__':
    main()


