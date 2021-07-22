Didn't see a lot of examples out there for this framework, so decided to create one.

[![Deploy](https://button.deta.dev/1/svg)](https://go.deta.dev/deploy)

## Mnual Deployment

We will be using Deta to deploy this API. It's very easy and free.

1. signup for a free account, then install the cli and login.
2. Clone this repo and `cd`into it.
3. run `deta new`

Now wait about a minute (installing the dependacies takes some time). You will see a URL, this is the endpoint

## Step 1: Hello World of FastAPI, Stub out the API endpoints

* Display Hello World
* Map out endpoints we will need, comment what they will do

## Step 2: Mock the UI with Semantic UI and Jinja2 Templates

* Including CSS and JavaScript from the CDN

## Step 3: Database Design

* To design our database, we create SQLAlchemy models
* See what yfinance provides 
* forwardPE, forwardEps, dividendYield, 50 Day, 200 Day, Close
* SQLAlchemy create_all

## Step 4: Add a stock endpoint

* Background task to fetch info and add to db also
* Use Insomnia to test it

## Step 5: Wire home screen

* Show added stocks in a table

## Step 6: Filters to filter table

* Filter boxes on UI
* Use SQLALchemy to filter in db
* Use query parameters to filter
 
## Step 7: Modal to add stock tickers via UI
