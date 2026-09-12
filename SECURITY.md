# Security Policy

## Supported Versions

Security fixes are provided for the latest released minor version of the
framework. Before the first stable release, the current `0.1.x` development
baseline is supported on a best-effort basis.

## Reporting a Vulnerability

Please do not report security vulnerabilities through public issues,
discussions, pull requests, or social media.

Use this repository's **Private vulnerability reporting** feature in the
Security tab to submit a report directly to the maintainers. Include a clear
description of the issue, affected versions or files, reproduction steps, and
the security impact.

Do not include real exchange API keys, account identifiers, order data,
balances, personal data, or other credentials in a report. Use redacted values
and minimal proof-of-concept code instead.

We aim to acknowledge reports within seven days. We will investigate the
report, coordinate a fix when appropriate, and publish a security advisory for
confirmed vulnerabilities after users have a reasonable opportunity to update.

## Scope

Reports are especially helpful when they affect the public strategy SDK,
snapshot handling, rate limiting, exchange connectivity, order execution,
credential handling, dependency supply chain, or GitHub Actions workflows.

The framework must not be used to submit live orders or access exchanges with
real credentials until those components are explicitly implemented and
documented.
