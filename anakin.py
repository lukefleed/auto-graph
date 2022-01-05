'''main program'''
import matplotlib.pyplot as plt
import pandas as pd
from output import Output
from tqdm import tqdm
import pathlib

ARANCIONE = '#F39200'
GRIGIO_SCURO = '#303030'


def main():
    '''main function'''
    out = Output()
    tests = ['CPU', 'GPU', 'GIOCHI']
    test_input = out.print_and_single_selection('Quali test vuoi guardare?', tests)

    excel_file = 'bench/cpu.xlsx' if test_input == 1 else 'bench/gpu.xlsx'
    xl_dataframe = pd.ExcelFile(excel_file)

    categorie = out.print_and_multi_selection(
        'Digita i benchmark che vuoi graficare, separati da virgola [ENTER per selezionarli tutti]',
        xl_dataframe.sheet_names[1:],
    )

    pathlib.Path('foto').mkdir(parents=True, exist_ok=True)

    excel_data = pd.read_excel(excel_file, sheet_name=categorie)
    titoli = pd.read_excel(excel_file, sheet_name=0)

    for bench in tqdm(excel_data):
        df = excel_data[bench]
        bench_name = xl_dataframe.sheet_names[bench]

        benchs = {
            tipologia: list(df[tipologia].sort_values().values) for tipologia in df[df.columns[1:]]
        }
        df = pd.DataFrame(benchs, index=df[df.columns[0]].values)

        # plotting
        ax = df.plot.barh(color=[ARANCIONE, GRIGIO_SCURO])

        # numeri davanti alle barre
        for container in ax.containers:
            ax.bar_label(container)


        plt.style.use('ggplot')
        plt.gcf().set_size_inches(38.4, 19.2)

        plt.suptitle(titoli["Titolo"][bench - 1])
        plt.title(titoli["Sottotitolo"][bench - 1])
        plt.xlabel(titoli["X"][bench - 1])
        plt.ylabel(titoli["Y"][bench - 1])

        plt.savefig(pathlib.Path('foto') / bench_name, dpi=100)


if __name__ == '__main__':
    main()
