# ISO/IEC 42001 "Auditor-in-a-Box" Partner Briefing

## Target Audience
GRC Platforms, ISO 42001 Lead Auditors, and Enterprise Risk Committees.

## The Evidence Gap
ISO 42001 requires organizations to maintain an AI Management System (AIMS) with continuous monitoring, incident logging, and strict data governance. However, standard LLM agents hallucinate states during network timeouts (HTTP 504), corrupting the audit trail and violating basic evidence requirements.

## Category H Controls Achieved via `smaos-audit`
Implementing `smaos-audit` as a post-execution sidecar immediately fulfills the following technical requirements:

1. **Incident Records:** Auto-generation of `dora_art17_gap_report.json` and `audit_trace.mermaid` provides immutable evidence of trapped system faults.
2. **Monitoring Results & KPIs:** The Toxic Receipt Index (`TRI_Scorecard.md`) gives Lead Auditors a quantitative KPI for AI failure rates across staging and production.
3. **Third-Party AI Oversight:** The `--network none` execution boundary ensures that third-party vendors (e.g., OpenAI, Anthropic) do not receive execution traces or PII, eliminating shadow processor risk.

For integration inquiries or GRC platform partnerships, contact the SMAOS s.r.o. architecture team.
