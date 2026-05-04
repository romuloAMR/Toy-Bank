import sys
from collections import OrderedDict


def prompt_account_number() -> str:
    while True:
        try:
            num = input("Digite o número da conta: ").strip()
            if not num:
                print("Número vazio. Tente novamente.")
                continue
            return num
        except (EOFError, KeyboardInterrupt):
            print("\nOperação cancelada.")
            sys.exit(0)


def run_registration(store):
    acc = prompt_account_number()
    created = store.create_account(acc)
    if created:
        print(f"Conta {acc} criada com saldo 0.00")
    else:
        balance = store.get_balance(acc)
        print(f"Conta {acc} já existe. Saldo atual: {balance:.2f}")


def show_balance(store):
    acc = prompt_account_number()
    bal = store.get_balance(acc)
    if bal is None:
        print(f"Conta {acc} não encontrada.")
    else:
        print(f"Saldo da conta {acc}: {bal:.2f}")


class Menu:
    def __init__(self, title: str = None):
        self.title = title or ""
        self._options = OrderedDict()

    def add_option(self, key: str, label: str, handler):
        self._options[str(key)] = (label, handler)

    def display(self):
        if self.title:
            print(f"\n{self.title}")
        for key, (label, _) in self._options.items():
            print(f"{key}) {label}")

    def run(self, store):
        try:
            while True:
                self.display()
                choice = input("Escolha uma opção: ").strip()
                if choice in self._options:
                    _, handler = self._options[choice]
                    result = handler(store)
                    if result is False:
                        break
                else:
                    print("Opção inválida. Tente novamente.")
        except (EOFError, KeyboardInterrupt):
            print("\nOperação cancelada. Saindo...")
            sys.exit(0)


def run_cli(store):
    menu = Menu("--- Toy-Bank ---")
    menu.add_option("1", "Criar conta", run_registration)
    menu.add_option("2", "Consultar saldo", show_balance)
    menu.add_option("0", "Sair", lambda s: False)
    menu.run(store)
