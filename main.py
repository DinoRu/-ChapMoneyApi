import uvicorn
from authlib import author
from fastapi import FastAPI

from app.routers import users, accounts
from app.routers import transactions
from app.routers import currency
from app.routers import countries
from app.routers import exchange_rates
from app.routers import receiving_methods
from app.routers import sending_methods
from app.routers import transfer_fees

app = FastAPI(
    title="Banking App",
    description="Send money app",
    author="Diarra Moustapha",
    version="1.0.0",
    openapi_url="/api/v1/openapi.json",
    swagger_ui_parameters={
        "persistAuthorization": True
    }
)

app.include_router(users.router)
app.include_router(transactions.router)
app.include_router(currency.router)
app.include_router(countries.router)
# app.include_router(accounts.router)
app.include_router(exchange_rates.router)
app.include_router(receiving_methods.router)
app.include_router(sending_methods.router)
app.include_router(transfer_fees.router)


@app.get("/")
async def root():
    return {'message': 'Welcome to Banking Api'}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)