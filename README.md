# crypto-trading-framework

A cryptocurrency trading framework designed around independently maintained strategies. Strategies read local snapshots and produce order intents; the framework is responsible for data updates, rate limiting, risk checks, and order execution.

The current `0.1.0` development baseline provides the initial public SDK contracts, quality checks, package builds, and GitHub Actions configuration. Exchange connectivity and order execution are planned components.

## Development Environment

Use Python 3.13 and uv to manage the project environment and dependencies:

```powershell
uv sync --locked
uv run ruff check .
uv run ruff format --check .
uv run ty check
uv run pytest
uv build
```

Install the Git hooks after cloning the repository:

```powershell
uv run pre-commit install
```

## VS Code

Open this repository as the workspace folder, run `uv sync --locked`, and install the recommended Python, Python Debugger, Ruff, and ty extensions from the Extensions view. Extension recommendations are recorded in the repository; they do not install extensions automatically.

The default interpreter is the workspace `.venv` directory. If VS Code previously selected a different interpreter, run **Python: Select Interpreter** and choose `.venv`. Ruff and ty use the project environment; ty provides type checking and language services. Python files are formatted and imports organized on explicit saves.

- **Ctrl+Shift+B** runs `uv: check all`: dependency sync, lint, format checks, type checks, tests, and the package build, in sequence.
- **Tasks: Run Task** exposes individual checks, formatting, and the dependency audit.
- **Run and Debug** supports the current Python file and all pytest tests.
- **Test Explorer** discovers tests in `tests/` and supports running or debugging individual tests.

Test Explorer does not enforce the full-suite coverage threshold on a partial test run. The `uv: test` task and CI retain the configured 90% threshold. Test debugging disables coverage collection so breakpoints work correctly.

Settings use workspace-relative paths for Windows and Linux. Shared Ruff, ty, pytest, and coverage rules remain in `pyproject.toml`.

## Public SDK Contracts

- Snapshot reads return local data without waiting for network requests, database queries, or background refreshes.
- Snapshots describe the value, availability, freshness, and source health. Missing data is not represented as a zero value.
- Strategies return `Decision` and `OrderIntent` objects without directly calling exchanges or order executors.
- The execution layer will process order intents. Local acceptance and subsequent status events must be distinguished from exchange confirmation and fills.

See `src/crypto_trading_framework/sdk/`, [architecture](docs/architecture.md), and [API contracts](docs/api-contracts.md).

## Project Layout

```text
src/crypto_trading_framework/sdk/  Public strategy interfaces and value objects
tests/                            Unit and contract tests
.github/workflows/ci.yml           GitHub Actions checks
.vscode/                          Shared editor, task, and debug configuration
```

## Example

[`examples/minimal_strategy.py`](examples/minimal_strategy.py) illustrates the strategy boundary by reading a local snapshot and returning an order intent. It does not connect to an exchange or place an order.
