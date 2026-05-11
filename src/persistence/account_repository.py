import pandas as pd
import os
from domain.account_types import (
    BONUS_ACCOUNT_INITIAL_POINTS,
    BONUS_ACCOUNT_TYPE,
    DEFAULT_ACCOUNT_TYPE,
    SAVINGS_ACCOUNT_TYPE,
)


class AccountRepository:
    def __init__(self, file_path: str = "data/accounts.csv"):
        """
        Initialise CSV database for accounts
        """
        self.FILE_PATH = file_path
        if os.path.exists(self.FILE_PATH):
            self._db = pd.read_csv(self.FILE_PATH)
        else:
            db = pd.DataFrame(columns=["account_id", "balance", "account_type", "points"])
            directory = os.path.dirname(self.FILE_PATH)
            if directory:
                os.makedirs(directory, exist_ok=True)
            db.to_csv(self.FILE_PATH, index=False)
            self._db = pd.read_csv(self.FILE_PATH)
            print("Account table create with sucess!")

        if "account_type" not in self._db.columns:
            self._db["account_type"] = DEFAULT_ACCOUNT_TYPE

        if "points" not in self._db.columns:
            self._db["points"] = 0
            bonus_accounts = self._db["account_type"] == BONUS_ACCOUNT_TYPE
            self._db.loc[bonus_accounts, "points"] = BONUS_ACCOUNT_INITIAL_POINTS
            self._db.to_csv(self.FILE_PATH, index=False)

        self._db['account_id'] = self._db['account_id'].astype(int)
        self._db['balance'] = self._db['balance'].astype(float)
        self._db["account_type"] = self._db["account_type"].fillna(DEFAULT_ACCOUNT_TYPE).astype(str)
        self._db["points"] = self._db["points"].fillna(0).astype(int)

    def account_exists(self, id: int) -> bool:
        """
        Check whether or not an account exists
        """
        return id in self._db['account_id'].values

    def create_account(self, id: int, account_type: str = DEFAULT_ACCOUNT_TYPE) -> bool:
        """
        Create an account on the system
        """
        if self.account_exists(id):
            return False

        points = BONUS_ACCOUNT_INITIAL_POINTS if account_type == BONUS_ACCOUNT_TYPE else 0
        new_registration = pd.DataFrame(
            [{"account_id": id, "balance": 0.0, "account_type": account_type, "points": points}]
        )
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

        current_balance = self.get_balance(id)

        if amount > current_balance:
            return False

        self._db.loc[self._db['account_id'] == id, 'balance'] -= amount
        self._db.to_csv(self.FILE_PATH, index=False)

        return True

    def get_account_type(self, id: int) -> str | None:
        """
        Returns the type of an account.
        """
        account_type = self._db.loc[self._db["account_id"] == id, "account_type"].values
        if len(account_type) > 0:
            return str(account_type[0])
        return None

    def apply_interest_to_savings_accounts(self, interest_rate: float) -> int:
        """
        Applies an interest rate to every savings account and returns how many were updated.
        """
        savings_accounts = self._db["account_type"] == SAVINGS_ACCOUNT_TYPE
        updated_accounts = int(savings_accounts.sum())

        if updated_accounts == 0:
            return 0

        multiplier = 1 + (interest_rate / 100)
        self._db.loc[savings_accounts, "balance"] *= multiplier
        self._db.to_csv(self.FILE_PATH, index=False)

        return updated_accounts

    def get_points(self, id: int) -> int | None:
        """
        Returns the points of an account.
        """
        points = self._db.loc[self._db["account_id"] == id, "points"].values
        if len(points) > 0:
            return int(points[0])
        return None

    def add_points(self, id: int, points: int) -> bool:
        """
        Adds points to an account.
        """
        if not self.account_exists(id):
            return False

        self._db.loc[self._db["account_id"] == id, "points"] += points
        self._db.to_csv(self.FILE_PATH, index=False)
        return True
