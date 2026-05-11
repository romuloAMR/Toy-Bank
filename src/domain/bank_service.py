from persistence.account_repository import AccountRepository
from domain.account_types import BONUS_ACCOUNT_TYPE, DEFAULT_ACCOUNT_TYPE

class BankService:
    def __init__(self, repository: AccountRepository):
        self.repository = repository

    def register_account(
        self, account_id: int, account_type: str = DEFAULT_ACCOUNT_TYPE
    ) -> tuple[bool, float]:
        """
        Try to create an account with a balance of 0 and return whether it was successful or not, and the balance;
        if the account already exists, return the current balance.
        """
        if self.repository.create_account(account_id, account_type):
            return True, 0.0

        balance = self.repository.get_balance(account_id)
        return False, balance

    def check_balance(self, account_id: int) -> tuple[float, bool]:
        """
        Returns the balance of the specified account, if it exists.
        """
        balance = self.repository.get_balance(account_id)
        if balance == -float("inf"):
            return balance, False
        return balance, True
    
    def make_deposit(self, account_id: int, amount: float) -> tuple[float, int, bool]:
        """
        Make the deposit and refund the amount.
        """
        if amount <= 0:
            return -float("inf"), 0, False
        sucess = self.repository.deposit(account_id, amount)
        if sucess:
            earned_points = self._award_bonus_points_for_deposit(account_id, amount)
            return self.repository.get_balance(account_id), earned_points, sucess
        return -float("inf"), 0, sucess
    
    def make_withdrawal(self, account_id: int, amount: float) -> tuple[float, bool]:
        """
        Make the withdrawal and refund the amount.
        """
        if amount <= 0:
            return -float("inf"), False
        sucess = self.repository.withdrawal(account_id, amount)
        if sucess:
            return self.repository.get_balance(account_id), sucess
        return -float("inf"), sucess

    def make_transfer(
        self, origin_id: int, destination_id: int, amount: float
    ) -> tuple[float, float, int, bool]:
        """
        Make a transfer from origin to destination and return both balances.
        """
        if amount <= 0:
            return -float("inf"), -float("inf"), 0, False
        
        _, origin_exists = self.check_balance(origin_id)
        _, destination_exists = self.check_balance(destination_id)
        
        if not origin_exists or not destination_exists:
            return -float("inf"), -float("inf"), 0, False
        
        withdraw_success = self.repository.withdrawal(origin_id, amount)

        if not withdraw_success:
            return -float("inf"), -float("inf"), 0, False

        self.repository.deposit(destination_id, amount)
        earned_points = self._award_bonus_points_for_received_transfer(
            destination_id, amount
        )
        
        return (
            self.repository.get_balance(origin_id),
            self.repository.get_balance(destination_id),
            earned_points,
            True,
        )

    def render_interest(self, interest_rate: float) -> tuple[int, bool]:
        """
        Applies interest to every savings account.
        """
        if interest_rate < 0:
            return 0, False

        updated_accounts = self.repository.apply_interest_to_savings_accounts(interest_rate)
        return updated_accounts, True

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

    def _award_bonus_points_for_received_transfer(
        self, account_id: int, amount: float
    ) -> int:
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
