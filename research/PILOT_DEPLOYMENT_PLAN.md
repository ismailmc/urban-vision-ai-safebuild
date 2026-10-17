# Pilot deployment, adoption and costs
Recommendation only; no partner, hosted service or field pilot exists.

## One bounded workflow
Primary user: traffic-management/roadwork engineer with a local planning reviewer; secondary reviewer: municipal engineer/community liaison.
Decision: compare supplied construction access arrangements and determine which communities warrant further site review.
Inputs: source plan/notice, dates and mode, frozen roads, verified origins/facility entrances, allowed alternatives and permission/cost uncertainty.
Outputs: per-origin reachability and route-distance changes, worst affected origins, five-state attribution, feasible/Pareto alternatives, unstable assumptions and a source-linked report.
Human review: approve road matching, access classes, turns, entrances, construction feasibility and authority permissions. SafeBuild does not authorize a diversion.

Jurisdiction: selected Kakkanad roads may involve Thrikkakara municipality, road owner and traffic police as well as KMRL; exact ownership/competent authority remains a dependency. KMRL provides a public entry channel, not an agreement:
https://kochimetro.org/contact-us/
customerrelations@kmrl.co.in ; 0484-2846700.
Pune fallback public contact: https://www.punemetrorail.org/report ; customercare.pmrp@mahametro.org.
Use institutional faculty to request forwarding to relevant planning/traffic officials. No contact was sent.

## Practical deployment
Start offline/local: frozen PBF/GeoPackage snapshots, immutable JSON run manifests and reports. No continuous feeds needed for the research demo.
A designated data steward records refresh dates, audits changes to critical roads/entrances, and invalidates results when construction phase or restrictions change. Require re-review at each phase change; proposed weekly checks during an active pilot are a team policy, not a verified authority obligation.
Integration: export PDF/CSV/GeoPackage into existing traffic-management review; preserve source edge IDs and approval status. No GIS replacement or automatic government API integration assumed.

Security: server-only model key; authenticated editing; read-only public views; file-size/type and zip/path checks; bounded graph workloads; restricted-plan segregation; no household-level acquisition records in public exports; redact third-party private information. Record reviewer/version and permission changes. Public release needs an explicit disclosure audit.
Store inputs, hashes, configs, measured outputs, failures and source rights; keep sensitive plans separate. Storage volume has not been measured. AI retention/privacy choice must be checked against account terms before using restricted documents.

## Costs: transparent categories
| Category | Verified price or assumption | What is excluded |
|---|---|---|
| Local demo software | Existing hardware assumed; open data/tools do not imply zero operating labor | Development, power, reviewer and field travel |
| AI tokens | Provider current standard rate: $0.30 input/$2.50 output per million for selected model | Quota, taxes, retrieval, retries |
| Illustrative 100-call allowance | $0.34 for assumed 3k input/1k billed output each | Not measured or quoted |
| Hosted software pilot | No hosting quote selected; measure CPU/RAM/storage then obtain provider quote | Do not claim free-tier suitability for municipal use |
| Field verification | Hours/travel/reviewer rates unknown | No fabricated total |
| Physical intervention | UNKNOWN until design, quantities, local schedule of rates and authority review | Separate from all software costs |

Formula: software cost = compute + storage/backups + AI + data stewardship/reviewer + security/maintenance. Physical cost = approved quantities × applicable verified rates + safety controls + traffic management + reinstatement/contingency. No rupee conversion or infrastructure estimate is supplied without verified rates.
AI price source: https://ai.google.dev/gemini-api/docs/pricing

## Outreach draft — not sent
Subject: Request for technical feedback on a student construction-accessibility prototype

Dear KMRL team,
I am Ismail, a B.Tech Computer Engineering student at Vimal Jyothi Engineering College. We are developing Urban Vision AI — SafeBuild for SFIC, a research prototype comparing how construction access arrangements may affect surrounding residents' road access to essential destinations. We have reviewed public Phase II documentation and seek feedback from the relevant traffic-management or planning engineer. Could you direct us to publicly shareable diversion/phase drawings and advise whether a short technical review is possible? The tool does not estimate real ambulance response times or authorize road changes. We will seek approval before using restricted plans or naming an organization as a partner.
Thank you,
Ismail
Vimal Jyothi Engineering College

## Deadline gates
Proposed schedule, not a completion promise:
12–14 Oct: coordinator slot/rules, full snapshot and site/destination audit.
15–17 Oct: directed graph + independent route tests; stop if data assumptions materially invalidate it.
18–19 Oct: five-state causality and finite intervention tests.
20–21 Oct: optional AI evaluation + external formative review if arranged.
22 Oct: reproducibility/security/public disclosure and demo rehearsal.
23 Oct: coordinator reviews and submits; 24 Oct official closing date.
If factual evidence remains missing, submit a narrow correctly labeled research demonstration; do not promote it to “pilot-ready”.

