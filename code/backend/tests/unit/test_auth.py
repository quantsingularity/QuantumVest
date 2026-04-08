"""Unit tests for the authentication service."""

from app.core.auth import AuthService


class TestEmailValidation:
    def test_valid_emails(self):
        valid = [
            "user@example.com",
            "user.name+tag@sub.domain.org",
            "123@numbers.io",
        ]
        for email in valid:
            assert AuthService.validate_email(email), f"Expected valid: {email}"

    def test_invalid_emails(self):
        invalid = [
            "invalid-email",
            "@example.com",
            "test@",
            "",
        ]
        for email in invalid:
            assert not AuthService.validate_email(email), f"Expected invalid: {email}"


class TestPasswordValidation:
    def test_strong_password(self):
        ok, msg = AuthService.validate_password("StrongPass1")
        assert ok

    def test_too_short(self):
        ok, msg = AuthService.validate_password("Ab1")
        assert not ok
        assert "8" in msg

    def test_no_uppercase(self):
        ok, msg = AuthService.validate_password("lowercase1")
        assert not ok

    def test_no_lowercase(self):
        ok, msg = AuthService.validate_password("UPPERCASE1")
        assert not ok

    def test_no_digit(self):
        ok, msg = AuthService.validate_password("NoDigitPass")
        assert not ok


class TestUserRegistration:
    def test_register_success(self, app, db):
        with app.app_context():
            result = AuthService.register_user(
                username="newuser",
                email="new@quantumvest.io",
                password="SecurePass1",
            )
        assert result["success"]
        assert "access_token" in result
        assert "user" in result

    def test_register_duplicate_email(self, app, db, test_user):
        with app.app_context():
            result = AuthService.register_user(
                username="different",
                email="test@quantumvest.io",
                password="SecurePass1",
            )
        assert not result["success"]
        assert "Email" in result["error"] or "email" in result["error"]

    def test_register_duplicate_username(self, app, db, test_user):
        with app.app_context():
            result = AuthService.register_user(
                username="testuser",
                email="unique@quantumvest.io",
                password="SecurePass1",
            )
        assert not result["success"]

    def test_register_invalid_email(self, app, db):
        with app.app_context():
            result = AuthService.register_user(
                username="validu",
                email="not-an-email",
                password="SecurePass1",
            )
        assert not result["success"]

    def test_register_weak_password(self, app, db):
        with app.app_context():
            result = AuthService.register_user(
                username="weakpwduser",
                email="weakpwd@quantumvest.io",
                password="password",
            )
        assert not result["success"]

    def test_register_short_username(self, app, db):
        with app.app_context():
            result = AuthService.register_user(
                username="ab",
                email="short@quantumvest.io",
                password="SecurePass1",
            )
        assert not result["success"]


class TestUserLogin:
    def test_login_success(self, app, db, test_user):
        with app.app_context():
            result = AuthService.login_user("testuser", "TestPassword123")
        assert result["success"]
        assert "access_token" in result

    def test_login_by_email(self, app, db, test_user):
        with app.app_context():
            result = AuthService.login_user("test@quantumvest.io", "TestPassword123")
        assert result["success"]

    def test_login_wrong_password(self, app, db, test_user):
        with app.app_context():
            result = AuthService.login_user("testuser", "WrongPassword")
        assert not result["success"]

    def test_login_nonexistent_user(self, app, db):
        with app.app_context():
            result = AuthService.login_user("nobody", "SomePass1")
        assert not result["success"]


class TestTokenLifecycle:
    def test_generate_and_verify(self, app, test_user):
        with app.app_context():
            token = AuthService.generate_token(test_user.id)
            user_id = AuthService.verify_token(token)
        assert user_id is not None
        assert str(user_id) == str(test_user.id)

    def test_invalid_token_returns_none(self, app):
        with app.app_context():
            result = AuthService.verify_token("not.a.valid.token")
        assert result is None

    def test_refresh_token_flow(self, app, db, test_user):
        with app.app_context():
            refresh = AuthService.generate_refresh_token(test_user.id)
            result = AuthService.refresh_access_token(refresh)
        assert result["success"]
        assert "access_token" in result
