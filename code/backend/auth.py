"""
Authentication Module for QuantumVest
JWT-based authentication with role-based access control
"""

import re
from datetime import datetime, timedelta, timezone
from functools import wraps
import jwt
from flask import current_app, jsonify, request
from models import User, db


class AuthService:
    """Authentication service for user management"""

    @staticmethod
    def generate_token(user_id: Any, expires_in: Any = 24) -> Any:
        """Generate JWT token for user"""
        payload = {
            "user_id": str(user_id),
            "exp": datetime.now(timezone.utc) + timedelta(hours=expires_in),
            "iat": datetime.now(timezone.utc),
            "type": "access",
        }
        return jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")

    @staticmethod
    def generate_refresh_token(user_id: Any, expires_in: Any = 168) -> Any:
        """Generate refresh token for user"""
        payload = {
            "user_id": str(user_id),
            "exp": datetime.now(timezone.utc) + timedelta(hours=expires_in),
            "iat": datetime.now(timezone.utc),
            "type": "refresh",
        }
        return jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")

    @staticmethod
    def verify_token(token: Any) -> Any:
        """Verify JWT token and return user_id"""
        try:
            payload = jwt.decode(
                token, current_app.config["SECRET_KEY"], algorithms=["HS256"]
            )
            return payload["user_id"]
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    @staticmethod
    def validate_email(email: Any) -> Any:
        """Validate email format"""
        pattern = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
        return re.match(pattern, email) is not None

    @staticmethod
    def validate_password(password: Any) -> Any:
        """Validate password strength"""
        if len(password) < 8:
            return (False, "Password must be at least 8 characters long")
        if not re.search("[A-Z]", password):
            return (False, "Password must contain at least one uppercase letter")
        if not re.search("[a-z]", password):
            return (False, "Password must contain at least one lowercase letter")
        if not re.search("\\d", password):
            return (False, "Password must contain at least one digit")
        return (True, "Password is valid")

    @staticmethod
    def register_user(
        username: Any,
        email: Any,
        password: Any,
        first_name: Any = None,
        last_name: Any = None,
    ) -> Any:
        """Register a new user"""
        try:
            if not username or len(username) < 3:
                return {
                    "success": False,
                    "error": "Username must be at least 3 characters long",
                }
            if not AuthService.validate_email(email):
                return {"success": False, "error": "Invalid email format"}
            is_valid, message = AuthService.validate_password(password)
            if not is_valid:
                return {"success": False, "error": message}
            if User.query.filter_by(username=username).first():
                return {"success": False, "error": "Username already exists"}
            if User.query.filter_by(email=email).first():
                return {"success": False, "error": "Email already registered"}
            user = User(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
            )
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            access_token = AuthService.generate_token(user.id)
            refresh_token = AuthService.generate_refresh_token(user.id)
            return {
                "success": True,
                "user": user.to_dict(),
                "access_token": access_token,
                "refresh_token": refresh_token,
            }
        except Exception as e:
            db.session.rollback()
            return {"success": False, "error": str(e)}

    @staticmethod
    def login_user(username_or_email: Any, password: Any) -> Any:
        """Authenticate user login"""
        try:
            user = User.query.filter(
                (User.username == username_or_email) | (User.email == username_or_email)
            ).first()
            if not user:
                return {"success": False, "error": "Invalid credentials"}
            if not user.check_password(password):
                return {"success": False, "error": "Invalid credentials"}
            if not user.is_active:
                return {"success": False, "error": "Account is deactivated"}
            user.last_login = datetime.now(timezone.utc)
            db.session.commit()
            access_token = AuthService.generate_token(user.id)
            refresh_token = AuthService.generate_refresh_token(user.id)
            return {
                "success": True,
                "user": user.to_dict(),
                "access_token": access_token,
                "refresh_token": refresh_token,
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def refresh_access_token(refresh_token: Any) -> Any:
        """Refresh access token using refresh token"""
        try:
            payload = jwt.decode(
                refresh_token, current_app.config["SECRET_KEY"], algorithms=["HS256"]
            )
            if payload.get("type") != "refresh":
                return {"success": False, "error": "Invalid token type"}
            user_id = payload["user_id"]
            user = User.query.get(user_id)
            if not user or not user.is_active:
                return {"success": False, "error": "User not found or inactive"}
            access_token = AuthService.generate_token(user.id)
            return {"success": True, "access_token": access_token}
        except jwt.ExpiredSignatureError:
            return {"success": False, "error": "Refresh token expired"}
        except jwt.InvalidTokenError:
            return {"success": False, "error": "Invalid refresh token"}
        except Exception as e:
            return {"success": False, "error": str(e)}


def token_required(f: Any) -> Any:
    """Decorator to require valid JWT token"""

    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            auth_header = request.headers["Authorization"]
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return (jsonify({"error": "Invalid token format"}), 401)
        if not token:
            return (jsonify({"error": "Token is missing"}), 401)
        try:
            user_id = AuthService.verify_token(token)
            if not user_id:
                return (jsonify({"error": "Token is invalid or expired"}), 401)
            current_user = User.query.get(user_id)
            if not current_user or not current_user.is_active:
                return (jsonify({"error": "User not found or inactive"}), 401)
        except Exception:
            return (jsonify({"error": "Token verification failed"}), 401)
        return f(current_user, *args, **kwargs)

    return decorated


def admin_required(f: Any) -> Any:
    """Decorator to require admin privileges"""

    @wraps(f)
    def decorated(current_user, *args, **kwargs):
        if current_user.subscription_tier != "admin":
            return (jsonify({"error": "Admin privileges required"}), 403)
        return f(current_user, *args, **kwargs)

    return decorated


def premium_required(f: Any) -> Any:
    """Decorator to require premium subscription"""

    @wraps(f)
    def decorated(current_user, *args, **kwargs):
        if current_user.subscription_tier not in ["premium", "professional", "admin"]:
            return (jsonify({"error": "Premium subscription required"}), 403)
        return f(current_user, *args, **kwargs)

    return decorated


class RateLimiter:
    """Simple in-memory rate limiter"""

    def __init__(self) -> Any:
        self.requests = {}

    def is_allowed(self, key: Any, limit: Any, window: Any) -> Any:
        """Check if request is allowed based on rate limit"""
        now = datetime.now(timezone.utc)
        if key not in self.requests:
            self.requests[key] = []
        self.requests[key] = [
            req_time
            for req_time in self.requests[key]
            if now - req_time < timedelta(seconds=window)
        ]
        if len(self.requests[key]) >= limit:
            return False
        self.requests[key].append(now)
        return True


rate_limiter = RateLimiter()


def rate_limit(limit: Any = 100, window: Any = 3600) -> Any:
    """Decorator for rate limiting"""

    def decorator(f):

        @wraps(f)
        def decorated(*args, **kwargs):
            key = request.remote_addr
            if not rate_limiter.is_allowed(key, limit, window):
                return (
                    jsonify(
                        {
                            "error": "Rate limit exceeded",
                            "limit": limit,
                            "window": window,
                        }
                    ),
                    429,
                )
            return f(*args, **kwargs)

        return decorated

    return decorator
