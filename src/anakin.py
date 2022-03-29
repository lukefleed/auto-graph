'''main program'''
import pandas as pd
from output import Output
from tqdm import tqdm
from plotting.plotting import Plot
from plotting.tiltes import PlotTitles, Suptitle, Title, Xlabel, Ylabel
import pathlib
import sys

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
    titoli = pd.read_excel(excel_file, sheet_name=0)

    for bench in tqdm(excel_data):
        df = excel_data[bench]

        benchs = pd.DataFrame(
            {
                tipologia: list(df[tipologia].sort_values().values)
                for tipologia in df[df.columns[1:]]
            },
            index=df[df.columns[0]].values,
        )

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


if __name__ == '__main__':
    main()
