from persistence.account_repository import AccountRepository

class BankService:
    def __init__(self, repository: AccountRepository):
        self.repository = repository

    def register_account(self, account_id: int, opening_balance: float = 0.0) -> tuple[float, bool]:
        """
        Try to create an account.
        """
        if self.repository.create_account(account_id, opening_balance):
            return opening_balance, True

        balance = self.repository.get_balance(account_id)
        
        return balance if balance is not None else 0.0, False

    def check_balance(self, account_id: int) -> tuple[float | None, bool]:
        """
        Return account balance if account exists.
        """
        balance = self.repository.get_balance(account_id)

        if balance is None:
            return None, False

        return balance, True

    def make_deposit(self, account_id: int, amount: float) -> tuple[float | None, str]:
        """
        Make the deposit and refund the amount.
        """
        if amount <= 0:
            return None, "Valor deve ser maior que zero"

        success = self.repository.deposit(account_id, amount)

        if not success:
            return None, "Conta inexistente"

        return self.repository.get_balance(account_id), "Sucesso"

    def make_withdrawal(self, account_id: int, amount: float) -> tuple[float | None, str]:
        """
        Make the withdrawal and refund the amount.
        """
        if amount <= 0:
            return None, "Valor deve ser maior que zero"

        current_balance = self.repository.get_balance(account_id)

        if current_balance is None:
            return None, "Conta inexistente"

        if amount > current_balance:
            return None, "Saldo insuficiente"

        success = self.repository.withdrawal(account_id, amount)

        if not success:
            return None, "Erro no saque"

        return self.repository.get_balance(account_id), "Sucesso"

    def make_transfer(self, origin_id: int, destination_id: int, amount: float) -> tuple[float | None, float | None, str]:
        """
        Make a transfer from origin to destination and return both balances.
        """
        if amount <= 0:
            return None, None, "Valor deve ser maior que zero"

        origin_balance = self.repository.get_balance(origin_id)
        if origin_balance is None:
            return None, None, "Conta de origem não existe"
        
        destination_balance = self.repository.get_balance(destination_id)
        if destination_balance is None:
            return None, None, "Conta de destino não existe"

        if amount > origin_balance:
            return None, None, "Saldo insuficiente"

        withdraw_success = self.repository.withdrawal(origin_id, amount)
        if not withdraw_success:
            return None, None, "Erro na retirada"

        deposit_success = self.repository.deposit(destination_id, amount)
        if not deposit_success:
            _ = self.repository.deposit(origin_id, amount)
            return None, None, "Erro no deposito"

        return (
            self.repository.get_balance(origin_id),
            self.repository.get_balance(destination_id),
            "Sucesso",
        )
