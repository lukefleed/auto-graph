#!/usr/bin/env python3
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# test = input("Quali test vuoi guardare?:\n [1] CPU\n [2] GPU\n [3] Giochi\n Scrivi il numero: ")

EXCEL_FILE = 'bench/cpu.xlsx'

xl = pd.ExcelFile(EXCEL_FILE)

categorie = input(
    "\nChoose one of the following benchmarks\n  "
    + "\n  ".join(
        f"[{i+1}] {n}" for i, n in enumerate(xl.sheet_names[1:]))
    + "\n  [press enter] All benchmarks"
    + "\nWrite the number: ")
if categorie:
    categorie = [int(categorie)]
else:
    categorie = list(range(1, len(xl.sheet_names)))

plt.style.use('ggplot')
for categoria in categorie:
    benchmark = pd.read_excel(EXCEL_FILE, sheet_name=int(categoria))

    if len(categorie) == 1:
        cpus = input(
            "\nChoose which CPUs compare\n  "
            + "\n  ".join(
                f"[{i}] {n}" for i, n in enumerate(benchmark['CPU']))
            + "\n  [press enter] All CPUs"
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
        #columns=['multicore','singlecore'],
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

#plt.show()

