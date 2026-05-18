from persistence.account_repository import AccountRepository
from domain.bank_service import BankService
from presentation.bank_cli import (
    BankCLI,
    run_registration,
    run_render_interest,
    run_deposit,
    run_transfer,
    run_withdrawal,
    show_balance,
)

if __name__ == "__main__":
    storage = AccountRepository()
    
    service = BankService(storage)
    
    cli = BankCLI("--- Toy-Bank CLI ---")
    cli.add_option("1", "Criar Conta", run_registration)
    cli.add_option("2", "Ver Saldo", show_balance)
    cli.add_option("3", "Realizar Deposito", run_deposit)
    cli.add_option("4", "Realizar Saque", run_withdrawal)
    cli.add_option("5", "Realizar Transferência", run_transfer)
    cli.add_option("6", "Render Juros", run_render_interest)
    cli.add_option("0", "Sair", lambda s: False)
    
    cli.run(service)
