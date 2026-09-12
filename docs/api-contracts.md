# Public API Contracts

`sdk` defines the public interface for strategy packages. Other modules are internal implementation details and may change as the framework develops.

## Snapshots

Reads of `Snapshot[T]` must return local state immediately, without waiting for network requests, database queries, or background refreshes. Callers must inspect `availability`, `freshness`, and `health`, and must not trade using an absent `value`.

`Snapshot.usable()` checks the strategy's minimum data-quality requirements. It does not guarantee the exchange's current state, order acceptance, or execution.

## Decisions and Order Intents

A strategy's `on_event()` returns a `Decision`. Its `intents` describe requested actions; they do not indicate that an order has been submitted, accepted by the exchange, or filled.

Strategies must reuse the same `OrderIntent.client_order_id` for repeated submissions of the same logical action. The execution layer will use that identifier to correlate deduplication, persistence, and order reconciliation.
