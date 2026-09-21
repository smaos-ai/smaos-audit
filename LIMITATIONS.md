# Limitations & Disclosures

1. **Non-Certification Scope:** This repository (Door 1) provides mechanical post-execution reconciliation. It does *not* contain the Ring 0 eBPF LSM hooks or hardware enclave cryptography (Door 2).
2. **Liability:** Users are responsible for integrating `smaos-audit` with their internal SIEM/SOC infrastructure. No guarantees are made regarding automated regulatory filing acceptance.
3. **Wasm Boundaries:** The provided WebAssembly verifier bounds memory but relies on the host runtime (e.g., Wasmtime/Extism) to enforce filesystem isolation.
