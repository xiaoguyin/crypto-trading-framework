from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from crypto_trading_framework.sdk import (
    Availability,
    Decision,
    Freshness,
    Health,
    OrderIntent,
    OrderSide,
    OrderType,
    Snapshot,
)


def test_fresh_ready_snapshot_is_usable_within_age_limit() -> None:
    now = datetime(2026, 9, 12, tzinfo=UTC)
    snapshot = Snapshot(
        value={"last": Decimal("100")},
        availability=Availability.READY,
        freshness=Freshness.FRESH,
        health=Health.HEALTHY,
        received_at=now - timedelta(seconds=1),
    )

    assert snapshot.usable(max_age=timedelta(seconds=2), now=now)


@pytest.mark.parametrize(
    ("availability", "freshness", "health"),
    [
        (Availability.WARMING, Freshness.UNKNOWN, Health.HEALTHY),
        (Availability.READY, Freshness.STALE, Health.HEALTHY),
        (Availability.READY, Freshness.FRESH, Health.DISCONNECTED),
    ],
)
def test_unready_or_unhealthy_snapshot_is_not_usable(
    availability: Availability,
    freshness: Freshness,
    health: Health,
) -> None:
    snapshot = Snapshot(
        value={"last": Decimal("100")},
        availability=availability,
        freshness=freshness,
        health=health,
    )

    assert not snapshot.usable()


def test_limit_order_requires_price() -> None:
    with pytest.raises(ValueError, match="require a price"):
        OrderIntent(
            symbol="BTC/USDT",
            side=OrderSide.BUY,
            order_type=OrderType.LIMIT,
            amount=Decimal("0.01"),
            client_order_id="strategy-1",
        )


@pytest.mark.parametrize(
    ("order_type", "price", "error"),
    [
        (OrderType.MARKET, Decimal("100"), "must not include a price"),
        (OrderType.MARKET, None, None),
    ],
)
def test_order_intent_enforces_order_type_price_rules(
    order_type: OrderType,
    price: Decimal | None,
    error: str | None,
) -> None:
    if error is None:
        intent = OrderIntent(
            symbol="BTC/USDT",
            side=OrderSide.BUY,
            order_type=order_type,
            amount=Decimal("0.01"),
            client_order_id="strategy-2",
            price=price,
        )
        assert intent.price is None
    else:
        with pytest.raises(ValueError, match=error):
            OrderIntent(
                symbol="BTC/USDT",
                side=OrderSide.BUY,
                order_type=order_type,
                amount=Decimal("0.01"),
                client_order_id="strategy-2",
                price=price,
            )


@pytest.mark.parametrize(
    ("symbol", "amount", "error"),
    [
        ("", Decimal("1"), "symbol must not be empty"),
        ("BTC/USDT", Decimal("0"), "amount must be positive"),
    ],
)
def test_order_intent_rejects_invalid_identifiers_or_amounts(
    symbol: str,
    amount: Decimal,
    error: str,
) -> None:
    with pytest.raises(ValueError, match=error):
        OrderIntent(
            symbol=symbol,
            side=OrderSide.BUY,
            order_type=OrderType.MARKET,
            amount=amount,
            client_order_id="strategy-3",
        )


def test_age_limited_snapshot_requires_clock_and_recent_local_data() -> None:
    snapshot = Snapshot(
        value={"last": Decimal("100")},
        availability=Availability.READY,
        freshness=Freshness.FRESH,
        health=Health.HEALTHY,
    )

    assert not snapshot.usable(max_age=timedelta(seconds=1))


def test_skip_decision_has_no_order_intents() -> None:
    assert Decision.skip("ticker unavailable").intents == ()
