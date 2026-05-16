import os
import pandas as pd


class AccountRepository:
    _FILE_PATH = "data/accounts.csv"

    def __init__(self):
        """
        Initialize CSV database for accounts.
        """
        if not os.path.exists(self._FILE_PATH):
            os.makedirs(os.path.dirname(self._FILE_PATH), exist_ok=True)

            db = pd.DataFrame({
                "account_id": pd.Series(dtype="int64"),
                "balance": pd.Series(dtype="float64"),
            })

            db.to_csv(self._FILE_PATH, index=False)
            print("Account table created successfully!")

        self._db = pd.read_csv(self._FILE_PATH)

        if self._db.empty:
            self._db = pd.DataFrame({
                "account_id": pd.Series(dtype="int64"),
                "balance": pd.Series(dtype="float64"),
            })

        else:
            self._db = self._db.astype({"account_id": "int64", "balance": "float64"})

    def _save(self) -> None:
        """
        Persist data to CSV.
        """
        self._db.to_csv(self._FILE_PATH, index=False)

    def account_exists(self, account_id: int) -> bool:
        """
        Check whether an account exists.
        """
        return (self._db["account_id"] == account_id).any()

    def create_account(self, account_id: int, opening_balance: float = 0.0) -> bool:
        """
        Create a new account.
        """
        if self.account_exists(account_id):
            return False

        new_account = pd.DataFrame([
            {
                "account_id": account_id,
                "balance": opening_balance,
            }
        ])

        self._db = pd.concat([self._db, new_account], ignore_index=True)

        self._save()

        return True

    def get_balance(self, account_id: int) -> float | None:
        """
        Return account balance.
        """
        balance = self._db.loc[self._db["account_id"] == account_id, "balance"].values
        if len(balance) == 0:
            return None
        return float(balance[0])

    def deposit(self, account_id: int, amount: float) -> bool:
        """
        Deposit money into account.
        """
        if not self.account_exists(account_id):
            return False

        self._db.loc[self._db["account_id"] == account_id, "balance"] += amount
        self._save()

        return True

    def withdrawal(self, account_id: int, amount: float) -> bool:
        """
        Withdraw money from account.
        """
        if not self.account_exists(account_id):
            return False

        self._db.loc[self._db["account_id"] == account_id, "balance"] -= amount
        self._save()

        return True
