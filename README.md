# smaos-audit (Agent Flight Recorder)

> **`smaos-audit`**: Zero-dependency wire-fault & cognitive overclaim auditor for autonomous agentic workflows.  
> **Core Invariant:** \(\text{Evidence Absent} \implies \mathbf{UNKNOWN} \quad (\text{NEVER } \mathbf{CONFIRMED})\)

**smaos-audit** mitigates the hallucinated state drift (e.g., HTTP 504 timeouts) left behind by pre-execution authorization frameworks like Microsoft AGT.

## 1-Line Execution
Run offline to guarantee zero data egress:
```bash
docker run --rm -v $(pwd)/traces:/data:ro --network none smaos-ai/smaos-audit:v0.1.0
```

## The Remediation Decorator (`fix.patch`)
```python
@proof_or_stop
def execute_wire_action(payload):
    # If HTTP 504 or unverified retrieval occurs:
    # Forces immutable UNKNOWN state & prevents double-spend retries
    return gateway_dispatch(payload)
```

## Architecture
See `smaos_audit/` for the 0-dependency stdlib Python pipeline (Anonymizer, Dispatcher, Bundler, Interrogator, Reflector, Reporter). See `examples/` for board-ready output deliverables.

## License
Apache 2.0. See [LICENSE](LICENSE).
