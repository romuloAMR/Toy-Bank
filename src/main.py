from persistence.account_repository import AccountRepository
from domain.bank_service import BankService
from presentation.bank_cli import BankCLI, run_registration, show_balance, run_deposit

if __name__ == "__main__":
    storage = AccountRepository()
    
    service = BankService(storage)
    
    cli = BankCLI("--- Toy-Bank CLI ---")
    cli.add_option("1", "Criar Conta", run_registration)
    cli.add_option("2", "Ver Saldo", show_balance)
    cli.add_option("3", "Realizar Deposito", run_deposit)
    cli.add_option("0", "Sair", lambda s: False)
    
    cli.run(service)
