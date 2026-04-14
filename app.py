import dash
from dash import *
import plotly.graph_objects as go
from main import *

app = dash.Dash(__name__)

app.layout = html.Div([

    html.H1("Stock Dashboard", style = {""}),


    html.Div([
        dcc.Input(
            id="ticker",        
            value="AAPL",  
            debounce=True,
            placeholder="Enter ticker...",
            type="text",
            style={"padding": "8px", "fontSize": "16px"}
        ),

        dcc.Dropdown(
            id = "period",
            options = [
                {"label": "1 Month",  "value": "1mo"},
                {"label": "3 Months", "value": "3mo"},
                {"label": "6 Months", "value": "6mo"},
                {"label": "1 Year",   "value": "1y"},
                {"label": "5 Years",  "value": "5y"},
            ],
            value="6mo",
            clearable=False,
            style = {}
        ),



    ], style = {}),

    html.Div(id = "kpi_cards"),
    dcc.Graph(id="price-chart"),
    dcc.Graph(id="volume-chart"),
])

@app.callback(
    Output("kpi-cards", "children"),
    Output("price-chart", "figure"),
    Output("volume-chart", "figure"),
    Input("ticker", "value"),
    Input("period", "value")
)

def update_dashboard(ticker, period):
    df = get_stock_data(ticker, period)
    info = get_stock_info(ticker)

    kpi_items = [
        ("Current Price", info['price']),
        ("P/E Ratio", info['pe_ratio']),
        ("52W High", info['52w_high']),
        ("52W Low", info['52w_low']),
    ]

    cards = []

    for label, value in kpi_items:
        card = html.Div([
            html.P(label, style={"margin": 0, "color": "#888", "fontSize": "12px"}),
            html.H3(str(value), style={"margin": "4px 0 0"}),
        ], style={
            "padding": "16px 20px",
            "border": "1px solid #ddd",
            "borderRadius": "10px",
            "minWidth": "130px",
            "backgroundColor": "#fafafa",
        })
        cards.append(card)

        price_fig = go.Figure(data=[
        go.Candlestick(
            x=df.index,        # X axis = dates (the DataFrame's index)
            open=df["Open"],   # Opening price of each day
            high=df["High"],   # Intraday high
            low=df["Low"],     # Intraday low
            close=df["Close"], # Closing price
            name=ticker
        )
    ])


    price_fig.update_layout(
        title=f"{info['name']} — Price ({period})",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        xaxis_rangeslider_visible=False,
        plot_bgcolor="white",
        paper_bgcolor="white",
    )


    vol_fig = go.Figure(data=[
        go.Bar(
            x=df.index,       # X axis = dates
            y=df["Volume"],   # Y axis = number of shares traded
            name="Volume",
            marker_color="steelblue"
        )
    ])


    vol_fig.update_layout(
        title="Daily Trading Volume",
        xaxis_title="Date",
        yaxis_title="Shares Traded",
        plot_bgcolor="white",
        paper_bgcolor="white",
    )

    return cards, price_fig, vol_fig


if __name__ == "__main__":
    app.run(debug=True)






