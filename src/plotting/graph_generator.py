from typing import Iterable
import pathlib
from plotly.subplots import make_subplots
from plotly import graph_objects as go
import pandas as pd

class Plot:
    def __init__(
        self, output_folder: str = 'output'
    ) -> None:

        self.__output_folder = pathlib.Path(output_folder)
        self._create_output_folder()

    def _create_output_folder(self) -> None:
        self.__output_folder.mkdir(parents=True, exist_ok=True)

    def plot_graph(self, benchs: pd.DataFrame, grouped = True, colors: Iterable = None):
        fig = make_subplots(rows=2, cols=1)
        columns = benchs.columns
        title = columns[0]
        remaining = columns[1:]
        i = 0
        j = 0
        if len(colors) > len(remaining):
            colors = colors[len(remaining):]
        elif len(colors) < len(remaining):
            colors = [colors * len(remaining)][0][:len(remaining)]
        for column in remaining:
            fig.add_trace(
                go.Bar(
                    name=column,
                    x=benchs[column],
                    y=benchs[title],
                    offsetgroup=i,
                    orientation='h',
                    marker_color = colors[j]
                ),
                row=len(remaining) if grouped else 1,
                col=1,
            )
            if grouped:
                i = i + 1
            j = j + 1
        fig.update_layout(bargroupgap = 0.1)
        fig.show()
