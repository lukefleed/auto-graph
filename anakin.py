#!/usr/bin/env python3
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

test = input("Quali test vuoi guardare?:\n [1] CPU\n [2] GPU\n [3] Giochi\n Scrivi il numero: ")

xl = pd.ExcelFile('bench/cpu.xlsx')

categoria = input("\nScegli uno dei seguenti benchmark\n  "
                  + "\n  ".join(
                      f"[{i}] {n}" for i, n in enumerate(xl.sheet_names))
                  + "\nScrivi il numero: ")

excel_file = 'bench/cpu.xlsx'
benchmark = pd.read_excel(excel_file, sheet_name=int(categoria))

cpus = input(
    "\nScegli quali processori confrontare\n  "
    + "\n  ".join(
        f"[{i}] {n}" for i, n in enumerate(benchmark['CPU']))
    + "\nScrivi i numeri separati da spazi: ").split()
cpus = [int(x) for x in cpus]

# data = {'multicore': benchmark['Multi Core'][cpus].to_list(),
#         'singlecore': benchmark['Single Core'][cpus].to_list()
#        }
data = {col: benchmark[col][cpus].to_list() for col in benchmark.columns[1:]}

df = pd.DataFrame(
    data,
    #columns=['multicore','singlecore'],
    index=benchmark['CPU'][cpus].to_list())

plt.style.use('ggplot')
df.plot.barh(color=["#303030", "#F39200"])


titolo = input("\nTitolo del grafico: ")
plt.title(titolo)

ordinate = input("Titolo asse Y: ")
plt.ylabel(ordinate)

ascisse = input("Titolo asse X: ")
plt.xlabel(ascisse)

plt.show()

