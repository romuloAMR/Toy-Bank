from persistence.account_repository import AccountRepository

class BankService:
    def __init__(self, repository: AccountRepository):
        self.repository = repository

    def register_account(self, account_id: int) -> tuple[bool, float]:
        """
        Try to create an account with a balance of 0 and return whether it was successful or not, and the balance;
        if the account already exists, return the current balance.
        """
        if self.repository.create_account(account_id):
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
    
    def make_deposit(self, account_id: int, amount: float) -> tuple[float, bool]:
        """
        Make the deposit and refund the amount.
        """
        if amount <= 0:
            return -float("inf"), False
        sucess = self.repository.deposit(account_id, amount)
        if sucess:
            return self.repository.get_balance(account_id), sucess
        return -float("inf"), sucess
    
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

    def make_transfer(self, origin_id: int, destination_id: int, amount: float) -> tuple[float, float, bool]:
        """
        Make a transfer from origin to destination and return both balances.
        """
        if amount <= 0:
            return -float("inf"), -float("inf"), False
        
        _, origin_exists = self.check_balance(origin_id)
        _, destination_exists = self.check_balance(destination_id)
        
        if not origin_exists or not destination_exists:
            return -float("inf"), -float("inf"), False
        
        withdraw_success = self.repository.withdrawal(origin_id, amount)

        if not withdraw_success:
            return -float("inf"), -float("inf"), False

        self.repository.deposit(destination_id, amount)
        
        return self.repository.get_balance(origin_id), self.repository.get_balance(destination_id), True
