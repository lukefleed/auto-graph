'''main program'''
import pandas as pd
from output import Output
from tqdm import tqdm
from plotting import Plot

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
            titoli["Titolo"][bench - 1],
            titoli["Sottotitolo"][bench - 1],
            titoli["X"][bench - 1],
            titoli["Y"][bench - 1]
        )


if __name__ == '__main__':
    main()
