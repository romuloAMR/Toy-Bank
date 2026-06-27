from pydantic import BaseModel, Field


class CreateAccountRequest(BaseModel):
    id: int
    account_type: str
    opening_balance: float = 0.0


class CreditRequest(BaseModel):
    amount: float


class DebitRequest(BaseModel):
    amount: float


class TransferRequest(BaseModel):
    from_account: int = Field(alias="from")
    to_account: int = Field(alias="to")
    amount: float


class InterestRequest(BaseModel):
    interest_rate: float
