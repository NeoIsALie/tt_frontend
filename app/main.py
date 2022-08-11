import asyncio
import json
from typing import Any

import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, dcc, html

from .config import SERVER_URL
from .request import request
from .styles import block_style

colors = {"background": "#000000", "text": "#ffFFFF"}

app = Dash(__name__)

app.layout = html.Div(
    [html.H1('Курс валют', style={
        "textAlign": "center",
        "color": colors["text"]
    }),
    html.H3('Текущая валюта: n/a', id='title',
            style={
                "textAlign": "center",
                "color": colors["text"]
            }
            ),
    html.Div(
        [
            html.P('Выбрать валюту:',
                   style={
                       "textAlign": "center",
                       "color": colors["text"]
                   }
                   ),
            dcc.Dropdown(
                id='ticker_selector',
                options=[],
                value=1,
                clearable=False,
                style=
            ),
        ],
        style=block_style,
    ),
    dcc.Graph(id='graph'),
    dcc.Store(id='ticker_list'),
    dcc.Store(id='ticker_id'),
    dcc.Interval(
        id='interval',
        interval=1 * 1000,
        n_intervals=0,
    ),
],
    style={"backgroundColor": colors["background"]},
)


def get_ticker_data(ticker_id: str) -> dict:
    """Запрос данных по валюте по ее ID."""
    resp = asyncio.run(request(f'{SERVER_URL}/tickers/{ticker_id}'))
    return resp


@app.callback(Output('ticker_list', 'data'), Input('ticker_selector', 'value'))
def save_title(_: str) -> str:
    """Сохранение списка валют в кэш."""
    resp = asyncio.run(request(f'{SERVER_URL}/tickers'))
    return json.dumps([{'label': el['title'], 'value': el['id']} for el in resp])


@app.callback(Output('ticker_selector', 'options'), Input('ticker_list', 'data'))
def update_title(data: str) -> list:
    """Вывод отсортированного списка валют из кеша."""
    return sorted(json.loads(data), key=lambda x: x['label'])


@app.callback(Output('ticker_id', 'data'), Input('ticker_selector', 'value'))
def update_dataframe(ticker_id: str) -> str:
    """Сохранение ID валюты в кэш при переключении селектора."""
    return ticker_id


@app.callback(
    Output('title', 'children'),
    Output('graph', 'figure'),
    Input('ticker_id', 'data'),
    Input('interval', 'n_intervals'),
)
def display_data(ticker_id: str, _: int) -> tuple[str, Any]:
    """Получение ID валюты из кеша и обновление данных по валюте."""
    resp = get_ticker_data(ticker_id)
    df = pd.DataFrame(resp['rates'])
    fig = px.line(df, x='timestamp', y='rate', template='plotly_dark')
    return f"Current ticker: {resp['title']}", fig
