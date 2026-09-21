import json

def generate_mermaid_trace(output_file="audit_trace.mermaid"):
    mermaid_content = """sequenceDiagram
    autonumber
    participant A as AI Agent (Harness)
    participant G as API Gateway
    participant P as Target API (Payment/Mutation)
    participant L as Audit Ledger (smaos-audit)

    Note over A, L: Scenario: Wire Fault / Cognitive Fault
    A->>G: Tool Call: Execute Transaction
    G->>P: Forward Request
    P--xG: Network Fault (HTTP 504 Timeout)
    G-->>A: TCP RST / Exception
    
    rect rgb(255, 200, 200)
        Note over A, P: FATAL HALLUCINATION RISK
        Note right of A: Standard Agent assumes success because request was fired.
    end
    
    rect rgb(200, 255, 200)
        Note over A, L: EVIDENCE ABSENT ⟹ UNKNOWN
        A->>L: @proof_or_stop downgrades state to UNKNOWN
        Note right of L: Ledger drift prevented. Safe state maintained.
    end
"""
    with open(output_file, "w") as f:
        f.write(mermaid_content)
    print(f"Generated {output_file}")

def generate_dora_report(output_file="dora_art17_gap_report.json"):
    report = {
        "incident_classification": "Major",
        "affected_clients_threshold": "0% (Mitigated)",
        "financial_impact_risk": "High (€100,000+ Potential Double-Spend)",
        "mitigation": "State forced to UNKNOWN via Evidence Absent invariant",
        "tri_score": "0% Toxic Receipts in current trace"
    }
    with open(output_file, "w") as f:
        json.dump(report, f, indent=2)
    print(f"Generated {output_file}")

if __name__ == "__main__":
    generate_mermaid_trace()
    generate_dora_report()
