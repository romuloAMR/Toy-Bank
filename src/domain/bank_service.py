from persistence.account_repository import AccountRepository

from domain.account_types import BONUS_ACCOUNT_TYPE, DEFAULT_ACCOUNT_TYPE, SAVINGS_ACCOUNT_TYPE


class BankService:
    def __init__(self, repository: AccountRepository):
        self.repository = repository

    def register_account(self, account_id: int, account_type: str = DEFAULT_ACCOUNT_TYPE, opening_balance: float = 0.0) -> tuple[float, bool]:
        """
        Try to create an account with a balance of 0 and return whether it was successful or not, and the balance;
        if the account already exists, return the current balance.
        """
        if account_type == SAVINGS_ACCOUNT_TYPE:
            if self.repository.create_account(account_id, account_type, opening_balance):
                return opening_balance, True
        else:
            if self.repository.create_account(account_id, account_type):
                return 0.0, True

        balance = self.repository.get_balance(account_id)

        return balance if balance is not None else 0.0, False

    def check_balance(self, account_id: int) -> tuple[float | None, bool]:
        """
        Returns the balance of the specified account, if it exists.
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

        if not self.repository.account_exists(account_id):
            return None, "Conta inexistente"

        self.repository.deposit(account_id, amount)

        earned_points = self._award_bonus_points_for_deposit(account_id, amount)

        balance = self.repository.get_balance(account_id)

        if earned_points > 0:
            return balance, f"Sucesso ({earned_points} ponto(s) ganhos)"

        return balance, "Sucesso"

    def make_withdrawal(self, account_id: int, amount: float) -> tuple[float | None, str]:
        """
        Make the withdrawal and refund the amount.
        """
        if amount <= 0:
            return None, "Valor deve ser maior que zero"

        current_balance = self.repository.get_balance(account_id)
        if current_balance is None:
            return None, "Conta inexistente"

        account_type = self.repository.get_account_type(account_id)

        if (
            account_type in [DEFAULT_ACCOUNT_TYPE, BONUS_ACCOUNT_TYPE]
            and current_balance - amount < -1000
        ):
            return None, "Limite excedido"

        if (
            account_type == SAVINGS_ACCOUNT_TYPE
            and amount > current_balance
        ):
            return None, "Saldo insuficiente"

        self.repository.withdrawal(account_id, amount)

        return self.repository.get_balance(account_id), "Sucesso"

    def make_transfer(self, origin_id: int, destination_id: int, amount: float) -> tuple[float | None, float | None, str]:
        """
        Make a transfer from origin to destination and return both balances.
        """
        if amount <= 0:
            return None, None, "Valor deve ser maior que zero"

        origin_balance = self.repository.get_balance(origin_id)
        if origin_balance is None:
            return None, None, "Conta de origem inexistente"

        destination_balance = self.repository.get_balance(destination_id)
        if destination_balance is None:
            return None, None, "Conta de destino inexistente"

        origin_type = self.repository.get_account_type(origin_id)

        if (
            origin_type in [DEFAULT_ACCOUNT_TYPE, BONUS_ACCOUNT_TYPE]
            and origin_balance - amount < -1000
        ):
            return None, None, "Limite excedido"

        if (
            origin_type == SAVINGS_ACCOUNT_TYPE
            and amount > origin_balance
        ):
            return None, None, "Saldo insuficiente"

        self.repository.withdrawal(origin_id, amount)
        deposit_success = self.repository.deposit(destination_id, amount)
        if not deposit_success:
            self.repository.deposit(origin_id, amount)
            return None, None, "Erro na transferência"

        earned_points = self._award_bonus_points_for_received_transfer(destination_id, amount)

        origin_balance = self.repository.get_balance(origin_id)
        destination_balance = self.repository.get_balance(destination_id)

        if earned_points > 0:
            return origin_balance, destination_balance, f"Sucesso ({earned_points} ponto(s) ganhos)"

        return origin_balance, destination_balance, "Sucesso"

    def render_interest(self, interest_rate: float) -> tuple[int, str]:
        """
        Applies interest to every savings account.
        """
        if interest_rate < 0:
            return 0, "Taxa inválida"

        updated_accounts = self.repository.apply_interest_to_savings_accounts(interest_rate)

        return updated_accounts, "Sucesso"

    def get_account_type(self, account_id: int) -> str | None:
        """
        Returns the registered account type.
        """
        return self.repository.get_account_type(account_id)

    def get_points(self, account_id: int) -> int | None:
        """
        Returns the registered account points.
        """
        return self.repository.get_points(account_id)

    def _award_bonus_points_for_deposit(self, account_id: int, amount: float) -> int:
        """
        Awards bonus account points for deposits.
        """
        account_type = self.repository.get_account_type(account_id)
        if account_type != BONUS_ACCOUNT_TYPE:
            return 0

        points = int(amount // 100)

        if points > 0:
            self.repository.add_points(account_id, points)

        return points

    def _award_bonus_points_for_received_transfer(self, account_id: int, amount: float) -> int:
        """
        Awards bonus account points for received transfers.
        """
        account_type = self.repository.get_account_type(account_id)
        if account_type != BONUS_ACCOUNT_TYPE:
            return 0

        points = int(amount // 200)
        if points > 0:
            self.repository.add_points(account_id, points)

        return points
