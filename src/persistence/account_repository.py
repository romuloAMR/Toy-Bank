from pathlib import Path
import pandas as pd

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
        self._file_path = Path(file_path)

        if not self._file_path.exists():
            self._file_path.parent.mkdir(parents=True, exist_ok=True)

            db = pd.DataFrame({
                "account_id": pd.Series(dtype="int64"),
                "balance": pd.Series(dtype="float64"),
                "account_type": pd.Series(dtype="str"),
                "points": pd.Series(dtype="int64"),
            })

            db.to_csv(self._file_path, index=False)

        self._db = pd.read_csv(self._file_path)

        if self._db.empty:
            self._db = pd.DataFrame({
                "account_id": pd.Series(dtype="int64"),
                "balance": pd.Series(dtype="float64"),
                "account_type": pd.Series(dtype="str"),
                "points": pd.Series(dtype="int64"),
            })

        self._db = self._db.astype({
            "account_id": "int64",
            "balance": "float64",
            "account_type": "str",
            "points": "int64",
        })

    def _save(self):
        """
        Save DB.
        """
        self._db.to_csv(self._file_path, index=False)

    def account_exists(self, account_id: int) -> bool:
        """
        Check whether or not an account exists
        """
        return (self._db["account_id"] == account_id).any()

    def create_account(self, account_id: int, account_type: str = DEFAULT_ACCOUNT_TYPE, opening_balance: float = 0.0) -> bool:
        """
        Create an account on the system
        """
        if self.account_exists(account_id):
            return False

        points = BONUS_ACCOUNT_INITIAL_POINTS if account_type == BONUS_ACCOUNT_TYPE else 0

        new_account = pd.DataFrame([{
            "account_id": account_id,
            "balance": opening_balance,
            "account_type": account_type,
            "points": points,
        }])

        self._db = pd.concat([self._db, new_account], ignore_index=True)

        self._save()

        return True

    def get_balance(self, account_id: int) -> float | None:
        """
        Returns the balance of an account
        """
        balance = self._db.loc[self._db["account_id"] == account_id, "balance"].values
        if len(balance) == 0:
            return None

        return float(balance[0])

    def deposit(self, account_id: int, amount: float) -> bool:
        """
        Deposits the amount into the account.
        """
        if not self.account_exists(account_id):
            return False

        self._db.loc[self._db["account_id"] == account_id, "balance"] += amount
        self._save()

        return True

    def withdrawal(self, account_id: int, amount: float) -> bool:
        """
        Withdraws money from the account.
        """
        if not self.account_exists(account_id):
            return False

        self._db.loc[self._db["account_id"] == account_id, "balance"]-= amount
        self._save()

        return True

    def get_account_type(self, account_id: int) -> str | None:
        """
        Returns the type of an account.
        """
        account_type = self._db.loc[self._db["account_id"] == account_id, "account_type"].values
        if len(account_type) == 0:
            return None

        return str(account_type[0])

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
        self._save()

        return updated_accounts

    def get_points(self, account_id: int) -> int | None:
        """
        Returns the points of an account.
        """
        points = self._db.loc[self._db["account_id"] == account_id, "points"].values
        if len(points) == 0:
            return None

        return int(points[0])

    def add_points(self, account_id: int, points: int) -> bool:
        """
        Adds points to an account.
        """
        if not self.account_exists(account_id):
            return False

        self._db.loc[self._db["account_id"] == account_id, "points"] += points
        self._save()

        return True
