from collections import OrderedDict

def _prompt_account_number() -> int:
    """
    Clear the text field
    """
    while True:
        num = input("Digite o número da conta: ").strip()
        if num.isdigit():
            return int(num)
        print("Entrada inválida. Digite apenas números.")

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
