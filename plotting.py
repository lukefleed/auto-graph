from typing import Iterable
import matplotlib.pyplot as plt
import pathlib
import pandas as pd


class Plot:
    def __init__(
        self, colors: Iterable, output_folder: str = 'foto', style: str = 'ggplot'
    ) -> None:
        self.__style = style
        self.__colors = colors
        self.__output_folder = pathlib.Path(output_folder)
        self._create_output_folder()

    def _create_output_folder(self) -> None:
        self.__output_folder.mkdir(parents=True, exist_ok=True)

    def plot_barh(
        self,
        df: pd.DataFrame,
        title: str,
        suptitle: str,
        xlabel: str,
        ylabel: str,
        width: float = 3840,
        height: float = 2160,
        dpi: int = 100,
        detailed_numbers: bool = True,
    ) -> None:

        ax = df.plot.barh(color=self.__colors)

        if detailed_numbers:
            for container in ax.containers:
                ax.bar_label(container)

        plt.style.use(self.__style)
        plt.gcf().set_size_inches(width / dpi, height / dpi)
        plt.suptitle(suptitle)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)

        plt.savefig(self.__output_folder / title, dpi=dpi)
