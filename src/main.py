from fastapi import FastAPI

from src.presentation.balance_router import balance

app = FastAPI(
    title="Toy Bank API",
    version="1.0.0",
)

app.include_router(balance)
