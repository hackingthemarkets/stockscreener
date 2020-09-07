import yfinance
from deta import App, Deta
from fastapi import BackgroundTasks, Depends, FastAPI, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

deta = Deta()
db = deta.Base("stocks")
app = App(FastAPI())
templates = Jinja2Templates(directory="templates")

class StockRequest(BaseModel):
    symbol: str


@app.get("/")
def home(request: Request, forward_pe = None, dividend_yield = None, ma50 = None, ma200 = None):
    """
    show all stocks in the database and button to add more
    button next to each stock to delete from database
    filters to filter this list of stocks
    button next to each to add a note or save for later
    """

    query = {}
    if forward_pe:
        query["forward_pe?gt"] = forward_pe

    if dividend_yield:
        query["dividend_yield?gt"] = dividend_yield
    
    stocks = next(db.fetch(query))
    if ma50:
        stocks = [s for s in stocks if s.get("price") and s.get("price") > s.get("ma50")]
    
    if ma200:
        stocks = [s for s in stocks if s.get("price") and s.get("price") > s.get("ma200")]


    return templates.TemplateResponse("home.html", {
        "request": request, 
        "stocks": stocks, 
        "dividend_yield": dividend_yield,
        "forward_pe": forward_pe,
        "ma200": ma200,
        "ma50": ma50
    })


def fetch_stock_data(symbol: str):
    yahoo_data = yfinance.Ticker(symbol)
    print(yahoo_data, "hello")
    db.put({
        "key": symbol,
        "symbol": symbol,
        "ma200": yahoo_data.info['twoHundredDayAverage'],
        "ma50": yahoo_data.info['fiftyDayAverage'],
        "price": yahoo_data.info['previousClose'],
        "forward_pe": yahoo_data.info['forwardPE'],
        "forward_eps": yahoo_data.info['forwardEps'],
        "dividend_yield": (yahoo_data.info.get('dividendYield') or 0) * 100
    })


@app.post("/stock")
async def create_stock(stock_request: StockRequest, background_tasks: BackgroundTasks):
    """
    add one or more tickers to the database
    background task to use yfinance and load key statistics
    """

    background_tasks.add_task(fetch_stock_data, stock_request.symbol)

    return {
        "code": "success",
        "message": "stock was added to the database"
    }


@app.lib.run()
def reset_db(event):
    items = next(db.fetch())
    for item in items:
        db.delete(item["key"])
    return "OK"
