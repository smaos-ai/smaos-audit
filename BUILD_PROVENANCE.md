# Build Provenance & Supply Chain Integrity

This repository follows strict SLSA (Supply-chain Levels for Software Artifacts) Level 3 guidelines to guarantee build provenance for the `smaos-audit` engine.

## Deterministic Builds
The Python codebase relies exclusively on the Python 3.12 Standard Library. There are zero external dependencies in `smaos_audit/`, eliminating supply chain poisoning vectors (e.g., malicious PyPI packages).

## WebAssembly Verification
The `smaos_verify_bg.wasm` binary is compiled deterministically from Rust using `wasm-pack`. 
To verify the build locally:
```bash
cargo build --target wasm32-unknown-unknown --release
sha256sum target/wasm32-unknown-unknown/release/smaos_verify.wasm
```
*Note: Cryptographic signatures for the WASM binaries are maintained in the private Door 2 registry.*
