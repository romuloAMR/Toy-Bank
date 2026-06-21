from src.domain.bank_service import BankService
from src.persistence.account_repository import AccountRepository

repository = AccountRepository()


def get_bank_service():
    return BankService(repository)
