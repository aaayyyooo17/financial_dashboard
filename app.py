import dash
from dash import *
import plotly.graph_objects as go
from data import *

app = dash.Dash(__name__)

app.layout = html.Div([

    html.H1("Stock Dashboard", style = {"fontWeight": "bold"}),


    html.Div([
        dcc.Input(
            id="ticker",        
            value="TSLA",  
            debounce=True,
            placeholder="Enter ticker...",
            type="text",
            style={"paddingTop": "8px", "padding": "8px", "fontSize": "16px"}
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
            style = {"paddingTop": "8px", "padding": "8px", "fontSize": "16px", "width": "150px"}
        ),



    ], style = {"display": "flex", "flexdirection": "row", "gap": "20px", "marginBottom": "20px", "backgroundColor": "#fafafa", "padding": "10px", "borderRadius": "10px"}),

    html.Div(id = "kpi_cards", style = {"display": "flex", "flexDirection": "row", "gap": "20px", "marginBottom": "20px", "width": "25%"}),
    dcc.Graph(id="price_chart", style = {"marginBottom": "20px", "border": "1px solid #ddd", "borderRadius": "10px", "backgroundColor": "#fafafa"}),
    dcc.Graph(id="volume_chart", style = {"marginBottom": "20px", "border": "1px solid #ddd", "borderRadius": "10px", "backgroundColor": "#fafafa"}),
])

@app.callback(
    Output("kpi_cards", "children"),
    Output("price_chart", "figure"),
    Output("volume_chart", "figure"),
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
            html.H3(str(value), style={"margin": "4px"}),
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
            x=df.index,
            open=df["Open"],
            high=df["High"],
            low=df["Low"], 
            close=df["Close"],
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
            x=df.index,  
            y=df["Volume"],
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






