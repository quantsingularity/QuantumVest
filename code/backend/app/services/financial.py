"""
Financial services: compliance checking, alert management, performance analytics.
"""

import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import numpy as np
from app.extensions import db
from app.models.financial import Alert, ComplianceStatus, Portfolio, PortfolioHolding

logger = logging.getLogger(__name__)


@dataclass
class PerformanceMetrics:
    total_return: float
    annualized_return: float
    volatility: float
    sharpe_ratio: float
    alpha: float
    beta: float
    max_drawdown: float
    calmar_ratio: float
    sortino_ratio: float


class PerformanceAnalyticsService:
    """Portfolio performance analytics."""

    @staticmethod
    def compute(
        values: List[float], risk_free_rate: float = 0.02
    ) -> PerformanceMetrics:
        if len(values) < 2:
            return PerformanceMetrics(0, 0, 0, 0, 0, 1.0, 0, 0, 0)

        arr = np.array(values, dtype=float)
        denom = np.where(arr[:-1] != 0, arr[:-1], 1)
        daily = np.diff(arr) / denom
        ann_ret = float(np.mean(daily) * 252)
        ann_vol = float(np.std(daily) * np.sqrt(252))
        total = float((arr[-1] - arr[0]) / arr[0] * 100) if arr[0] != 0 else 0
        sharpe = (ann_ret - risk_free_rate) / ann_vol if ann_vol > 0 else 0.0

        down = daily[daily < 0]
        down_dev = float(np.std(down) * np.sqrt(252)) if len(down) > 0 else 0.0
        sortino = ann_ret / down_dev if down_dev > 0 else float("inf")

        peak = np.maximum.accumulate(arr)
        dd = (arr - peak) / np.where(peak != 0, peak, 1)
        max_dd = float(np.min(dd))
        calmar = ann_ret / abs(max_dd) if max_dd != 0 else float("inf")

        return PerformanceMetrics(
            total_return=total,
            annualized_return=ann_ret,
            volatility=ann_vol,
            sharpe_ratio=sharpe,
            alpha=0.0,
            beta=1.0,
            max_drawdown=max_dd,
            calmar_ratio=calmar,
            sortino_ratio=sortino,
        )


class ComplianceService:
    """Regulatory compliance checks for portfolios."""

    @staticmethod
    def check_portfolio_compliance(portfolio_id: str) -> Dict[str, Any]:
        try:
            portfolio = db.session.get(Portfolio, portfolio_id)
            if not portfolio:
                return {"success": False, "error": "Portfolio not found"}

            holdings = PortfolioHolding.query.filter_by(portfolio_id=portfolio_id).all()
            results = {
                "overall_status": ComplianceStatus.COMPLIANT,
                "checks": [],
                "violations": [],
            }

            # Concentration check
            total_val = sum(float(h.market_value or 0) for h in holdings)
            if total_val > 0:
                for h in holdings:
                    w = float(h.market_value or 0) / total_val
                    if w > 0.30:
                        results["violations"].append(
                            {
                                "type": "concentration",
                                "message": f"Single position exceeds 30% threshold ({w:.1%})",
                            }
                        )
                        results["overall_status"] = ComplianceStatus.NON_COMPLIANT

            # Diversification check
            if len(holdings) < 5:
                results["checks"].append(
                    {
                        "type": "diversification",
                        "status": "warning",
                        "message": "Portfolio has fewer than 5 holdings",
                    }
                )

            results["overall_status"] = results["overall_status"].value
            return {"success": True, "compliance": results}
        except Exception as exc:
            logger.error("Compliance check error: %s", exc)
            return {"success": False, "error": str(exc)}


class AlertService:
    """User alert creation and management."""

    @staticmethod
    def create_alert(
        user_id: str,
        title: str,
        message: str,
        alert_type: str,
        severity: str = "info",
        meta: Optional[Dict[str, Any]] = None,
    ) -> Optional[Alert]:
        try:
            alert = Alert(
                user_id=user_id,
                title=title,
                message=message,
                alert_type=alert_type,
                severity=severity,
                meta_data=meta,
            )
            db.session.add(alert)
            db.session.commit()
            return alert
        except Exception as exc:
            db.session.rollback()
            logger.error("Failed to create alert: %s", exc)
            return None

    @staticmethod
    def get_user_alerts(
        user_id: str, unread_only: bool = False, limit: int = 50
    ) -> List[Dict[str, Any]]:
        try:
            q = Alert.query.filter_by(user_id=user_id, is_dismissed=False)
            if unread_only:
                q = q.filter_by(is_read=False)
            alerts = q.order_by(Alert.created_at.desc()).limit(limit).all()
            return [
                {
                    "id": str(a.id),
                    "title": a.title,
                    "message": a.message,
                    "alert_type": a.alert_type,
                    "severity": a.severity,
                    "is_read": a.is_read,
                    "created_at": a.created_at.isoformat() if a.created_at else None,
                }
                for a in alerts
            ]
        except Exception as exc:
            logger.error("Failed to get alerts: %s", exc)
            return []
