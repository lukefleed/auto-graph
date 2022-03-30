'''main program'''
from enum import Enum
import pathlib
import sys
import pandas as pd
import plotly.express as px
from tqdm import tqdm

from plotting.plotting import Plot
from plotting.tiltes import PlotTitles, Suptitle, Title, Xlabel, Ylabel
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
    titoli = pd.read_excel(excel_file, sheet_name=0)

    for bench in tqdm(excel_data):
        df = excel_data[bench]
        print(df)
        benchs = pd.DataFrame(
            {
                tipologia: list(df[tipologia].sort_values().values)
                for tipologia in df[df.columns]
            },
            index=df[df.columns[0]].values,
        )

        '''
        plt = Plot([ARANCIONE, GRIGIO_SCURO])
        plt.plot_barh(
            benchs,
            PlotTitles(
                Title(titoli["Titolo"][bench - 1]),
                Suptitle(titoli["Sottotitolo"][bench - 1]),
                Xlabel(titoli["X"][bench - 1]),
                Ylabel(titoli["Y"][bench - 1]),
            ),
        )
        '''
        #print(benchs)
        fig = px.histogram(benchs, x="Perfrormance", y="CPU", orientation='h', barmode = 'group')
        fig.show()


if __name__ == '__main__':
    main()
