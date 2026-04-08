"""
Portfolio management service: CRUD, transaction processing, performance analytics, optimization.
"""

import logging
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from typing import Any, Dict, Optional

import numpy as np
import pandas as pd
from app.extensions import db
from app.models.financial import (
    Asset,
    Portfolio,
    PortfolioHolding,
    PortfolioPerformance,
    PriceData,
    Transaction,
    TransactionType,
)
from sqlalchemy import and_

logger = logging.getLogger(__name__)


class PortfolioService:
    """Service for portfolio management and analytics."""

    @staticmethod
    def create_portfolio(
        user_id: str,
        name: str,
        description: Optional[str] = None,
        currency: str = "USD",
        is_default: bool = False,
    ) -> Dict[str, Any]:
        try:
            if is_default:
                existing = Portfolio.query.filter_by(
                    user_id=user_id, is_default=True
                ).first()
                if existing:
                    existing.is_default = False

            portfolio = Portfolio(
                user_id=user_id,
                name=name,
                description=description,
                currency=currency,
                is_default=is_default,
            )
            db.session.add(portfolio)
            db.session.commit()
            return {"success": True, "portfolio": portfolio.to_dict()}
        except Exception as exc:
            db.session.rollback()
            logger.error("Error creating portfolio: %s", exc)
            return {"success": False, "error": str(exc)}

    @staticmethod
    def delete_portfolio(portfolio_id: str, user_id: str) -> Dict[str, Any]:
        try:
            portfolio = Portfolio.query.filter_by(
                id=portfolio_id, user_id=user_id
            ).first()
            if not portfolio:
                return {"success": False, "error": "Portfolio not found"}
            db.session.delete(portfolio)
            db.session.commit()
            return {"success": True, "message": "Portfolio deleted successfully"}
        except Exception as exc:
            db.session.rollback()
            logger.error("Error deleting portfolio: %s", exc)
            return {"success": False, "error": str(exc)}

    @staticmethod
    def get_user_portfolios(user_id: str) -> Dict[str, Any]:
        try:
            portfolios = Portfolio.query.filter_by(
                user_id=user_id, is_active=True
            ).all()
            result = []
            for p in portfolios:
                d = p.to_dict()
                d["holdings_count"] = PortfolioHolding.query.filter_by(
                    portfolio_id=p.id
                ).count()
                result.append(d)
            return {"success": True, "portfolios": result}
        except Exception as exc:
            logger.error("Error getting user portfolios: %s", exc)
            return {"success": False, "error": str(exc)}

    @staticmethod
    def get_portfolio_details(portfolio_id: str, user_id: str) -> Dict[str, Any]:
        try:
            portfolio = Portfolio.query.filter_by(
                id=portfolio_id, user_id=user_id
            ).first()
            if not portfolio:
                return {"success": False, "error": "Portfolio not found"}

            rows = (
                db.session.query(PortfolioHolding, Asset)
                .join(Asset, PortfolioHolding.asset_id == Asset.id)
                .filter(PortfolioHolding.portfolio_id == portfolio_id)
                .all()
            )

            holdings_data = []
            total_value = Decimal("0")

            for holding, asset in rows:
                latest_price = PortfolioService._get_latest_price(asset.id)
                if latest_price:
                    holding.current_price = latest_price
                    holding.market_value = holding.quantity * latest_price
                    holding.unrealized_pnl = holding.market_value - (
                        holding.quantity * holding.average_cost
                    )
                    if holding.average_cost and holding.average_cost > 0:
                        holding.unrealized_pnl_percent = float(
                            (holding.current_price - holding.average_cost)
                            / holding.average_cost
                            * 100
                        )
                    total_value += holding.market_value or Decimal("0")

                h_dict = holding.to_dict()
                h_dict["asset"] = asset.to_dict()
                holdings_data.append(h_dict)

            portfolio.total_value = total_value
            for h in holdings_data:
                h["current_allocation"] = (
                    float(Decimal(str(h["market_value"])) / total_value * 100)
                    if total_value > 0
                    else 0
                )

            db.session.commit()
            d = portfolio.to_dict()
            d["holdings"] = holdings_data
            d["total_value"] = float(total_value)
            return {"success": True, "portfolio": d}
        except Exception as exc:
            db.session.rollback()
            logger.error("Error getting portfolio details: %s", exc)
            return {"success": False, "error": str(exc)}

    @staticmethod
    def add_transaction(
        portfolio_id: str,
        user_id: str,
        asset_symbol: str,
        transaction_type: str,
        quantity: float,
        price: float,
        fees: float = 0,
        notes: Optional[str] = None,
    ) -> Dict[str, Any]:
        try:
            portfolio = Portfolio.query.filter_by(
                id=portfolio_id, user_id=user_id
            ).first()
            if not portfolio:
                return {"success": False, "error": "Portfolio not found"}

            asset = Asset.query.filter_by(symbol=asset_symbol.upper()).first()
            if not asset:
                return {"success": False, "error": f"Asset {asset_symbol} not found"}

            try:
                trans_type = TransactionType[transaction_type.upper()]
            except KeyError:
                return {
                    "success": False,
                    "error": f"Invalid transaction type: {transaction_type}",
                }

            qty = Decimal(str(quantity))
            px = Decimal(str(price))
            fee = Decimal(str(fees))
            total_amount = qty * px + fee

            transaction = Transaction(
                user_id=user_id,
                portfolio_id=portfolio_id,
                asset_id=asset.id,
                transaction_type=trans_type,
                quantity=qty,
                price=px,
                total_amount=total_amount,
                fees=fee,
                notes=notes,
            )
            db.session.add(transaction)

            holding = PortfolioHolding.query.filter_by(
                portfolio_id=portfolio_id, asset_id=asset.id
            ).first()

            if trans_type == TransactionType.BUY:
                cost_basis = qty * px
                if holding:
                    old_cost = holding.quantity * holding.average_cost
                    holding.quantity += qty
                    holding.average_cost = (old_cost + cost_basis) / holding.quantity
                else:
                    holding = PortfolioHolding(
                        portfolio_id=portfolio_id,
                        asset_id=asset.id,
                        quantity=qty,
                        average_cost=px,
                    )
                    db.session.add(holding)

            elif trans_type == TransactionType.SELL:
                if not holding or holding.quantity < qty:
                    return {"success": False, "error": "Insufficient holdings to sell"}
                realized_pnl = (px - holding.average_cost) * qty
                transaction.realized_pnl = realized_pnl
                portfolio.realized_pnl = (
                    portfolio.realized_pnl or Decimal("0")
                ) + realized_pnl
                holding.quantity -= qty
                if holding.quantity <= Decimal("0"):
                    db.session.delete(holding)

            db.session.commit()
            return {"success": True, "transaction": transaction.to_dict()}
        except Exception as exc:
            db.session.rollback()
            logger.error("Error adding transaction: %s", exc)
            return {"success": False, "error": str(exc)}

    @staticmethod
    def get_transactions(
        portfolio_id: str, user_id: str, page: int = 1, per_page: int = 20
    ) -> Dict[str, Any]:
        try:
            portfolio = Portfolio.query.filter_by(
                id=portfolio_id, user_id=user_id
            ).first()
            if not portfolio:
                return {"success": False, "error": "Portfolio not found"}

            paginated = (
                Transaction.query.filter_by(portfolio_id=portfolio_id)
                .order_by(Transaction.executed_at.desc())
                .paginate(page=page, per_page=per_page, error_out=False)
            )
            return {
                "success": True,
                "transactions": [t.to_dict() for t in paginated.items],
                "total": paginated.total,
                "pages": paginated.pages,
                "page": page,
                "per_page": per_page,
            }
        except Exception as exc:
            logger.error("Error getting transactions: %s", exc)
            return {"success": False, "error": str(exc)}

    @staticmethod
    def get_portfolio_performance(
        portfolio_id: str, user_id: str, days: int = 30
    ) -> Dict[str, Any]:
        try:
            portfolio = Portfolio.query.filter_by(
                id=portfolio_id, user_id=user_id
            ).first()
            if not portfolio:
                return {"success": False, "error": "Portfolio not found"}

            end_date = datetime.now(timezone.utc)
            start_date = end_date - timedelta(days=days)

            perf_records = (
                PortfolioPerformance.query.filter(
                    and_(
                        PortfolioPerformance.portfolio_id == portfolio_id,
                        PortfolioPerformance.timestamp >= start_date,
                        PortfolioPerformance.timestamp <= end_date,
                    )
                )
                .order_by(PortfolioPerformance.timestamp)
                .all()
            )

            if not perf_records:
                current_value = PortfolioService._calculate_current_value(portfolio_id)
                return {
                    "success": True,
                    "performance": {
                        "current_value": float(current_value),
                        "total_return": 0,
                        "total_return_percentage": 0,
                        "daily_returns": [],
                        "volatility": 0,
                        "sharpe_ratio": 0,
                        "max_drawdown": 0,
                    },
                }

            values = [float(p.total_value) for p in perf_records]
            dates = [p.timestamp.isoformat() for p in perf_records]

            if len(values) > 1:
                arr = np.array(values)
                denom = np.where(arr[:-1] != 0, arr[:-1], 1)
                returns = np.diff(arr) / denom
                total_return = (
                    (values[-1] - values[0]) / values[0] * 100 if values[0] > 0 else 0
                )
                volatility = float(np.std(returns) * np.sqrt(252) * 100)
                rf = 0.02 / 252
                excess = returns - rf
                sharpe_ratio = (
                    float(np.mean(excess) / np.std(returns) * np.sqrt(252))
                    if np.std(returns) > 0
                    else 0
                )
                peak = np.maximum.accumulate(arr)
                drawdown = (arr - peak) / np.where(peak != 0, peak, 1)
                max_drawdown = float(np.min(drawdown) * 100)
            else:
                total_return = volatility = sharpe_ratio = max_drawdown = 0

            return {
                "success": True,
                "performance": {
                    "current_value": values[-1] if values else 0,
                    "total_return": total_return,
                    "total_return_percentage": total_return,
                    "volatility": volatility,
                    "sharpe_ratio": sharpe_ratio,
                    "max_drawdown": max_drawdown,
                    "dates": dates,
                    "values": values,
                },
            }
        except Exception as exc:
            logger.error("Error getting portfolio performance: %s", exc)
            return {"success": False, "error": str(exc)}

    @staticmethod
    def optimize_portfolio(
        portfolio_id: str,
        user_id: str,
        target_return: Optional[float] = None,
        risk_tolerance: float = 0.5,
    ) -> Dict[str, Any]:
        try:
            import cvxpy as cp
        except ImportError:
            return {
                "success": False,
                "error": "cvxpy not installed. Cannot optimize portfolio.",
            }

        try:
            portfolio = Portfolio.query.filter_by(
                id=portfolio_id, user_id=user_id
            ).first()
            if not portfolio:
                return {"success": False, "error": "Portfolio not found"}

            holdings = PortfolioHolding.query.filter_by(portfolio_id=portfolio_id).all()
            if len(holdings) < 2:
                return {
                    "success": False,
                    "error": "Need at least 2 assets for optimization",
                }

            asset_returns = {}
            symbols = []
            for h in holdings:
                rets = PortfolioService._get_asset_returns(h.asset_id, days=252)
                if rets is not None and len(rets) > 0:
                    asset = db.session.get(Asset, h.asset_id)
                    if asset:
                        asset_returns[asset.symbol] = rets
                        symbols.append(asset.symbol)

            if len(asset_returns) < 2:
                return {
                    "success": False,
                    "error": "Insufficient price data for optimization",
                }

            min_len = min(len(v) for v in asset_returns.values())
            for k in asset_returns:
                asset_returns[k] = asset_returns[k][-min_len:]

            df = pd.DataFrame(asset_returns)
            exp_ret = df.mean().values * 252
            cov = df.cov().values * 252
            n = len(symbols)

            w = cp.Variable(n)
            obj = cp.Minimize(cp.quad_form(w, cov))
            prob = cp.Problem(obj, [cp.sum(w) == 1, w >= 0])
            prob.solve()

            if prob.status not in ["optimal", "optimal_inaccurate"]:
                return {
                    "success": False,
                    "error": f"Optimization failed: {prob.status}",
                }

            opt_w = w.value
            port_ret = float(np.dot(opt_w, exp_ret))
            port_vol = float(np.sqrt(max(float(prob.value), 0)))
            sharpe = (port_ret - 0.02) / port_vol if port_vol > 0 else 0

            recs = []
            for i, sym in enumerate(symbols):
                holding = next(
                    (
                        h
                        for h in holdings
                        if db.session.get(Asset, h.asset_id)
                        and db.session.get(Asset, h.asset_id).symbol == sym
                    ),
                    None,
                )
                cur_w = 0.0
                if (
                    holding
                    and portfolio.total_value
                    and float(portfolio.total_value) > 0
                ):
                    mv = holding.market_value or Decimal("0")
                    cur_w = float(mv) / float(portfolio.total_value)
                opt = float(opt_w[i])
                diff = opt - cur_w
                recs.append(
                    {
                        "symbol": sym,
                        "current_weight": round(cur_w, 4),
                        "optimal_weight": round(opt, 4),
                        "recommendation": (
                            "buy"
                            if diff > 0.05
                            else ("sell" if diff < -0.05 else "hold")
                        ),
                    }
                )

            return {
                "success": True,
                "optimization": {
                    "expected_return": round(port_ret * 100, 2),
                    "volatility": round(port_vol * 100, 2),
                    "sharpe_ratio": round(float(sharpe), 4),
                    "recommendations": recs,
                },
            }
        except Exception as exc:
            logger.error("Error optimizing portfolio: %s", exc)
            return {"success": False, "error": str(exc)}

    @staticmethod
    def _get_latest_price(asset_id: str) -> Optional[Decimal]:
        try:
            row = (
                PriceData.query.filter_by(asset_id=asset_id)
                .order_by(PriceData.timestamp.desc())
                .first()
            )
            return row.close_price if row else None
        except Exception as exc:
            logger.error("Error getting latest price: %s", exc)
            return None

    @staticmethod
    def _calculate_current_value(portfolio_id: str) -> Decimal:
        try:
            holdings = PortfolioHolding.query.filter_by(portfolio_id=portfolio_id).all()
            total = Decimal("0")
            for h in holdings:
                price = PortfolioService._get_latest_price(h.asset_id)
                if price:
                    total += h.quantity * price
            return total
        except Exception as exc:
            logger.error("Error calculating portfolio value: %s", exc)
            return Decimal("0")

    @staticmethod
    def _get_asset_returns(asset_id: str, days: int = 252) -> Optional[np.ndarray]:
        try:
            end = datetime.now(timezone.utc)
            start = end - timedelta(days=days)
            rows = (
                PriceData.query.filter(
                    and_(
                        PriceData.asset_id == asset_id,
                        PriceData.timestamp >= start,
                        PriceData.timestamp <= end,
                        PriceData.interval == "1d",
                    )
                )
                .order_by(PriceData.timestamp)
                .all()
            )
            if len(rows) < 2:
                return None
            prices = np.array([float(r.close_price) for r in rows])
            denom = np.where(prices[:-1] != 0, prices[:-1], 1)
            return np.diff(prices) / denom
        except Exception as exc:
            logger.error("Error getting asset returns: %s", exc)
            return None
