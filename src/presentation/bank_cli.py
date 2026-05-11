from domain.bank_service import BankService
from domain.account_types import ACCOUNT_TYPE_LABELS, DEFAULT_ACCOUNT_TYPE, SAVINGS_ACCOUNT_TYPE
from collections import OrderedDict

def _prompt_account_number() -> int:
    """
    Clear the account field
    """
    while True:
        num = input("Digite o número da conta: ").strip()
        if num.isdigit():
            return int(num)
        print("Entrada inválida. Digite apenas números.")

def _prompt_amount_number() -> float:
    """
    Clear the amount field
    """
    while True:
        num = input("Digite o valor para operação: ").strip().replace(",",".")
        try:
            return float(num)
        except ValueError:
            print("Entrada inválida. Digite um valor numérico (ex: 100.50).")

def _prompt_interest_rate() -> float:
    """
    Clear the interest rate field
    """
    while True:
        num = input("Digite a taxa de juros (%): ").strip().replace(",",".")
        try:
            return float(num)
        except ValueError:
            print("Entrada inválida. Digite uma taxa numérica (ex: 10.5).")

def _prompt_account_type() -> str:
    """
    Ask the user which account type should be created.
    """
    while True:
        print("Tipo da conta:")
        print(f"1) {ACCOUNT_TYPE_LABELS[DEFAULT_ACCOUNT_TYPE]}")
        print(f"2) {ACCOUNT_TYPE_LABELS[SAVINGS_ACCOUNT_TYPE]}")
        choice = input("Escolha: ").strip()
        if choice == "1":
            return DEFAULT_ACCOUNT_TYPE
        if choice == "2":
            return SAVINGS_ACCOUNT_TYPE
        print("Opção inválida.")

def run_registration(service):
    """
    Call registration service
    """
    acc_id = _prompt_account_number()
    account_type = _prompt_account_type()
    success, balance = service.register_account(acc_id, account_type)
    if success:
        account_label = ACCOUNT_TYPE_LABELS[account_type]
        print(f"{account_label} {acc_id} criada com sucesso. Saldo: R$ {balance:.2f}")
    else:
        existing_type = service.get_account_type(acc_id) or DEFAULT_ACCOUNT_TYPE
        account_label = ACCOUNT_TYPE_LABELS.get(existing_type, existing_type)
        print(f"{account_label} {acc_id} já existe. Saldo: R$ {balance:.2f}")

def show_balance(service):
    """
    Call balance service
    """
    acc_id = _prompt_account_number()
    balance, exists = service.check_balance(acc_id)
    if exists:
        print(f"Saldo da conta {acc_id}: R$ {balance:.2f}")
    else:
        print(f"Conta {acc_id} não encontrada.")

def run_deposit(service: BankService):
    """
    Call deposit service
    """
    acc_id = _prompt_account_number()
    amount = _prompt_amount_number()
    
    if amount <= 0:
        print("O valor do depósito deve ser maior que zero.")
        return

    balance, success = service.make_deposit(acc_id, amount)
    if success:
        print(f"Depósito realizado! Novo saldo da conta {acc_id}: R$ {balance:.2f}")
    else:
        print(f"Erro: Conta {acc_id} não encontrada.")

def run_withdrawal(service: BankService):
    """
    Call withdrawal service
    """
    acc_id = _prompt_account_number()
    amount = _prompt_amount_number()
    
    if amount <= 0:
        print("O valor do saque deve ser maior que zero.")
        return

    balance, success = service.make_withdrawal(acc_id, amount)
    if success:
        print(f"Saque realizado! Novo saldo da conta {acc_id}: R$ {balance:.2f}")
    else:
        print(f"Erro: Conta {acc_id} não encontrada.")

def run_transfer(service: BankService):
    """
    Call transfer service
    """
    print("Conta de origem:")
    origin_id = _prompt_account_number()
    print("Conta de destino:")
    destination_id = _prompt_account_number()
    amount = _prompt_amount_number()

    if amount <= 0:
        print("O valor da transferência deve ser maior que zero.")
        return

    origin_balance, destination_balance, success = service.make_transfer(origin_id, destination_id, amount)
    if success:
        print(f"Transferência realizada!")
        print(f"Novo saldo da conta {origin_id}: R$ {origin_balance:.2f}")
        print(f"Novo saldo da conta {destination_id}: R$ {destination_balance:.2f}")
    else:
        print("Erro: verifique se as contas existem e o valor é válido.")

def run_render_interest(service: BankService):
    """
    Call render interest service
    """
    interest_rate = _prompt_interest_rate()

    if interest_rate < 0:
        print("A taxa de juros não pode ser negativa.")
        return

    updated_accounts, success = service.render_interest(interest_rate)
    if success:
        print(
            f"Rendimento aplicado com sucesso em {updated_accounts} conta(s) poupança."
        )
    else:
        print("Erro ao aplicar rendimento.")

class BankCLI:
    """
    Iterative menu for the Bank.
    """
    def __init__(self, title: str):
        """
        Init Bank CLI
        """
        self.title = title
        self._options = OrderedDict()

    def add_option(self, key, label, handler):
        """
        Add new services to the bank
        """
        self._options[str(key)] = (label, handler)

    def run(self, service):
        """
        Main loop
        """
        try:
            while True:
                print(f"\n{self.title}")
                for k, (label, _) in self._options.items():
                    print(f"{k}) {label}")

                choice = input("Escolha: ").strip()
                if choice in self._options:
                    _, handler = self._options[choice]
                    if handler(service) is False:
                        break
                else:
                    print("Opção inválida.")
        except KeyboardInterrupt:
            print("\n\nSaindo do sistema... Até logo!")

        except EOFError:
            print("\nConexão encerrada. Saindo...")
