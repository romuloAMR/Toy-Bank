from fastapi import APIRouter, Depends, HTTPException

from src.domain.bank_service import BankService
from src.presentation.dependencies import get_bank_service
from src.presentation.schemas import (
    CreateAccountRequest,
    CreditRequest,
    DebitRequest,
    InterestRequest,
    TransferRequest,
)

balance = APIRouter(prefix="/banco/conta", tags=["Account"])


@balance.post("/")
def create_account(
    request: CreateAccountRequest, service: BankService = Depends(get_bank_service)
):

    balance, success = service.register_account(
        request.id,
        request.account_type,
        request.opening_balance,
    )

    return {
        "success": success,
        "balance": round(balance or 0.0, 2),
    }


@balance.get("/{account_id}")
def get_account(account_id: int, service: BankService = Depends(get_bank_service)):

    balance, exists = service.check_balance(account_id)

    if not exists:
        raise HTTPException(
            status_code=404,
            detail="Account not found",
        )

    account_type = service.get_account_type(account_id)

    response = {
        "id": account_id,
        "account_type": account_type,
        "balance": round(balance or 0.0, 2),
    }

    points = service.get_points(account_id)

    if points is not None:
        response["bonus_points"] = points

    return response


@balance.get("/{account_id}/saldo")
def get_balance(account_id: int, service: BankService = Depends(get_bank_service)):

    balance, exists = service.check_balance(account_id)

    if not exists:
        raise HTTPException(
            status_code=404,
            detail="Account not found",
        )

    return {
        "account_id": account_id,
        "balance": round(balance or 0.0, 2),
    }


@balance.put("/{account_id}/credito")
def credit_account(
    account_id: int,
    request: CreditRequest,
    service: BankService = Depends(get_bank_service),
):

    balance, message = service.make_deposit(
        account_id,
        request.amount,
    )

    if balance is None:
        raise HTTPException(
            status_code=400,
            detail=message,
        )

    return {
        "balance": round(balance or 0.0, 2),
        "message": message,
    }


@balance.put("/{account_id}/debito")
def debit_account(
    account_id: int,
    request: DebitRequest,
    service: BankService = Depends(get_bank_service),
):

    balance, message = service.make_withdrawal(
        account_id,
        request.amount,
    )

    if balance is None:
        raise HTTPException(
            status_code=400,
            detail=message,
        )

    return {
        "balance": round(balance or 0.0, 2),
        "message": message,
    }


@balance.put("/transferencia")
def transfer_funds(
    request: TransferRequest, service: BankService = Depends(get_bank_service)
):

    source_balance, destination_balance, message = service.make_transfer(
        request.from_account,
        request.to_account,
        request.amount,
    )

    if source_balance is None or destination_balance is None:
        raise HTTPException(
            status_code=400,
            detail=message,
        )

    return {
        "source_balance": round(source_balance or 0.0, 2),
        "destination_balance": round(destination_balance or 0.0, 2),
        "message": message,
    }


@balance.put("/rendimento")
def apply_interest(
    request: InterestRequest, service: BankService = Depends(get_bank_service)
):

    updated_accounts, message = service.render_interest(request.interest_rate)

    return {
        "updated_accounts": updated_accounts,
        "message": message,
    }
