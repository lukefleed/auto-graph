import shutil
from enum import Enum
from pathlib import Path
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
        P1 = '#1e81b0'
        P2 = '#eeeee4'
        P3 = '#e28743'
        P4 = '#eab676'
        P5 = '#76b5c5'

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
        else:
            colors = [Plot.Color.P4.value,Plot.Color.P3.value,Plot.Color.P2.value,Plot.Color.P5.value,Plot.Color.P1.value]

        if len(colors) > len(remaining):
            colors = colors[:len(remaining)]
        elif len(colors) < len(remaining):
            colors = [colors * len(remaining)][0][:len(remaining)]

        size_map = {
            "5":13,
            "4":14,
            "3":18,
            "2":21,
            "1":26
        }
        if str(len(remaining)) in size_map.keys():
            size = size_map[str(len(remaining))]
        else:
            size = 10
            print("Avvisa Flavio che hai grafi con numero di colonne mai fatto")
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
                marker_line_width=2,
                textposition = "inside",
                textangle=0,
                textfont=dict(family='Roboto', size=size, color='black'),
                constraintext = 'none'
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
