import pathlib
from enum import Enum
from typing import Iterable
import pandas as pd
from plotly import graph_objects as go
from plotly.subplots import make_subplots

class Plot:
    def __init__(self, output_folder: str) -> None:
        self.__output_folder = pathlib.Path(output_folder)
        self.__create_output_folder()

    class Color(Enum):
        CYAN = '#82B1FF'
        DARK_GRAY = '#303030'
        GRAY = '#404040'
        ORANGE = '#FFAB40'

    def __create_output_folder(self) -> None:
        self.__output_folder.mkdir(parents=True, exist_ok=True)

    def plot_graph(
        self,
        benchs: pd.DataFrame,
        grouped = True,
        colors: Iterable = None,
        title: str = None
    ) -> None:
        fig = make_subplots(rows=2, cols=1)
        columns = benchs.columns
        y_title = columns[0]
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
                    y=benchs[y_title],
                    text=benchs[column],
                    offsetgroup=i,
                    orientation='h',
                    marker_color=colors[j],
                    marker_line_color=colors[j],
                    marker_line_width=2
                )
            )
            if grouped: i += 1
            j += 1

        fig.update_yaxes(ticksuffix='  ')

        fig.update_layout(
            font=dict(family='Roboto', size=18, color='#FFF'),
            title=dict(text=title, font=dict(size=36), x=0.5, xanchor='center'),
            legend=dict(title=None, orientation='h', y=1, yanchor='bottom', x=0.5, xanchor='center'),
            xaxis=dict(gridcolor='rgba(255, 255, 255, 0.12)', zeroline=False),
            bargroupgap=0.2,
            paper_bgcolor=self.Color.GRAY.value,
            plot_bgcolor='rgba(255, 255, 255, 0.06)',
            # height=2160, width=3840
        )
        fig.show()
