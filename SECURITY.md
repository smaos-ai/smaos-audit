# Security Policy

## Zero-Egress Guarantee
`smaos-audit` is designed to be executed in a strictly air-gapped environment. We strongly recommend running the audit engine using the `--network none` Docker flag to mathematically guarantee that no PII, trace logs, or proprietary data can leave your host machine.

## Supported Versions
| Version | Supported          |
| ------- | ------------------ |
| v0.1.x  | :white_check_mark: |

## Reporting a Vulnerability
If you discover a vulnerability, please do NOT open a public issue. Email security@smaos.ai. We will respond within 24 hours.
