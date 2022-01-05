"""main program"""
import matplotlib.pyplot as plt
import pandas as pd
from output import Output
from tqdm import tqdm
import pathlib

ARANCIONE = "#F39200"
GRIGIO_SCURO = "#303030"


def main():
    """main function"""
    out = Output()
    tests = ["CPU", "GPU", "GIOCHI"]
    test_input = out.print_and_single_selection("Quali test vuoi guardare?", tests)

    excel_file = "bench/cpu.xlsx" if test_input == 1 else "bench/gpu.xlsx"
    xl_dataframe = pd.ExcelFile(excel_file)

    categorie = out.print_and_multi_selection(
        "Digita i benchmark che vuoi graficare, separati da virgola [ENTER per selezionarli tutti]",
        xl_dataframe.sheet_names[1:],
    )

    plt.style.use("ggplot")

    excel_data = pd.read_excel(excel_file, sheet_name=categorie)

    for bench in tqdm(excel_data):
        df = excel_data[bench]
        bench_name = xl_dataframe.sheet_names[bench]

        benchs = {
            tipologia: list(df[tipologia].values) for tipologia in df[df.columns[1:]]
        }
        df = pd.DataFrame(benchs, index=df[df.columns[0]].values)
        print(df)
        ax = df.plot.barh(color=[ARANCIONE, GRIGIO_SCURO])

        for container in ax.containers:
            ax.bar_label(container)
            
        pathlib.Path("foto").mkdir(parents=True, exist_ok=True)
        plt.savefig(pathlib.Path("foto") / bench_name)

    # for categoria in tqdm(categorie):
    #     print(categoria)
    #     benchmark = pd.read_excel(excel_file, sheet_name=categoria)

    #     if len(categorie) == 1:
    #         cpus = input(
    #             "\nChoose which products compare\n  "
    #             + "\n  ".join(f"[{i}] {n}" for i, n in enumerate(benchmark["CPU"]))
    #             + "\n  [press enter] All products"
    #             + "\nWrite the numbers divided by spaces: "
    #         ).split()
    #         cpus = [int(x) for x in cpus]
    #     else:
    #         cpus = False
    #     if not cpus:
    #         cpus = list(range(len(benchmark)))

    #     # data = {'multicore': benchmark['Multi Core'][cpus].to_list(),
    #     #         'singlecore': benchmark['Single Core'][cpus].to_list()
    #     #        }
    #     data = {col: benchmark[col][cpus].to_list() for col in benchmark.columns[1:]}

    #     plt.rc("font", size=24)
    #     dataframe = pd.DataFrame(data, index=benchmark["CPU"][cpus].to_list())

    #     # plt.figure()  # Ci pensa barh
    # dataframe.plot.barh(color=["#F39200", "#303030"])

    #     titoli = pd.read_excel(excel_file, sheet_name=0)
    #     plt.gcf().set_size_inches(38.4, 19.2)

    #     plt.suptitle(titoli["Titolo"][int(categoria) - 1])
    #     plt.title(titoli["Sottotitolo"][int(categoria) - 1])
    #     plt.ylabel(titoli["Y"][int(categoria) - 1])
    #     plt.xlabel(titoli["X"][int(categoria) - 1])

    #     plt.savefig(f"foto/{titoli['Scheda'][int(categoria)-1]}.png", dpi=100)


if __name__ == "__main__":
    main()
