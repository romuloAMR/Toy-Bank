from domain.bank_service import BankService
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

def run_registration(service):
    """
    Call registration service
    """
    acc_id = _prompt_account_number()
    success, balance = service.register_account(acc_id)
    if success:
        print(f"Conta {acc_id} criada com sucesso. Saldo: R$ {balance:.2f}")
    else:
        print(f"Conta {acc_id} já existe. Saldo: R$ {balance:.2f}")

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
