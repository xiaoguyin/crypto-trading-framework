"""A strategy package only reads snapshots and returns an order intent."""

from decimal import Decimal

from crypto_trading_framework.sdk import (
    Decision,
    OrderIntent,
    OrderSide,
    OrderType,
    StrategyContext,
)


class BuyOnFreshTicker:
    """Illustrates the SDK boundary; it is intentionally not a trading strategy."""

    @property
    def name(self) -> str:
        return "example.buy_on_fresh_ticker"

    def on_event(self, context: StrategyContext, event: object) -> Decision:
        del event
        ticker = context.ticker("BTC/USDT")
        if not ticker.usable():
            return Decision.skip("BTC/USDT ticker is not usable")

        return Decision(
            reason="example only: fresh ticker observed",
            intents=(
                OrderIntent(
                    symbol="BTC/USDT",
                    side=OrderSide.BUY,
                    order_type=OrderType.MARKET,
                    amount=Decimal("0.001"),
                    client_order_id=f"{self.name}:{context.now.isoformat()}",
                ),
            ),
        )
