from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import json
import plotly.graph_objects as go

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    # Load the JSON data
    with open('output.json', 'r', encoding='utf-8') as file:
        data = [json.loads(line) for line in file]

    # Prepare data for the plot
    dates = [d['date'] for d in data]
    opens = [float(d['start_transaction']) for d in data]
    highs = [float(d['highest_transaction']) for d in data]
    lows = [float(d['lowest_transaction']) for d in data]
    closes = [float(d['closing_transaction']) for d in data]

    # Create a candlestick chart
    fig = go.Figure(data=[go.Candlestick(x=dates,
                open=opens, high=highs,
                low=lows, close=closes)])

    fig.update_layout(title='Telegram Data Candlestick Chart',
                      xaxis_title='Date',
                      yaxis_title='Price')
    
    # Convert plot to HTML
    graph_html = fig.to_html(full_html=False)

    return f"<html><body>{graph_html}</body></html>"

