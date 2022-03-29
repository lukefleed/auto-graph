from typing import Iterable
import matplotlib.pyplot as plt
import pathlib
import pandas as pd

from plotting.tiltes import PlotTitles


class Plot:
    def __init__(
        self, colors: Iterable, output_folder: str = 'images', style: str = 'ggplot'
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
        plot_data: PlotTitles,
        width: int = 3840,
        height: int = 2160,
        dpi: int = 100,
        detailed_numbers: bool = True,
        bar_label_fontsize : int = 55,
        yticks_fontsize: int = 45,
        xticks_fontsize: int = 45
    ):
        ax = df.plot.barh(color=self.__colors)

        if detailed_numbers:
            for container in ax.containers:
                ax.bar_label(container, fontsize=bar_label_fontsize, color = self.__colors[1])

        # aggiungo la legenda solo se c'è più di un valore
        ax.legend(loc='best', fontsize=bar_label_fontsize) if len(df.columns) > 1 else ax.get_legend().remove()


        plt.xticks(fontsize=xticks_fontsize)
        plt.yticks(fontsize=yticks_fontsize)
        plt.style.use(self.__style)
        plt.gcf().set_size_inches(width / dpi, height / dpi)
        plt.suptitle(plot_data.suptitle.title, fontsize=plot_data.suptitle.font_size)
        plt.title(plot_data.title.title, fontdict={'fontsize': plot_data.title.font_size})
        plt.xlabel(plot_data.xlabel.label, fontdict={'fontsize': plot_data.xlabel.font_size})
        plt.ylabel(plot_data.ylabel.label, fontdict={'fontsize': plot_data.ylabel.font_size})

        plt.savefig(self.__output_folder / plot_data.title.title, dpi=dpi)
