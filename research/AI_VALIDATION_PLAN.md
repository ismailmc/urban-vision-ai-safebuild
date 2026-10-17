# Genuine AI architecture and evaluation
Status: proposed, not implemented or evaluated. Sources checked 2026-10-12.

## Candidate decisions
| Candidate | Task/input | Ground truth | Baseline/metrics | Risks and requirements | Decision |
|---|---|---|---|---|---|
| A: Evidence-grounded analyst | Explain structured run results and retrieved source excerpts; read-only tools | Backend metric values + reviewed source spans, plus manually authored answer key | Deterministic template; assertion accuracy, valid citations, abstention, reviewer time | Numeric/context hallucination, causal overclaim; server key, small CPU app + hosted model | INCLUDE after engine passes |
| B: Notice-to-Network | Extract road, endpoints, restriction type, mode, date/time from authentic notices; suggest edge IDs | Two-person notice annotation adjudicated against source; independently reviewed map match | Regex/manual entry; field precision/recall, temporal accuracy, accepted edge matches, review time | Ambiguous roads, OCR/date/language errors, no authentic notice corpus yet | POSTPONE; not a demo with fabricated notices |
| C: Predictive infrastructure model | Forecast an observed outcome from genuine labels | Independently recorded access failures/traffic outcomes | Historical/no-change baseline; outcome-specific calibration/error | No suitable authenticated local labels verified; graph-generated labels circular | EXCLUDE |

Documented hosted model: **gemini-3.5-flash-lite**, with structured outputs and function calling; optional escalation to a currently documented Flash model only if predeclared evaluation justifies it. Availability is verified in provider documentation, not in the user's API account. Sources:
https://ai.google.dev/gemini-api/docs/models/gemini-3.5-flash-lite
https://ai.google.dev/gemini-api/docs/models
https://ai.google.dev/gemini-api/docs/structured-output
No API credentials were requested, used or tested. Model support does not guarantee local billing/quota access.
For B the same model may parse text/PDF, but real notice annotation is the blocker. C has no justified model choice until task and training labels exist.

## Small implementation
Tools: get_run_manifest(run_id), get_origin_impacts(run_id), get_candidate_status(candidate_id), get_source_span(source_id,page/span), compare_runs(run_ids).
Return structured objects containing value, unit, scenario, origin/destination, source ID and evidence class. Model outputs claim objects referencing these IDs. Server validates every number and verifies its scope before rendering text. An equality check against any number somewhere in the run is insufficient.
No write tools, arbitrary SQL, arbitrary URL retrieval, geometry creation or automatic scenario application. Treat retrieved text as data and test prompt injection.
The model may explain supported comparisons and uncertainty, never confer permits, infer a real closure from a hypothetical one or convert distance to ambulance arrival time.
Use a deterministic report if model/key/network unavailable. Label cached AI as a saved result; do not present replay as runtime inference.

## Frozen evaluation
At least 40 predeclared cases, with raw prompts, tools, output, model/version, reviewer labels and token usage:
- 10 numeric/scope/unit cases, including stale run IDs and mixed scenarios.
- 8 causality/identical-plan/private-entrance cases.
- 8 missing evidence/unreachable/uncertain permission cases.
- 8 malicious source or user prompt cases.
- 6 mode/common-cause/no-option cases.
These counts are proposed corpus allocation, not achieved results.
Gold answers authored independently from model output and reviewed by a human. Do not use the same LLM's grading as independent truth.

Release targets: zero material unsupported numeric/causal/permit/ETA assertions released; 100% claim-ID/unit/run validation; 100% correct abstention on deliberately missing material evidence; at least 90% reviewed factual answers on answerable questions; no unauthorized tool action. A failed case blocks that AI release until corrected and rerun. Forty cases cannot prove universal hallucination immunity.
Compare explanation usefulness and review time to a deterministic template; disable AI if it adds errors without practical benefit.

For B, if later included: annotate at least 20 authentic notices from multiple dates/road names with document-level held-out split; propose >=95% precision on extracted critical restrictions, report recall, require 100% human confirmation before application. Small samples yield uncertain performance, so publish raw errors and confidence limitations. No live notices collected in this research.

## Operating estimate
Provider pricing checked: Flash-Lite standard input $0.30/million tokens, output including thinking $2.50/million.
Illustrative workload assumption: 100 calls × 3,000 input tokens + 1,000 billed output tokens = $0.34 in token fees. Not measured usage, not a quote; excludes retries, thinking above allowance, retrieval services, taxes and infrastructure.
Ground on the frozen local evidence store; do not pay for public web search for routine run explanations.
https://ai.google.dev/gemini-api/docs/pricing

