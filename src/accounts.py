class AccountStore:
    def __init__(self):
        self._accounts = {}

    def create_account(self, number: str) -> bool:
        if number in self._accounts:
            return False
        self._accounts[number] = 0.0
        return True

    def get_balance(self, number: str):
        return self._accounts.get(number)
