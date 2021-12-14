#!/usr/bin/env python3
import matplotlib.pyplot as plt
import pandas as pd
from output import Output


def main():
    out = Output()
    tests = ['CPU', 'GPU', 'GIOCHI']
    test_input = out.print_and_single_selection('Quali test vuoi guardare?', tests)

    EXCEL_FILE = 'bench/cpu.xlsx' if test_input == 1 else 'bench/gpu.xlsx'
    xl = pd.ExcelFile(EXCEL_FILE)

    categorie = out.print_and_multi_selection('Digita i benchmark che vuoi graficare, separati da virgola', xl.sheet_names[1:])
    print(categorie)


    #TODO refactor
    plt.style.use('ggplot')
    for categoria in categorie:
        benchmark = pd.read_excel(EXCEL_FILE, sheet_name=int(categoria))

        if len(categorie) == 1:
            cpus = input(
                "\nChoose which products compare\n  "
                + "\n  ".join(
                    f"[{i}] {n}" for i, n in enumerate(benchmark['CPU']))
                + "\n  [press enter] All products"
                + "\nWrite the numbers divided by spaces: ").split()
            cpus = [int(x) for x in cpus]
        else:
            cpus = False
        if not cpus:
            cpus = list(range(len(benchmark)))

        # data = {'multicore': benchmark['Multi Core'][cpus].to_list(),
        #         'singlecore': benchmark['Single Core'][cpus].to_list()
        #        }
        data = {col: benchmark[col][cpus].to_list() for col in benchmark.columns[1:]}

        plt.rc("font", size=24)
        df = pd.DataFrame(
            data,
            index=benchmark['CPU'][cpus].to_list())

        #plt.figure()  # Ci pensa barh
        df.plot.barh(color=["#F39200", "#303030"])

        titoli = pd.read_excel(EXCEL_FILE, sheet_name=0)
        plt.gcf().set_size_inches(38.4, 19.2)

        plt.suptitle(titoli["Titolo"][int(categoria)-1])
        plt.title(titoli["Sottotitolo"][int(categoria)-1])
        plt.ylabel(titoli["Y"][int(categoria)-1])
        plt.xlabel(titoli["X"][int(categoria)-1])

        plt.savefig(f"foto/{titoli['Scheda'][int(categoria)-1]}.png", dpi=100)

if __name__ == '__main__':
    main()