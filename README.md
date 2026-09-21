# smaos-audit (Agent Flight Recorder)

> **`smaos-audit`**: Zero-dependency wire-fault & cognitive overclaim auditor for autonomous agentic workflows.  
> **Core Invariant:** `Evidence Absent ⟹ UNKNOWN (NEVER CONFIRMED)`

**smaos-audit** mitigates the hallucinated state drift (e.g., HTTP 504 timeouts) left behind by pre-execution authorization frameworks like Microsoft AGT.

## 1-Line Execution
Run offline to guarantee zero data egress:
```bash
docker run --rm -v $(pwd)/traces:/data:ro --network none smaos-ai/smaos-audit:v0.1.0
```

## ISO 42001 "Category H" Capability Matrix
`smaos-audit` acts as an out-of-the-box technical control for ISO/IEC 42001 AI Management Systems:
* **Check 26 (Transparency):** Immutable SCITT receipts.
* **Check 29 (Human Oversight):** Forced state downgrades on network faults.
* **Check 31 (Security & Privacy):** Zero-egress `--network none` execution.
* **Check 33 (Documentation & Evidence):** Board-ready `audit_trace.mermaid` sequence generation.

## The Remediation Decorator (`fix.patch`)
```python
@proof_or_stop
def execute_wire_action(payload):
    # If HTTP 504 or unverified retrieval occurs:
    # Forces immutable UNKNOWN state & prevents double-spend retries
    return gateway_dispatch(payload)
```

## Architecture
See `smaos_audit/` for the 0-dependency stdlib Python pipeline. See `examples/` for board-ready output deliverables. See `docs/ISO42001_CATEGORY_H.md` for Lead Auditor documentation.

## License
Apache 2.0. See [LICENSE](LICENSE).
