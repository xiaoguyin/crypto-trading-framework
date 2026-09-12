# Architecture Boundaries

The planned framework consists of the strategy SDK, runtime, data layer, execution layer, and exchange adapters. This repository currently implements the minimal public strategy SDK contracts.

```text
Strategy plugin -> SDK <- Runtime -> Data snapshots
                            |
                            v
                      Execution layer -> CCXT adapter -> Exchange
```

Strategies use the SDK to read snapshots already available in local memory and return `Decision` and `OrderIntent` objects. They must not perform network requests, access databases, or call exchanges directly. The runtime schedules strategy execution. The data layer manages subscriptions, caching, and data quality. The execution layer manages risk checks, fund reservations, order state, and recovery.

This dependency direction keeps exchange access, order execution details, and persistence logic outside strategy code as strategies evolve.
