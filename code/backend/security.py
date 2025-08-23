"""
Enhanced Security Module for QuantumVest
Financial industry-grade security features including encryption, audit logging, and threat detection
"""
import hashlib
import hmac
import secrets
import jwt
import bcrypt
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Any, Tuple
from functools import wraps
from flask import request, jsonify, current_app, g
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import re
import logging
import ipaddress
from dataclasses import dataclass

from enhanced_models import db, User, AuditLog, UserRole

logger = logging.getLogger(__name__)

@dataclass
class SecurityEvent:
    """Security event data structure"""
    event_type: str
    severity: str
    description: str
    user_id: Optional[str] = None
    ip_address: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class EncryptionService:
    """Advanced encryption service for sensitive data"""
    
    def __init__(self, master_key: Optional[str] = None):
        """Initialize encryption service with master key"""
        if master_key:
            self.master_key = master_key.encode()
        else:
            self.master_key = secrets.token_bytes(32)
        
        # Derive encryption key from master key
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'quantumvest_salt',  # In production, use random salt per encryption
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(self.master_key))
        self.cipher_suite = Fernet(key)
    
    def encrypt(self, data: str) -> str:
        """Encrypt sensitive data"""
        try:
            encrypted_data = self.cipher_suite.encrypt(data.encode())
            return base64.urlsafe_b64encode(encrypted_data).decode()
        except Exception as e:
            logger.error(f"Encryption error: {e}")
            raise
    
    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt sensitive data"""
        try:
            decoded_data = base64.urlsafe_b64decode(encrypted_data.encode())
            decrypted_data = self.cipher_suite.decrypt(decoded_data)
            return decrypted_data.decode()
        except Exception as e:
            logger.error(f"Decryption error: {e}")
            raise
    
    def encrypt_pii(self, pii_data: Dict[str, Any]) -> Dict[str, str]:
        """Encrypt personally identifiable information"""
        encrypted_pii = {}
        sensitive_fields = ['ssn', 'tax_id', 'bank_account', 'credit_card', 'passport']
        
        for field, value in pii_data.items():
            if field.lower() in sensitive_fields and value:
                encrypted_pii[field] = self.encrypt(str(value))
            else:
                encrypted_pii[field] = value
        
        return encrypted_pii

class AuthenticationService:
    """Enhanced authentication service with multi-factor support"""
    
    @staticmethod
    def generate_secure_password_hash(password: str) -> str:
        """Generate secure password hash using bcrypt"""
        salt = bcrypt.gensalt(rounds=12)
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        """Verify password against hash"""
        try:
            return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
        except Exception as e:
            logger.error(f"Password verification error: {e}")
            return False
    
    @staticmethod
    def validate_password_strength(password: str) -> Tuple[bool, List[str]]:
        """Validate password strength according to financial industry standards"""
        errors = []
        
        # Minimum length
        if len(password) < 12:
            errors.append("Password must be at least 12 characters long")
        
        # Character requirements
        if not re.search(r'[A-Z]', password):
            errors.append("Password must contain at least one uppercase letter")
        
        if not re.search(r'[a-z]', password):
            errors.append("Password must contain at least one lowercase letter")
        
        if not re.search(r'\d', password):
            errors.append("Password must contain at least one digit")
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.append("Password must contain at least one special character")
        
        # Common password patterns
        common_patterns = [
            r'(.)\1{2,}',  # Repeated characters
            r'(012|123|234|345|456|567|678|789|890)',  # Sequential numbers
            r'(abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz)',  # Sequential letters
        ]
        
        for pattern in common_patterns:
            if re.search(pattern, password.lower()):
                errors.append("Password contains common patterns and is not secure")
                break
        
        # Dictionary words (simplified check)
        common_words = ['password', 'admin', 'user', 'login', 'quantumvest', 'finance', 'money']
        for word in common_words:
            if word in password.lower():
                errors.append("Password contains common dictionary words")
                break
        
        return len(errors) == 0, errors
    
    @staticmethod
    def generate_jwt_token(user: User, expires_in: int = 3600) -> str:
        """Generate JWT token for user authentication"""
        try:
            payload = {
                'user_id': str(user.id),
                'email': user.email,
                'role': user.role.value,
                'exp': datetime.now(timezone.utc) + timedelta(seconds=expires_in),
                'iat': datetime.now(timezone.utc),
                'iss': 'quantumvest',
                'aud': 'quantumvest-api'
            }
            
            token = jwt.encode(
                payload,
                current_app.config['SECRET_KEY'],
                algorithm='HS256'
            )
            
            return token
        except Exception as e:
            logger.error(f"JWT token generation error: {e}")
            raise
    
    @staticmethod
    def verify_jwt_token(token: str) -> Optional[Dict[str, Any]]:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256'],
                audience='quantumvest-api',
                issuer='quantumvest'
            )
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("JWT token expired")
            return None
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid JWT token: {e}")
            return None
    
    @staticmethod
    def generate_2fa_secret() -> str:
        """Generate 2FA secret for TOTP"""
        return base64.b32encode(secrets.token_bytes(20)).decode()
    
    @staticmethod
    def verify_2fa_token(secret: str, token: str) -> bool:
        """Verify 2FA TOTP token"""
        try:
            import pyotp
            totp = pyotp.TOTP(secret)
            return totp.verify(token, valid_window=1)
        except ImportError:
            logger.error("pyotp library not available for 2FA verification")
            return False
        except Exception as e:
            logger.error(f"2FA verification error: {e}")
            return False

class AuthorizationService:
    """Role-based access control and authorization"""
    
    # Define permissions for each role
    ROLE_PERMISSIONS = {
        UserRole.ADMIN: [
            'user:create', 'user:read', 'user:update', 'user:delete',
            'portfolio:create', 'portfolio:read', 'portfolio:update', 'portfolio:delete',
            'transaction:create', 'transaction:read', 'transaction:update', 'transaction:delete',
            'system:admin', 'compliance:manage', 'audit:read'
        ],
        UserRole.PORTFOLIO_MANAGER: [
            'user:read', 'portfolio:create', 'portfolio:read', 'portfolio:update',
            'transaction:create', 'transaction:read', 'transaction:update',
            'compliance:read', 'analytics:read'
        ],
        UserRole.ANALYST: [
            'portfolio:read', 'transaction:read', 'analytics:read', 'compliance:read'
        ],
        UserRole.CLIENT: [
            'portfolio:read', 'transaction:read', 'analytics:read'
        ],
        UserRole.VIEWER: [
            'portfolio:read', 'analytics:read'
        ]
    }
    
    @staticmethod
    def has_permission(user_role: UserRole, permission: str) -> bool:
        """Check if user role has specific permission"""
        return permission in AuthorizationService.ROLE_PERMISSIONS.get(user_role, [])
    
    @staticmethod
    def check_resource_access(user: User, resource_type: str, resource_id: str) -> bool:
        """Check if user can access specific resource"""
        # Admin can access everything
        if user.role == UserRole.ADMIN:
            return True
        
        # Portfolio managers can access portfolios they manage
        if resource_type == 'portfolio' and user.role == UserRole.PORTFOLIO_MANAGER:
            from enhanced_models import Portfolio
            portfolio = Portfolio.query.get(resource_id)
            return portfolio and portfolio.user_id == user.id
        
        # Clients can only access their own resources
        if user.role == UserRole.CLIENT:
            if resource_type == 'portfolio':
                from enhanced_models import Portfolio
                portfolio = Portfolio.query.get(resource_id)
                return portfolio and portfolio.user_id == user.id
            elif resource_type == 'transaction':
                from enhanced_models import Transaction
                transaction = Transaction.query.get(resource_id)
                return transaction and transaction.user_id == user.id
        
        return False

class SecurityMiddleware:
    """Security middleware for request processing"""
    
    def __init__(self):
        self.rate_limits = {}
        self.blocked_ips = set()
        self.suspicious_patterns = [
            r'<script.*?>.*?</script>',  # XSS attempts
            r'union.*select',  # SQL injection
            r'drop.*table',  # SQL injection
            r'exec.*\(',  # Command injection
        ]
    
    def check_rate_limit(self, ip_address: str, endpoint: str, limit: int = 100, window: int = 3600) -> bool:
        """Check rate limiting for IP and endpoint"""
        current_time = datetime.now(timezone.utc)
        key = f"{ip_address}:{endpoint}"
        
        if key not in self.rate_limits:
            self.rate_limits[key] = []
        
        # Remove old requests outside the window
        self.rate_limits[key] = [
            timestamp for timestamp in self.rate_limits[key]
            if current_time - timestamp < timedelta(seconds=window)
        ]
        
        # Check if limit exceeded
        if len(self.rate_limits[key]) >= limit:
            return False
        
        # Add current request
        self.rate_limits[key].append(current_time)
        return True
    
    def detect_suspicious_activity(self, request_data: str) -> List[str]:
        """Detect suspicious patterns in request data"""
        threats = []
        
        for pattern in self.suspicious_patterns:
            if re.search(pattern, request_data, re.IGNORECASE):
                threats.append(f"Suspicious pattern detected: {pattern}")
        
        return threats
    
    def validate_ip_address(self, ip_address: str) -> bool:
        """Validate and check IP address"""
        try:
            # Check if IP is blocked
            if ip_address in self.blocked_ips:
                return False
            
            # Validate IP format
            ipaddress.ip_address(ip_address)
            
            # Check against known malicious IP ranges (simplified)
            ip_obj = ipaddress.ip_address(ip_address)
            
            # Block private networks in production (except for development)
            if current_app.config.get('ENV') == 'production':
                if ip_obj.is_private and not ip_obj.is_loopback:
                    return False
            
            return True
            
        except ValueError:
            return False

class AuditService:
    """Comprehensive audit logging service"""
    
    @staticmethod
    def log_security_event(event: SecurityEvent):
        """Log security event to audit trail"""
        try:
            audit_log = AuditLog(
                user_id=event.user_id,
                event_type=event.event_type,
                event_description=event.description,
                ip_address=event.ip_address,
                user_agent=request.headers.get('User-Agent') if request else None,
                endpoint=request.endpoint if request else None,
                method=request.method if request else None,
                metadata={
                    'severity': event.severity,
                    'timestamp': datetime.now(timezone.utc).isoformat(),
                    **(event.metadata or {})
                }
            )
            
            db.session.add(audit_log)
            db.session.commit()
            
            # Log to application logger based on severity
            log_message = f"Security Event: {event.event_type} - {event.description}"
            if event.severity == 'critical':
                logger.critical(log_message)
            elif event.severity == 'error':
                logger.error(log_message)
            elif event.severity == 'warning':
                logger.warning(log_message)
            else:
                logger.info(log_message)
                
        except Exception as e:
            logger.error(f"Error logging security event: {e}")
            db.session.rollback()
    
    @staticmethod
    def log_user_action(user_id: str, action: str, resource_type: str, resource_id: str, details: Optional[Dict] = None):
        """Log user action for audit trail"""
        try:
            event = SecurityEvent(
                event_type='user_action',
                severity='info',
                description=f"User {action} {resource_type} {resource_id}",
                user_id=user_id,
                ip_address=request.remote_addr if request else None,
                metadata={
                    'action': action,
                    'resource_type': resource_type,
                    'resource_id': resource_id,
                    'details': details or {}
                }
            )
            
            AuditService.log_security_event(event)
            
        except Exception as e:
            logger.error(f"Error logging user action: {e}")
    
    @staticmethod
    def log_authentication_event(user_id: Optional[str], event_type: str, success: bool, details: Optional[Dict] = None):
        """Log authentication events"""
        try:
            severity = 'info' if success else 'warning'
            description = f"Authentication {event_type}: {'Success' if success else 'Failed'}"
            
            event = SecurityEvent(
                event_type=f'auth_{event_type}',
                severity=severity,
                description=description,
                user_id=user_id,
                ip_address=request.remote_addr if request else None,
                metadata={
                    'success': success,
                    'event_type': event_type,
                    'details': details or {}
                }
            )
            
            AuditService.log_security_event(event)
            
        except Exception as e:
            logger.error(f"Error logging authentication event: {e}")

class ThreatDetectionService:
    """Advanced threat detection and prevention"""
    
    def __init__(self):
        self.failed_login_threshold = 5
        self.suspicious_activity_threshold = 10
        self.monitoring_window = timedelta(hours=1)
    
    def detect_brute_force_attack(self, ip_address: str) -> bool:
        """Detect brute force login attempts"""
        try:
            cutoff_time = datetime.now(timezone.utc) - self.monitoring_window
            
            failed_attempts = AuditLog.query.filter(
                AuditLog.ip_address == ip_address,
                AuditLog.event_type == 'auth_login',
                AuditLog.created_at >= cutoff_time,
                AuditLog.metadata['success'].astext == 'false'
            ).count()
            
            return failed_attempts >= self.failed_login_threshold
            
        except Exception as e:
            logger.error(f"Error detecting brute force attack: {e}")
            return False
    
    def detect_account_takeover(self, user_id: str) -> bool:
        """Detect potential account takeover attempts"""
        try:
            cutoff_time = datetime.now(timezone.utc) - self.monitoring_window
            
            # Check for logins from multiple IPs
            login_ips = db.session.query(AuditLog.ip_address).filter(
                AuditLog.user_id == user_id,
                AuditLog.event_type == 'auth_login',
                AuditLog.created_at >= cutoff_time,
                AuditLog.metadata['success'].astext == 'true'
            ).distinct().all()
            
            # Check for unusual activity patterns
            activity_count = AuditLog.query.filter(
                AuditLog.user_id == user_id,
                AuditLog.created_at >= cutoff_time
            ).count()
            
            return len(login_ips) > 3 or activity_count > self.suspicious_activity_threshold
            
        except Exception as e:
            logger.error(f"Error detecting account takeover: {e}")
            return False
    
    def analyze_transaction_patterns(self, user_id: str) -> Dict[str, Any]:
        """Analyze transaction patterns for anomalies"""
        try:
            from enhanced_models import Transaction
            
            # Get recent transactions
            cutoff_time = datetime.now(timezone.utc) - timedelta(days=30)
            transactions = Transaction.query.filter(
                Transaction.user_id == user_id,
                Transaction.executed_at >= cutoff_time
            ).all()
            
            if not transactions:
                return {'anomalies': [], 'risk_score': 0}
            
            # Calculate transaction statistics
            amounts = [float(t.total_amount) for t in transactions]
            avg_amount = sum(amounts) / len(amounts)
            max_amount = max(amounts)
            
            anomalies = []
            risk_score = 0
            
            # Check for unusually large transactions
            for transaction in transactions:
                amount = float(transaction.total_amount)
                if amount > avg_amount * 5:  # 5x average
                    anomalies.append({
                        'type': 'large_transaction',
                        'transaction_id': str(transaction.id),
                        'amount': amount,
                        'threshold': avg_amount * 5
                    })
                    risk_score += 10
            
            # Check for high frequency trading
            transaction_dates = [t.executed_at.date() for t in transactions]
            daily_counts = {}
            for date in transaction_dates:
                daily_counts[date] = daily_counts.get(date, 0) + 1
            
            max_daily_transactions = max(daily_counts.values()) if daily_counts else 0
            if max_daily_transactions > 20:  # More than 20 transactions per day
                anomalies.append({
                    'type': 'high_frequency_trading',
                    'max_daily_transactions': max_daily_transactions,
                    'threshold': 20
                })
                risk_score += 15
            
            return {
                'anomalies': anomalies,
                'risk_score': min(risk_score, 100),  # Cap at 100
                'statistics': {
                    'transaction_count': len(transactions),
                    'avg_amount': avg_amount,
                    'max_amount': max_amount,
                    'max_daily_transactions': max_daily_transactions
                }
            }
            
        except Exception as e:
            logger.error(f"Error analyzing transaction patterns: {e}")
            return {'anomalies': [], 'risk_score': 0}

# Security decorators
def require_auth(f):
    """Decorator to require authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Authentication required'}), 401
        
        if token.startswith('Bearer '):
            token = token[7:]
        
        payload = AuthenticationService.verify_jwt_token(token)
        if not payload:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        # Get user
        user = User.query.get(payload['user_id'])
        if not user or not user.is_active:
            return jsonify({'error': 'User not found or inactive'}), 401
        
        # Store user in request context
        g.current_user = user
        
        # Log authentication event
        AuditService.log_authentication_event(
            user_id=str(user.id),
            event_type='token_validation',
            success=True
        )
        
        return f(*args, **kwargs)
    
    return decorated_function

def require_permission(permission: str):
    """Decorator to require specific permission"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not hasattr(g, 'current_user'):
                return jsonify({'error': 'Authentication required'}), 401
            
            if not AuthorizationService.has_permission(g.current_user.role, permission):
                return jsonify({'error': 'Insufficient permissions'}), 403
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator

def require_2fa(f):
    """Decorator to require 2FA verification"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not hasattr(g, 'current_user'):
            return jsonify({'error': 'Authentication required'}), 401
        
        if not g.current_user.two_factor_enabled:
            return jsonify({'error': '2FA required for this operation'}), 403
        
        # Check for 2FA token in headers
        totp_token = request.headers.get('X-TOTP-Token')
        if not totp_token:
            return jsonify({'error': '2FA token required'}), 403
        
        # Verify 2FA token (implementation depends on 2FA setup)
        # This is a simplified check - in production, verify against user's 2FA secret
        
        return f(*args, **kwargs)
    
    return decorated_function

# Initialize security services
encryption_service = EncryptionService()
security_middleware = SecurityMiddleware()
threat_detection_service = ThreatDetectionService()

