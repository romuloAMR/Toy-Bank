from collections import OrderedDict

from domain.bank_service import BankService
from domain.account_types import (
    ACCOUNT_TYPE_LABELS,
    BONUS_ACCOUNT_TYPE,
    DEFAULT_ACCOUNT_TYPE,
    SAVINGS_ACCOUNT_TYPE,
)


def _prompt_account_number() -> int:
    """
    Read and validate account number input.
    """
    while True:
        num = input("Digite o número da conta: ").strip()

        if num.isdigit():
            return int(num)

        print("Entrada inválida. Digite apenas números.")


def _prompt_amount_number() -> float:
    """
    Read and validate amount input.
    """
    while True:
        num = input("Digite o valor da operação: ").strip().replace(",", ".")

        try:
            return float(num)

        except ValueError:
            print(
                "Entrada inválida. "
                "Digite um valor numérico."
            )

def _prompt_opening_balance() -> float:
    """
    Read opening balance
    """
    while True:
        num = input("Digite o saldo inicial: ").strip().replace(",", ".")

        try:
            return float(num)

        except ValueError:
            print("Entrada inválida. Digite um valor numérico.")


def _prompt_interest_rate() -> float:
    """
    Read and validate interest rate.
    """
    while True:
        num = input("Digite a taxa de juros (%): ").strip().replace(",", ".")

        try:
            return float(num)

        except ValueError:
            print(
                "Entrada inválida. "
                "Digite um valor numérico."
            )


def _prompt_account_type() -> str:
    """
    Ask which account type should be created.
    """
    while True:
        print("\nTipo da conta:")
        print(f"1) {ACCOUNT_TYPE_LABELS[DEFAULT_ACCOUNT_TYPE]}")
        print(f"2) {ACCOUNT_TYPE_LABELS[SAVINGS_ACCOUNT_TYPE]}")
        print(f"3) {ACCOUNT_TYPE_LABELS[BONUS_ACCOUNT_TYPE]}")

        choice = input("Escolha: ").strip()

        if choice == "1":
            return DEFAULT_ACCOUNT_TYPE

        if choice == "2":
            return SAVINGS_ACCOUNT_TYPE

        if choice == "3":
            return BONUS_ACCOUNT_TYPE

        print("Opção inválida.")


def run_registration(service: BankService):
    """
    Create account flow.
    """
    account_id = _prompt_account_number()
    account_type = _prompt_account_type()
    opening_balance = _prompt_opening_balance()

    balance, success = service.register_account(account_id, account_type, opening_balance)
    account_label = ACCOUNT_TYPE_LABELS[account_type]

    if success:
        print(
            f"{account_label} {account_id} criada com sucesso. "
            f"Saldo: R$ {balance:.2f}"
        )

    else:
        print(
            f"Conta {account_id} já existe. "
            f"Saldo atual: R$ {balance:.2f}"
        )

def show_balance(service: BankService):
    """
    Balance flow.
    """
    account_id = _prompt_account_number()

    balance, exists = service.check_balance(account_id)

    if not exists:
        print("Conta não encontrada.")
        return

    print(
        f"Saldo da conta {account_id}: "
        f"R$ {balance:.2f}"
    )

    account_type = service.get_account_type(account_id)

    if account_type == BONUS_ACCOUNT_TYPE:
        points = service.get_points(account_id) or 0

        print(
            f"Pontos bônus: {points}"
        )


def run_deposit(service: BankService):
    """
    Deposit flow.
    """
    account_id = _prompt_account_number()
    amount = _prompt_amount_number()

    balance, msg = service.make_deposit(
        account_id,
        amount,
    )

    if balance is not None:
        print(
            f"Depósito realizado com sucesso!\n"
            f"Novo saldo: R$ {balance:.2f}"
        )

    print(msg)


def run_withdrawal(service: BankService):
    """
    Withdrawal flow.
    """
    account_id = _prompt_account_number()
    amount = _prompt_amount_number()

    balance, msg = service.make_withdrawal(
        account_id,
        amount,
    )

    if balance is not None:
        print(
            f"Saque realizado com sucesso!\n"
            f"Novo saldo: R$ {balance:.2f}"
        )

    else:
        print(msg)


def run_transfer(service: BankService):
    """
    Transfer flow.
    """
    print("Conta de origem:")
    origin_id = _prompt_account_number()

    print("Conta de destino:")
    destination_id = _prompt_account_number()

    amount = _prompt_amount_number()

    origin_balance, destination_balance, msg = service.make_transfer(origin_id, destination_id, amount)

    if (
        origin_balance is not None
        and destination_balance is not None
    ):
        print("\nTransferência realizada!")
        print(
            f"Novo saldo origem ({origin_id}): "
            f"R$ {origin_balance:.2f}"
        )
        print(
            f"Novo saldo destino ({destination_id}): "
            f"R$ {destination_balance:.2f}"
        )

    print(msg)


def run_render_interest(service: BankService):
    """
    Interest rendering flow.
    """
    interest_rate = _prompt_interest_rate()

    updated_accounts, msg = service.render_interest(interest_rate)

    if updated_accounts > 0:
        print(
            f"Rendimento aplicado em "
            f"{updated_accounts} conta(s)."
        )

    print(msg)


class BankCLI:
    """
    Iterative terminal menu.
    """

    def __init__(self, title: str):
        self.title = title
        self._options = OrderedDict()

    def add_option(self, key: str, label: str, handler):
        """
        Register menu option.
        """
        self._options[str(key)] = (
            label,
            handler,
        )

    def run(self, service: BankService):
        """
        Main application loop.
        """
        try:
            while True:
                print(f"\n{self.title}")

                for key, (label, _) in self._options.items():
                    print(f"{key}) {label}")

                choice = input(
                    "Escolha uma opção: "
                ).strip()

                if choice not in self._options:
                    print("Opção inválida.")
                    continue

                _, handler = self._options[choice]

                should_continue = handler(service)

                if should_continue is False:
                    break

        except KeyboardInterrupt:
            print("\n\nSaindo do sistema...")

        except EOFError:
            print("\nConexão encerrada.")
