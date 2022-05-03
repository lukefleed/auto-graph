from calendar import c
import shutil
from enum import Enum
from pathlib import Path
from typing import Iterable
import numpy as np
import pandas as pd
import plotly.io as pio
from plotly import graph_objects as go


class Plot:
    def __init__(self, output_dir: Path) -> None:
        self.__output_dir = output_dir
        self.__video_output_dir = output_dir.joinpath('video')
        self.__publication_output_dir = output_dir.joinpath('publication')
        self.__clean_output_dirs()

    class Color(Enum):
        CYAN = '#82B1FF'
        GRAY_100 = '#EEEEEE'
        GRAY_600 = '#404040'
        GRAY_700 = '#303030'
        ORANGE = '#FFAB40'

    def __clean_output_dirs(self) -> None:
        '''Ensure that the output directories exists and are empty'''
        if self.__output_dir.exists(): shutil.rmtree(str(self.__output_dir))
        self.__video_output_dir.mkdir(parents=True)
        self.__publication_output_dir.mkdir(parents=True)

    def plot_graph(
        self,
        data: pd.DataFrame,
        title: str = None,
        write_to_file: bool = True
    ) -> None:
        video_fig_name = self.__video_output_dir.joinpath(f'{title}.png')
        publication_fig_name = self.__publication_output_dir.joinpath(f'{title}.png')

        # Replace NaN values with empty strings
        data = data.replace(np.nan, '', regex=True)

        subtitle = data.iloc[0, 1] # Subtitle is first row, second column
        x_title = data.iloc[1, 1] # Title of the X axis is second row, second column
        grouped = data.iloc[2, 1] == 'Y' # Group based on the content of third row, second column
        data.columns = data.iloc[4] # Headings are on the fifth row
        data = data[5:] # Data starts from the fifth row
        columns = data.columns
        y_title = columns[0]
        remaining = columns[1:]
        i = 0
        j = 0

        if len(remaining) == 1:
            colors = [Plot.Color.GRAY_100.value]
        elif grouped:
            colors = [Plot.Color.GRAY_100.value, Plot.Color.ORANGE.value]
        else:
            colors = [Plot.Color.ORANGE.value, Plot.Color.GRAY_100.value]

        if len(colors) > len(remaining):
            colors = colors[len(remaining):]
        elif len(colors) < len(remaining):
            colors = [colors * len(remaining)][0][:len(remaining)]

        bars = []
        for column in remaining:
            bars.append(go.Bar(
                name=column,
                x=data[column],
                y=data[y_title],
                text=data[column],
                offsetgroup=i,
                orientation='h',
                marker_color=colors[j],
                marker_line_color=colors[j],
                marker_line_width=2
            ))
            if not grouped: i += 1
            j += 1

        common_layout = dict(
            font=dict(family='Roboto', size=22, color='#FFF'),
            title=dict(
                text=f'{title}<br><sup>{subtitle}</sup>',
                font=dict(size=36),
                x=0.5, xanchor='center'
            ),
            xaxis=dict(gridcolor='rgba(255, 255, 255, 0.12)', zeroline=False),
            yaxis=dict(ticksuffix='  ', autorange='reversed'),
            bargroupgap=0.2,
            paper_bgcolor=self.Color.GRAY_600.value,
            plot_bgcolor='rgba(0, 0, 0, 0)',
        )

        # Setup video layout

        video_fig = go.Figure(
            data=bars,
            layout=dict(
                **common_layout,
                legend=dict(title=None, orientation='h', y=1, yanchor='bottom', x=-0.012, xanchor='left'),
                height=960, width=1920,
                margin=dict(l=400, r=400, t=175, b=125),
                annotations=[
                    go.layout.Annotation(
                        text=x_title,
                        align='left',
                        showarrow=False,
                        xref='paper',
                        yref='paper',
                        x=-0.006,
                        y=-0.1
                    )
                ]
            )
        )

        if write_to_file:
            pio.write_image(video_fig, video_fig_name, scale=2)
        else:
            video_fig.show()

        # Setup publication layout

        publication_fig = go.Figure(
            data=bars,
            layout=dict(
                **common_layout,
                legend=dict(title=None, orientation='h', y=1, yanchor='bottom', x=-0.015, xanchor='left'),
                height=960, width=960,
                margin=dict(t=200, b=125),
                annotations=[
                    go.layout.Annotation(
                        text=x_title,
                        align='left',
                        showarrow=False,
                        xref='paper',
                        yref='paper',
                        x=-0.009,
                        y=-0.1
                    )
                ]
            )
        )

        if write_to_file:
            pio.write_image(publication_fig, publication_fig_name, scale=1.334)
        else:
            publication_fig.show()
