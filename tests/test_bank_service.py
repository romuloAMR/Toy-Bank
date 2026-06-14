import pytest
from unittest.mock import MagicMock
from src.domain.bank_service import BankService
from src.domain.account_types import DEFAULT_ACCOUNT_TYPE, BONUS_ACCOUNT_TYPE, SAVINGS_ACCOUNT_TYPE


@pytest.fixture
def mock_repo():
    return MagicMock()


@pytest.fixture
def service(mock_repo):
    return BankService(mock_repo)


# ─── Cadastrar Conta ───────────────────────────────────────────────────────────

class TestRegisterAccount:

    def test_cadastrar_conta_simples(self, service, mock_repo):
        mock_repo.create_account.return_value = True
        balance, success = service.register_account(1, DEFAULT_ACCOUNT_TYPE)
        assert success is True
        assert balance == 0.0

    def test_cadastrar_conta_bonus(self, service, mock_repo):
        mock_repo.create_account.return_value = True
        balance, success = service.register_account(2, BONUS_ACCOUNT_TYPE)
        assert success is True
        assert balance == 0.0

    def test_cadastrar_conta_poupanca_com_saldo_inicial(self, service, mock_repo):
        mock_repo.create_account.return_value = True
        balance, success = service.register_account(3, SAVINGS_ACCOUNT_TYPE, opening_balance=500.0)
        assert success is True
        assert balance == 500.0

    def test_cadastrar_conta_ja_existente(self, service, mock_repo):
        mock_repo.create_account.return_value = False
        mock_repo.get_balance.return_value = 100.0
        balance, success = service.register_account(1, DEFAULT_ACCOUNT_TYPE)
        assert success is False
        assert balance == 100.0


# ─── Consultar Conta ───────────────────────────────────────────────────────────

class TestGetAccount:

    def test_consultar_conta_simples(self, service, mock_repo):
        mock_repo.get_balance.return_value = 100.0
        mock_repo.get_account_type.return_value = DEFAULT_ACCOUNT_TYPE
        mock_repo.get_points.return_value = None
        balance, exists = service.check_balance(1)
        account_type = service.get_account_type(1)
        points = service.get_points(1)
        assert exists is True
        assert balance == 100.0
        assert account_type == DEFAULT_ACCOUNT_TYPE
        assert points is None

    def test_consultar_conta_bonus(self, service, mock_repo):
        mock_repo.get_balance.return_value = 200.0
        mock_repo.get_account_type.return_value = BONUS_ACCOUNT_TYPE
        mock_repo.get_points.return_value = 10
        balance, exists = service.check_balance(2)
        account_type = service.get_account_type(2)
        points = service.get_points(2)
        assert exists is True
        assert balance == 200.0
        assert account_type == BONUS_ACCOUNT_TYPE
        assert points == 10

    def test_consultar_conta_poupanca(self, service, mock_repo):
        mock_repo.get_balance.return_value = 500.0
        mock_repo.get_account_type.return_value = SAVINGS_ACCOUNT_TYPE
        mock_repo.get_points.return_value = None
        balance, exists = service.check_balance(3)
        account_type = service.get_account_type(3)
        points = service.get_points(3)
        assert exists is True
        assert balance == 500.0
        assert account_type == SAVINGS_ACCOUNT_TYPE
        assert points is None

    def test_consultar_conta_inexistente(self, service, mock_repo):
        mock_repo.get_balance.return_value = None
        balance, exists = service.check_balance(99)
        assert exists is False
        assert balance is None


# ─── Consultar Saldo ───────────────────────────────────────────────────────────

class TestCheckBalance:

    def test_consultar_saldo_conta_existente(self, service, mock_repo):
        mock_repo.get_balance.return_value = 250.0
        balance, exists = service.check_balance(1)
        assert exists is True
        assert balance == 250.0

    def test_consultar_saldo_conta_inexistente(self, service, mock_repo):
        mock_repo.get_balance.return_value = None
        balance, exists = service.check_balance(99)
        assert exists is False
        assert balance is None


# ─── Crédito ───────────────────────────────────────────────────────────────────

class TestMakeDeposit:

    def test_credito_caso_normal(self, service, mock_repo):
        mock_repo.account_exists.return_value = True
        mock_repo.get_balance.return_value = 150.0
        mock_repo.get_account_type.return_value = DEFAULT_ACCOUNT_TYPE
        balance, msg = service.make_deposit(1, 100.0)
        assert msg == "Sucesso"
        assert balance == 150.0

    def test_credito_valor_negativo(self, service, mock_repo):
        balance, msg = service.make_deposit(1, -50.0)
        assert balance is None
        assert msg == "Valor deve ser maior que zero"

    def test_credito_valor_zero(self, service, mock_repo):
        balance, msg = service.make_deposit(1, 0.0)
        assert balance is None
        assert msg == "Valor deve ser maior que zero"

    def test_credito_bonificacao_conta_bonus(self, service, mock_repo):
        mock_repo.account_exists.return_value = True
        mock_repo.get_account_type.return_value = BONUS_ACCOUNT_TYPE
        mock_repo.get_balance.return_value = 600.0
        balance, msg = service.make_deposit(2, 500.0)
        # 500 // 100 = 5 pontos
        assert "5 ponto(s) ganhos" in msg
        mock_repo.add_points.assert_called_once_with(2, 5)


# ─── Débito ────────────────────────────────────────────────────────────────────

class TestMakeWithdrawal:

    def test_debito_caso_normal(self, service, mock_repo):
        mock_repo.get_balance.side_effect = [500.0, 400.0]
        mock_repo.get_account_type.return_value = DEFAULT_ACCOUNT_TYPE
        balance, msg = service.make_withdrawal(1, 100.0)
        assert msg == "Sucesso"
        assert balance == 400.0

    def test_debito_valor_negativo(self, service, mock_repo):
        balance, msg = service.make_withdrawal(1, -50.0)
        assert balance is None
        assert msg == "Valor deve ser maior que zero"

    def test_debito_limite_negativo_conta_simples(self, service, mock_repo):
        mock_repo.get_balance.return_value = 0.0
        mock_repo.get_account_type.return_value = DEFAULT_ACCOUNT_TYPE
        balance, msg = service.make_withdrawal(1, 1001.0)
        assert balance is None
        assert msg == "Limite excedido"

    def test_debito_limite_negativo_conta_bonus(self, service, mock_repo):
        mock_repo.get_balance.return_value = 0.0
        mock_repo.get_account_type.return_value = BONUS_ACCOUNT_TYPE
        balance, msg = service.make_withdrawal(2, 1001.0)
        assert balance is None
        assert msg == "Limite excedido"

    def test_debito_saldo_insuficiente_conta_poupanca(self, service, mock_repo):
        mock_repo.get_balance.return_value = 100.0
        mock_repo.get_account_type.return_value = SAVINGS_ACCOUNT_TYPE
        balance, msg = service.make_withdrawal(3, 200.0)
        assert balance is None
        assert msg == "Saldo insuficiente"


# ─── Transferência ─────────────────────────────────────────────────────────────

class TestMakeTransfer:

    def test_transferencia_valor_negativo(self, service, mock_repo):
        balance_o, balance_d, msg = service.make_transfer(1, 2, -100.0)
        assert msg == "Valor deve ser maior que zero"

    def test_transferencia_limite_negativo_conta_simples(self, service, mock_repo):
        mock_repo.get_balance.side_effect = [0.0, 500.0]
        mock_repo.get_account_type.return_value = DEFAULT_ACCOUNT_TYPE
        balance_o, balance_d, msg = service.make_transfer(1, 2, 1001.0)
        assert msg == "Limite excedido"

    def test_transferencia_saldo_insuficiente_conta_poupanca(self, service, mock_repo):
        mock_repo.get_balance.side_effect = [100.0, 500.0]
        mock_repo.get_account_type.return_value = SAVINGS_ACCOUNT_TYPE
        balance_o, balance_d, msg = service.make_transfer(3, 2, 200.0)
        assert msg == "Saldo insuficiente"

    def test_transferencia_bonificacao_conta_bonus_destino(self, service, mock_repo):
        mock_repo.get_balance.side_effect = [500.0, 200.0, 300.0, 600.0]
        mock_repo.get_account_type.side_effect = [DEFAULT_ACCOUNT_TYPE, BONUS_ACCOUNT_TYPE]
        mock_repo.deposit.return_value = True
        balance_o, balance_d, msg = service.make_transfer(1, 2, 400.0)
        # 400 // 200 = 2 pontos
        assert "2 ponto(s) ganhos" in msg


# ─── Render Juros ──────────────────────────────────────────────────────────────

class TestRenderInterest:

    def test_render_juros_correto(self, service, mock_repo):
        mock_repo.apply_interest_to_savings_accounts.return_value = 3
        updated, msg = service.render_interest(10.0)
        assert updated == 3
        assert msg == "Sucesso"

    def test_render_juros_taxa_invalida(self, service, mock_repo):
        updated, msg = service.render_interest(-1.0)
        assert updated == 0