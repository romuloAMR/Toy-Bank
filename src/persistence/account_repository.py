import pandas as pd
import os

class AccountRepository:
    def __init__(self):
        """
        Initialise CSV database for accounts
        """
        self.FILE_PATH = "data/accounts.csv"
        if os.path.exists(self.FILE_PATH):
            self._db = pd.read_csv(self.FILE_PATH)
        else:
            db = pd.DataFrame(columns=["account_id", "balance"])
            os.makedirs(os.path.dirname(self.FILE_PATH), exist_ok=True)
            db.to_csv(self.FILE_PATH, index=False)
            self._db = pd.read_csv(self.FILE_PATH)
            print("Account table create with sucess!")

        self._db['account_id'] = self._db['account_id'].astype(int)
        self._db['balance'] = self._db['balance'].astype(float)

    def account_exists(self, id: int) -> bool:
        """
        Check whether or not an account exists
        """
        return id in self._db['account_id'].values

    def create_account(self, id: int) -> bool:
        """
        Create an account on the system
        """
        if self.account_exists(id):
            return False
            
        new_registration = pd.DataFrame([{"account_id": id, "balance": 0.0}])
        self._db = pd.concat([self._db, new_registration], ignore_index=True)
        self._db.to_csv(self.FILE_PATH, index=False)
        return True

    def get_balance(self, id: int) -> float:
        """
        Returns the balance of an account
        """
        balance = self._db.loc[self._db['account_id'] == id, 'balance'].values
        if len(balance) > 0:
            return float(balance[0])
        return -float("inf")
    
    def deposit(self, id: int, amount: float) -> bool:
        """
        Deposits the amount into the account.
        """
        if not self.account_exists(id):
            return False

        self._db.loc[self._db['account_id'] == id, 'balance'] += amount
        self._db.to_csv(self.FILE_PATH, index=False)

        return True

    def withdrawal(self, id: int, amount: float) -> bool:
        """
        Withdraws money from the account.
        """
        if not self.account_exists(id):
            return False

        self._db.loc[self._db['account_id'] == id, 'balance'] -= amount
        self._db.to_csv(self.FILE_PATH, index=False)

        return True
