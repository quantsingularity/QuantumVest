"""Unit tests for ORM models."""

import pytest
from app.models.financial import (
    Asset,
    AssetType,
    RiskLevel,
    Transaction,
    TransactionType,
    User,
    UserRole,
)


class TestUserModel:
    def test_create_user(self, db, test_user):
        assert test_user.id is not None
        assert test_user.email == "test@quantumvest.io"

    def test_password_hashing(self, db, test_user):
        assert test_user.check_password("TestPassword123")
        assert not test_user.check_password("wrongpassword")

    def test_to_dict_excludes_password(self, db, test_user):
        d = test_user.to_dict()
        assert "password_hash" not in d
        assert "id" in d
        assert "email" in d
        assert "role" in d

    def test_default_role_is_client(self, db, test_user):
        assert test_user.role == UserRole.CLIENT

    def test_unique_email_constraint(self, db, test_user):
        duplicate = User(username="other", email="test@quantumvest.io")
        duplicate.set_password("Pass123!")
        db.session.add(duplicate)
        with pytest.raises(Exception):
            db.session.commit()
        db.session.rollback()

    def test_unique_username_constraint(self, db, test_user):
        duplicate = User(username="testuser", email="other@quantumvest.io")
        duplicate.set_password("Pass123!")
        db.session.add(duplicate)
        with pytest.raises(Exception):
            db.session.commit()
        db.session.rollback()


class TestAssetModel:
    def test_create_asset(self, db, sample_asset):
        assert sample_asset.id is not None
        assert sample_asset.symbol == "AAPL"
        assert sample_asset.asset_type == AssetType.STOCK

    def test_to_dict(self, db, sample_asset):
        d = sample_asset.to_dict()
        assert d["symbol"] == "AAPL"
        assert d["asset_type"] == "stock"
        assert d["is_active"] is True

    def test_crypto_asset(self, db):
        btc = Asset(
            symbol="BTC",
            name="Bitcoin",
            asset_type=AssetType.CRYPTO,
            is_active=True,
            is_tradeable=True,
        )
        db.session.add(btc)
        db.session.commit()
        assert btc.asset_type == AssetType.CRYPTO
        assert btc.to_dict()["asset_type"] == "crypto"


class TestPortfolioModel:
    def test_create_portfolio(self, db, sample_portfolio, test_user):
        assert sample_portfolio.id is not None
        assert sample_portfolio.name == "Test Portfolio"
        assert str(sample_portfolio.user_id) == str(test_user.id)

    def test_owner_backref(self, db, sample_portfolio, test_user):
        assert str(sample_portfolio.owner.id) == str(test_user.id)

    def test_to_dict(self, db, sample_portfolio):
        d = sample_portfolio.to_dict()
        assert d["name"] == "Test Portfolio"
        assert "id" in d
        assert "user_id" in d

    def test_risk_level_default(self, db, sample_portfolio):
        assert sample_portfolio.risk_level == RiskLevel.MODERATE

    def test_cash_balance_default(self, db, sample_portfolio):
        assert float(sample_portfolio.cash_balance) == 0.0


class TestTransactionModel:
    def test_create_transaction(self, db, test_user, sample_portfolio, sample_asset):
        tx = Transaction(
            user_id=test_user.id,
            portfolio_id=sample_portfolio.id,
            asset_id=sample_asset.id,
            transaction_type=TransactionType.BUY,
            quantity=10,
            price=150.0,
            total_amount=1500.0,
            fees=5.0,
        )
        db.session.add(tx)
        db.session.commit()
        assert tx.id is not None
        assert tx.transaction_type == TransactionType.BUY
        assert float(tx.quantity) == 10.0
        assert float(tx.price) == 150.0

    def test_to_dict(self, db, test_user, sample_portfolio, sample_asset):
        tx = Transaction(
            user_id=test_user.id,
            portfolio_id=sample_portfolio.id,
            asset_id=sample_asset.id,
            transaction_type=TransactionType.SELL,
            quantity=5,
            price=200.0,
            total_amount=1000.0,
        )
        db.session.add(tx)
        db.session.commit()
        d = tx.to_dict()
        assert d["transaction_type"] == "sell"
        assert d["quantity"] == 5.0
