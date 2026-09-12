"""Value objects exchanged between strategies and the framework."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from decimal import Decimal
from enum import StrEnum


class Availability(StrEnum):
    """Whether a requested snapshot has a value available locally."""

    READY = "ready"
    WARMING = "warming"
    MISSING = "missing"
    UNSUPPORTED = "unsupported"


class Freshness(StrEnum):
    """How current a locally available snapshot is."""

    FRESH = "fresh"
    STALE = "stale"
    UNKNOWN = "unknown"


class Health(StrEnum):
    """Health of the data source that produced a snapshot."""

    HEALTHY = "healthy"
    DEGRADED = "degraded"
    DISCONNECTED = "disconnected"


@dataclass(frozen=True, slots=True)
class Snapshot[T]:
    """An immutable locally available value and its data-quality metadata."""

    value: T | None
    availability: Availability
    freshness: Freshness
    health: Health
    received_at: datetime | None = None
    source_time: datetime | None = None
    version: int = 0

    def usable(
        self,
        *,
        max_age: timedelta | None = None,
        now: datetime | None = None,
    ) -> bool:
        """Return whether the snapshot meets a strategy's minimum data requirement."""
        if self.value is None or self.availability is not Availability.READY:
            return False
        if self.freshness is not Freshness.FRESH or self.health is not Health.HEALTHY:
            return False
        if max_age is None:
            return True
        if self.received_at is None or now is None:
            return False
        return now - self.received_at <= max_age


class OrderSide(StrEnum):
    """Unified direction for an order."""

    BUY = "buy"
    SELL = "sell"


class OrderType(StrEnum):
    """Order types a strategy may request."""

    MARKET = "market"
    LIMIT = "limit"


@dataclass(frozen=True, slots=True)
class OrderIntent:
    """A validated-by-schema request that the execution layer may accept or reject."""

    symbol: str
    side: OrderSide
    order_type: OrderType
    amount: Decimal
    client_order_id: str
    price: Decimal | None = None
    expires_at: datetime | None = None

    def __post_init__(self) -> None:
        if not self.symbol:
            raise ValueError("symbol must not be empty")
        if self.amount <= Decimal("0"):
            raise ValueError("amount must be positive")
        if self.order_type is OrderType.LIMIT and self.price is None:
            raise ValueError("limit orders require a price")
        if self.order_type is OrderType.MARKET and self.price is not None:
            raise ValueError("market orders must not include a price")


@dataclass(frozen=True, slots=True)
class Decision:
    """A strategy result for one event, including a human-readable explanation."""

    reason: str
    intents: tuple[OrderIntent, ...] = ()
    annotations: dict[str, str] = field(default_factory=dict)

    @classmethod
    def skip(cls, reason: str) -> Decision:
        """Create a decision that intentionally requests no market action."""
        return cls(reason=reason)
