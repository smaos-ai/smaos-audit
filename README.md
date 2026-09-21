# smaos-audit v0.1.0 (Agent Flight Recorder)

**smaos-audit** is a zero-egress, air-gapped auditor for autonomous AI agents. It mitigates the hallucinated state drift (e.g., HTTP 504 timeouts) left behind by pre-execution authorization frameworks like Microsoft AGT.

## Core Problem
Agents assume an action succeeded because they triggered it. If a network drops during a deployment or trade, the agent hallucinates a \`CONFIRMED\` state, triggering catastrophic ledger drift and DORA compliance violations.

## How it Works
1. **Zero-Egress Execution:** Runs in a strict `--network none` Docker container or Wasm cell.
2. **Net Ledger Reconciliation:** Validates the bitemporal state to ensure \`∑Δ_net = 0.00\`.
3. **DORA RTS 2024/1772 Compliant:** Automatically generates Article 17 Major Incident gap reports.

## Quickstart
\`\`\`bash
# 1. Build the air-gapped auditor
docker build -t smaos-audit .

# 2. Run an audit trace offline
docker run --network none -v $(pwd)/fixtures:/data smaos-audit /data/sample_staging_traces.jsonl
\`\`\`

## Architecture
See \`smaos_audit/\` for the 6-stage stdlib Python pipeline (Dispatcher, Bundler, Interrogator, Reflector, Reporter).

## License
Apache 2.0. See [LICENSE](LICENSE).
