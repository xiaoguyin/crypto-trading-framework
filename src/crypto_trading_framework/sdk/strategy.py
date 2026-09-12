"""Protocols that define the boundary between a strategy package and the framework."""

from __future__ import annotations

from datetime import datetime
from typing import Protocol

from crypto_trading_framework.sdk.models import Decision, Snapshot


class StrategyContext(Protocol):
    """Read-only data view supplied to a strategy for a single decision event."""

    @property
    def now(self) -> datetime:
        """Return the framework clock used for this decision."""
        ...

    def ticker(self, symbol: str) -> Snapshot[object]:
        """Return the latest local ticker snapshot without waiting for network I/O."""
        ...


class Strategy(Protocol):
    """The minimal contract implemented by an independently versioned strategy."""

    @property
    def name(self) -> str:
        """Return the stable strategy identifier."""
        ...

    def on_event(self, context: StrategyContext, event: object) -> Decision:
        """Read snapshots and produce a decision without directly performing I/O."""
        ...
