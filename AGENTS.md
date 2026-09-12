# Development Guidelines

- `src/crypto_trading_framework/sdk/` is the public interface for strategy packages. Framework internals must not depend on strategy projects.
- Public snapshot reads must not initiate network or database requests, or wait for background tasks.
- Strategies return `Decision` objects and order intents. Order submission, risk checks, fund reservations, and exchange interactions belong to the execution layer.
- When changing public types, snapshot semantics, event semantics, or persistence formats, update the tests, README, and changelog together.
- Run `uv run ruff check .`, `uv run ruff format --check .`, `uv run ty check`, `uv run pytest`, and `uv build` before completing changes.
- Keep shared VS Code settings portable: use workspace-relative paths and the uv-managed `.venv` environment.
- Do not commit API keys, account data, order data, or local runtime logs.
