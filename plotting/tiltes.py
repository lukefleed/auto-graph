from dataclasses import dataclass


@dataclass
class Title:
    title: str
    font_size: float = 70.0


@dataclass
class Suptitle:
    title: str
    font_size: float = 90.0


@dataclass
class Xlabel:
    label: str
    font_size: float = 70.0


@dataclass
class Ylabel:
    label: str
    font_size: float = 70.0


@dataclass
class PlotTitles:
    '''Classe che tiene insieme tutte le informazioni testuali dei grafici
    fatti da plotting'''

    title: Title
    suptitle: Suptitle
    xlabel: Xlabel
    ylabel: Ylabel
