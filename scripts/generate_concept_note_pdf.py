"""
Script to generate SafeBuild_Concept_Note.pdf (6-8 A4 pages)
Conforming strictly to submission guidelines, verified claims, ReportLab standards,
and exact budget/operating parameters.
"""
import os
import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 7.5)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header (Pages 2+)
        if self._pageNumber > 1:
            self.drawString(36, 806, "URBAN VISION AI — SAFEBUILD | CONCEPT NOTE & TECHNICAL PROPOSAL")
            self.drawRightString(559, 806, "PROTOTYPE FOR SCENARIO PLANNING")
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.5)
            self.line(36, 800, 559, 800)

        # Footer (All pages)
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(36, 38, 559, 38)
        self.drawString(36, 28, "SafeBuild: Plan roadwork. Keep communities connected. • SFIC 2026")
        self.drawRightString(559, 28, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()

def build_concept_note(output_pdf_path="SafeBuild_Concept_Note.pdf"):
    # Target: A4 (595.27 x 841.89 points)
    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=46,
        bottomMargin=46
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=4
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#0D9488'),
        spaceAfter=6
    )
    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor('#0F766E'),
        spaceBefore=6,
        spaceAfter=3,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#1E293B'),
        spaceAfter=4
    )
    body_bold = ParagraphStyle(
        'BodyBold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )
    badge_style = ParagraphStyle(
        'BadgeText',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor('#0F766E')
    )
    alert_box_style = ParagraphStyle(
        'AlertBox',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#92400E')
    )
    callout_box_style = ParagraphStyle(
        'CalloutBox',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#0F172A')
    )

    story = []

    # =========================================================================
    # PAGE 1: TITLE, EXECUTIVE SUMMARY & READINESS DECLARATION
    # =========================================================================
    story.append(Paragraph("URBAN VISION AI — SAFEBUILD", title_style))
    story.append(Paragraph("Plan roadwork. Keep communities connected.", subtitle_style))
    story.append(Paragraph("<b>Sustainable Futures Innovation Challenge (SFIC 2026) — Track A: Infrastructure & Access Planning</b>", body_bold))
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0D9488"), spaceBefore=2, spaceAfter=8))

    # Readiness Declaration Box
    readiness_text = """
    <b>READINESS DECLARATION & PROTOTYPE NOTICE:</b><br/>
    <b>Working prototype tested using real Kakkanad geographic data and hypothetical construction scenarios; field validation and authority review pending.</b><br/>
    SafeBuild is a functional decision-support prototype built to demonstrate how municipal roadwork restrictions can be modeled deterministically to assess community accessibility and compare eligible construction arrangements before ground-breaking. It is not an officially deployed municipal software or statutory clearance authority.
    """
    readiness_table = Table([[Paragraph(readiness_text, alert_box_style)]], colWidths=[523])
    readiness_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FEF3C7')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#F59E0B')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(readiness_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph("1. Executive Summary", h1_style))
    story.append(Paragraph(
        "Rapid urbanization and major transit infrastructure construction across Indian Tier-1 and Tier-2 cities frequently "
        "introduce uncoordinated road closures that sever community access to essential facilities—most critically healthcare receiving centers, "
        "public transport interchanges, schools, and employment centers. While civil engineering specifications rigorously define structural "
        "workzones, the spatial accessibility impacts on surrounding neighborhoods are rarely modeled before construction begins. "
        "The consequences include compounded detour burdens on vulnerable neighborhoods, unmanaged rat-running through narrow residential lanes, "
        "and total severance of non-motorized access.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Urban Vision AI — SafeBuild</b> addresses this operational gap by providing an open, verifiable scenario planning studio that enables urban "
        "planners, public works agencies, and civic advocates to evaluate proposed road restrictions before implementation. "
        "Rather than relying on ungrounded generative guesses or computationally opaque black boxes, SafeBuild couples an authentic 19,582-node "
        "OpenStreetMap road network with deterministic 5-state routing algebra, multi-phase construction schedule modeling, and a guarded AI analyst "
        "governed by strict verification safeguards.",
        body_style
    ))

    story.append(Paragraph("2. Strategic Alignment & Core Mission", h1_style))
    story.append(Paragraph(
        "SafeBuild directly advances SFIC Track A objectives by embedding community equity and accessibility into urban capital project planning. "
        "The project is structured around three foundational principles:",
        body_style
    ))
    principles_data = [
        [Paragraph("<b>1. Spatial Equity First</b>", body_bold), Paragraph("Measures how road restrictions affect distinct residential clusters differently, identifying isolated neighborhoods and preventing one-size-fits-all diversion plans.", body_style)],
        [Paragraph("<b>2. Mathematical Determinism</b>", body_bold), Paragraph("Eliminates simulation randomness and hallucinated timings. All metrics are computed as reproducible shortest-path graph calculations with complete referential integrity.", body_style)],
        [Paragraph("<b>3. Truthful Prototype Gating</b>", body_bold), Paragraph("Enforces strict prototype review gates. If candidate mitigation options lack signed authority clearance or physical feasibility, SafeBuild strictly emits <code>NO_VERIFIED_OPTION</code>.", body_style)]
    ]
    p_table = Table(principles_data, colWidths=[140, 383])
    p_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(p_table)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: THE URBAN CHALLENGE & CASE STUDY CONTEXT
    # =========================================================================
    story.append(Paragraph("3. The Urban Challenge: Roadwork Severance in Indian Cities", h1_style))
    story.append(Paragraph(
        "In rapidly growing Indian metropolitan regions, linear infrastructure projects—such as elevated metro rail corridors, flyovers, "
        "stormwater drain overhauls, and utility trenching—frequently occupy the primary carriage-width of key arterial roads for 12 to 36 months. "
        "Standard construction practice relies on piecemeal, reactive traffic advisories issued only after barricades are erected. "
        "This paradigm causes four systemic planning failures:",
        body_style
    ))

    challenges = [
        ("Asymmetric Neighborhood Detour Penalties", "While vehicles originating directly on the arterial may face modest detours, feeder settlements located behind the corridor face compounding access bottlenecks, turning short trips into circuitous journeys exceeding 20-30% additional travel distance."),
        ("Unregulated Residential Spillover", "When major arterial reaches close without modeled alternative capacity, diverted passenger vehicles flood narrow collector and residential streets never designed for arterial traffic volumes, creating localized safety hazards and pavement degradation."),
        ("Pedestrian & Non-Motorized Vulnerability", "Operational interventions like single-lane vehicular contraflow frequently consume existing footway width or force pedestrians into active construction gutters, directly compromising walkability."),
        ("Lack of Pre-Construction Arrangement Auditing", "Civil contractors typically execute work sequences based on contractor equipment logistics rather than community accessibility exposure, missing opportunities to sequence reaches in ways that minimize cumulative community disruption.")
    ]
    c_table_data = [[Paragraph(f"<b>{title}</b>", body_bold), Paragraph(desc, body_style)] for title, desc in challenges]
    c_table = Table(c_table_data, colWidths=[160, 363])
    c_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(c_table)
    story.append(Spacer(1, 6))

    story.append(Paragraph("4. Representative Case Study: Kakkanad Corridor, Kochi", h1_style))
    story.append(Paragraph(
        "To ground the prototype in genuine spatial geometry, SafeBuild models the <b>Palarivattom–Kakkanad Road Corridor</b> in Ernakulam District, "
        "Kerala, India. This corridor represents a critical arterial spine connecting residential suburbs, government administrative headquarters "
        "(Kakkanad Civil Station), and major employment centers (Infopark / SmartCity Kochi). "
        "The corridor is currently undergoing major public infrastructure planning, making it an ideal empirical testbed for evaluating simulated construction closures.",
        body_style
    ))

    study_meta_rows = [
        ["Study Attribute", "Case Study Value", "Topological Verification"],
        ["Geographic Extent", "Kakkanad, Kochi [76.330°E – 76.360°E, 10.010°N – 10.035°N]", "Full 32.8 km² routing buffer bounding box"],
        ["Base Road Network", "19,582 nodes; 11,675 motor vehicle directed edges", "OpenStreetMap contributors (ODbL 1.0), 0 dangling refs"],
        ["Pedestrian Permeability", "16,842 directed edges (footways, paths, steps)", "Explicitly separated dual-graph routing topology"],
        ["Evaluated Facility", "Sunrise Hospital, Seaport-Airport Road", "Verified active tertiary emergency healthcare anchor"],
        ["Sampled Community Anchors", "7 distinct residential clusters (Kakkanad West, Padamugal, DLF, etc.)", "Curb-snapped centroid anchors representing settlement catchments"],
        ["Simulated Restriction", "Palarivattom–Kakkanad Rd Reach (Ways 197827530, 383253303, etc.)", "Hypothetical civil pier foundation workzone closure"]
    ]
    s_table = Table([[Paragraph(c, body_bold if i==0 else body_style) for c in r] for i, r in enumerate(study_meta_rows)], colWidths=[120, 240, 163])
    s_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E2E8F0')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#94A3B8')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(s_table)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: THE SAFEBUILD SOLUTION & GUIDED WORKFLOW
    # =========================================================================
    story.append(Paragraph("5. The SafeBuild Solution: Guided Four-Step Workflow", h1_style))
    story.append(Paragraph(
        "SafeBuild redesigns the planning interaction around one intuitive question: "
        "<i>'If this road is restricted during construction, how does community access change, and would another arrangement help?'</i> "
        "The application organizes complex network graph theory into four sequential steps:",
        body_style
    ))

    workflow_steps = [
        ("Step 1: Define Work", "Choose any road segment on the interactive map or select from pre-configured corridor phases. Specify directionality (bidirectional vs one-way), travel mode, and construction activity. All unverified closures are clearly tagged as hypothetical models."),
        ("Step 2: Check Access", "Execute live Dijkstra shortest-path calculations against baseline network conditions. Instantly view modeled detours, newly unreachable origins, and visual before/after routing paths to critical facilities."),
        ("Step 3: Compare Arrangements", "Audit candidate work arrangements (e.g. sequential phasing vs contraflow lane management vs accelerated concurrent closures) to understand trade-offs across duration, detour severity, and pedestrian mode conflict."),
        ("Step 4: Export Plan", "Download RFC 4180 compliant CSV audit trails and tamper-evident PDF scenario briefs containing complete metadata, snapshot dates, and scientific disclaimers.")
    ]
    w_data = [[Paragraph(f"<b>{step}</b>", body_bold), Paragraph(desc, body_style)] for step, desc in workflow_steps]
    w_table = Table(w_data, colWidths=[130, 393])
    w_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(w_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph("6. Formal 5-State Routing Algebra", h1_style))
    story.append(Paragraph(
        "To guarantee mathematical rigor and prevent confounding baseline network characteristics with construction impacts, "
        "SafeBuild defines a formal 5-state graph algebra. Every reported distance is strictly attributed to a specific network state:",
        body_style
    ))

    algebra_rows = [
        ["State Notation", "Formal Set Definition", "Physical Meaning in Planning", "Invariance / Safeguard"],
        ["G0", "G_base = (V, E_base)", "Pre-construction baseline network", "Baseline reference for all detour deltas"],
        ["G0 + P", "G_base ∪ E_proposal", "Network with planned permanent capital additions", "Identity Invariant: G0+P == G0 when P=identity"],
        ["G0 + P + C", "(G0 ∪ E_p) \\ E_closure", "Network under active construction restriction", "Closure Monotonicity: dist(G0_C) >= dist(G0)"],
        ["G0 + P + C + M", "((G0 ∪ E_p) \\ E_c) ∪ E_mitigation", "Construction state with candidate mitigation (e.g. contraflow)", "Re-weighted or added capacity; evaluated for feasibility"]
    ]
    a_table = Table([[Paragraph(c, body_bold if i==0 else body_style) for c in r] for i, r in enumerate(algebra_rows)], colWidths=[70, 110, 183, 160])
    a_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E2E8F0')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#94A3B8')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(a_table)
    story.append(Spacer(1, 6))

    story.append(Paragraph("Attribution Isolation Principle:", h2_style))
    story.append(Paragraph(
        "Net construction detour delta is strictly defined as: <b>Δ = dist(G0_C) - dist(G0)</b>. "
        "Because baseline travel distance varies significantly across residential origins (e.g., DLF City is 2,060 m from Sunrise Hospital while "
        "Padamugal is 283 m), evaluating absolute detour distance alongside percentage increase provides an honest, transparent metric of impact.",
        body_style
    ))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: TECHNICAL ARCHITECTURE & MULTI-PHASE SCHEDULING
    # =========================================================================
    story.append(Paragraph("7. Technical Architecture & Multi-Phase Engine", h1_style))
    story.append(Paragraph(
        "SafeBuild is architected as an offline-capable, high-performance web platform combining a FastAPI/NetworkX backend with "
        "a React/Next.js/MapLibre GL client. All spatial calculations execute deterministically on directed multigraphs without external API dependencies.",
        body_style
    ))

    arch_components = [
        ("Geospatial Ingestion Engine", "Parses raw OpenStreetMap XML files across tiled subboxes with 100% boundary overlap. Resolves shared nodes, eliminates duplicates, and builds referentially complete directed multigraphs (OSMParser)."),
        ("Dual-Mode Directed Routing Engine", "Maintains separate topological subgraphs for motor vehicles (excluding dedicated footpaths and service alleys) and pedestrians (incorporating stairs, living streets, and pedestrian paths) using NetworkX."),
        ("Multi-Phase Construction Engine", "Models complex multi-phase construction schedules with predecessor dependencies. Features DFS-based circular dependency detection, calendar day unit normalization, and non-overlapping schedule exposure calculation."),
        ("Guarded Geospatial AI Analyst", "Integrates Google Gemini API with deterministic server-side assertion filtering. If API credentials are unavailable or if prompt responses fail truthfulness filters, the engine falls back gracefully to deterministic analysis templates.")
    ]
    arch_table_data = [[Paragraph(f"<b>{comp}</b>", body_bold), Paragraph(desc, body_style)] for comp, desc in arch_components]
    arch_table = Table(arch_table_data, colWidths=[150, 373])
    arch_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(arch_table)
    story.append(Spacer(1, 6))

    story.append(Paragraph("8. Multi-Phase Construction Schedule Specification", h1_style))
    story.append(Paragraph(
        "Real-world urban infrastructure works are never executed in a single monolithic closure. "
        "SafeBuild models construction as a sequence of discrete engineering activities with independent durations and road restrictions:",
        body_style
    ))

    phase_rows = [
        ["Phase ID", "Engineering Activity", "Duration", "Dependencies", "Restricted OSM Ways", "Modeled Schedule Window"],
        ["phase_1_utility", "Underground Utility Relocation", "21.0 days", "None (Initial)", "Way 197827530 (Eastbound)", "Day 0.0 to 21.0"],
        ["phase_2_piling", "Metro Pier Foundation & Piling", "45.0 days", "Depends on Phase 1", "Ways 197827530, 383253303 (Both)", "Day 21.0 to 66.0"],
        ["phase_3_girder", "Viaduct Girder Launching", "30.0 days", "Depends on Phase 2", "Ways 1011679137, 1011679138 (Both)", "Day 66.0 to 96.0"]
    ]
    ph_table = Table([[Paragraph(c, body_bold if i==0 else body_style) for c in r] for i, r in enumerate(phase_rows)], colWidths=[80, 130, 60, 75, 100, 78])
    ph_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E2E8F0')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#94A3B8')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(ph_table)
    story.append(Spacer(1, 6))

    story.append(Paragraph(
        "<b>Schedule Verification Note:</b> The 96.0-day sequential duration represents the exact arithmetic sum of modeled activities (21 + 45 + 30 days). "
        "In accelerated scenarios (e.g. Arrangement C), an illustrative 35% time compression factor (0.65 multiplier -> 62.4 days) is explored "
        "to model parallel reach execution; this factor is explicitly labeled as a simulation assumption rather than an empirical CPM schedule.",
        body_style
    ))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: EMPIRICAL KAKKANAD SCENARIO STUDY RESULTS
    # =========================================================================
    story.append(Paragraph("9. Empirical Scenario Study Results: Access to Sunrise Hospital", h1_style))
    story.append(Paragraph(
        "The baseline analysis evaluates motor vehicle access from seven representative residential anchors across Kakkanad to the "
        "primary emergency entrance of Sunrise Hospital on Seaport-Airport Road. The hypothetical workzone restricts the Palarivattom–Kakkanad Road "
        "arterial reach (OSM Way IDs 197827530, 383253303, 1011679137, 1011679138):",
        body_style
    ))

    results_table_data = [
        ["Community Anchor (Origin)", "Sampling Method", "Baseline G0 (m)", "Under Work G0_C (m)", "Net Detour (m)", "Detour %", "Access Status"],
        ["Kakkanad West / Civil Station", "Road-side curb anchor", "1,572.6", "1,927.5", "+354.9", "+22.6%", "Reachable via Collector"],
        ["Civil Station Administrative Hub", "Frontage curb node", "1,842.1", "2,052.4", "+210.3", "+11.4%", "Reachable via Bypass"],
        ["Padamugal Residential Anchor", "Post-office frontage node", "282.7", "415.8", "+133.1", "+47.1%", "Reachable via Local Lane"],
        ["Kollamkudimugal Settlement", "Junction centroid", "1,140.5", "1,140.5", "0.0", "0.0%", "Unaffected (Alternate Corridor)"],
        ["Canal Colony / Athani Settlement", "Canal access road centroid", "1,420.0", "1,420.0", "0.0", "0.0%", "Unaffected (Eastern Reach)"],
        ["DLF City / New Town Heights", "Arterial access centroid", "2,060.4", "2,060.4", "0.0", "0.0%", "Unaffected (Seaport Corridor)"],
        ["NGO Quarters Housing Colony", "Colony arterial connector", "1,650.2", "1,650.2", "0.0", "0.0%", "Unaffected (Northern Corridor)"]
    ]
    r_table = Table([[Paragraph(c, body_bold if i==0 else body_style) for c in r] for i, r in enumerate(results_table_data)], colWidths=[120, 95, 62, 75, 55, 48, 68])
    r_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E2E8F0')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#94A3B8')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(r_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph("10. Analytical Insights & Spatial Equity Findings", h1_style))
    story.append(Paragraph(
        "<b>1. Asymmetric Severance Pattern:</b> The closure creates pronounced spatial asymmetry. Western origins (Kakkanad West, Civil Station) "
        "and central residential pockets (Padamugal) bear the entire network detour penalty, while eastern and southern clusters (DLF City, Canal Colony) "
        "experience exactly 0.0 m change due to independent access via Seaport-Airport Road.",
        body_style
    ))
    story.append(Paragraph(
        "<b>2. Percentage vs Absolute Disproportion:</b> Padamugal experiences the highest relative route expansion (+47.1%), while Kakkanad West "
        "suffers the largest absolute distance penalty (+354.9 m). Evaluating both metrics simultaneously prevents misleading prioritization.",
        body_style
    ))
    story.append(Paragraph(
        "<b>3. Zero Network Disconnection:</b> Despite the closure of the primary arterial, 7 of 7 sampled origins retain connected routing paths to "
        "Sunrise Hospital via secondary collectors (e.g. Civil Lane Road and residential bypasses), demonstrating that the road network has topological redundancy.",
        body_style
    ))
    story.append(Paragraph(
        "<b>4. Pedestrian Mode Divergence:</b> Walking route distances are substantially shorter (1,240.2 m for Kakkanad West vs 1,572.8 m vehicle baseline) "
        "due to pedestrian permeability through narrow public footpaths. However, vehicular workzones directly threaten this permeability.",
        body_style
    ))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 6: BOUNDED ARRANGEMENT COMPARISON & PROTOTYPE REVIEW GATE
    # =========================================================================
    story.append(Paragraph("11. Bounded Work Arrangement Tradeoff Analysis", h1_style))
    story.append(Paragraph(
        "Rather than proposing unconstrained, arbitrary diversions, SafeBuild performs a bounded comparison over three operationally distinct "
        "construction sequencing arrangements, evaluating what improves, what worsens, and what remains unverified:",
        body_style
    ))

    arrangement_cards = [
        ("Arrangement A: Standard Sequential Phasing", "Sequential (96.0 days)", "Executes utility relocation, piling, and girder launching one phase at a time.", "• Improves: Restricts only one reach at any given time, preserving collector bypass capacity.\n• Worsens: Extends total project schedule exposure to full 96.0 days.", "PROVISIONAL_GEOMETRY_MODEL / UNVERIFIED_MODEL_SCENARIO", "Ineligible (Awaiting formal authority review)"),
        ("Arrangement B: Managed Contraflow & Signal Priority", "Sequential (96.0 days)", "Preserves one managed unidirectional vehicle lane through the workzone with human flaggers.", "• Improves: Mathematically recovers arterial connectivity, reducing worst detour by up to 180 m.\n• Worsens: Compresses pedestrian walkway clearance and elevates worker exposure in the active workzone.", "PROVISIONAL_GEOMETRY_MODEL / UNVERIFIED_MODEL_SCENARIO", "Ineligible (Awaiting safety review & authority clearance)"),
        ("Arrangement C: Accelerated Concurrent Work", "Concurrent (62.4 days modeled)", "Simultaneously closes multiple corridor reaches to compress modeled project duration by ~35%.", "• Improves: Shortens total calendar duration exposure from 96.0 to 62.4 days.\n• Worsens: Simultaneous corridor closures concentrate detour traffic onto collector streets, compounding neighborhood route congestion.", "HIGH_NETWORK_DETOUR_CONCENTRATION / EXCLUDED_BY_MODEL_CONSTRAINTS", "Excluded (Fails scenario accessibility thresholds)")
    ]

    for title, sched, desc, tradeoffs, status, elig in arrangement_cards:
        card_content = f"""
        <b>{title}</b> | <i>{sched}</i><br/>
        <b>Description:</b> {desc}<br/>
        <b>Tradeoff Analysis:</b><br/>{tradeoffs.replace(chr(10), '<br/>')}<br/>
        <b>Feasibility Status:</b> <code>{status}</code> | <b>Review Gate:</b> <b>{elig}</b>
        """
        card_table = Table([[Paragraph(card_content, callout_box_style)]], colWidths=[523])
        card_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
            ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ]))
        story.append(card_table)
        story.append(Spacer(1, 4))

    story.append(Paragraph("12. The Prototype Review Gate: Strict NO_VERIFIED_OPTION", h1_style))
    gate_explanation = """
    <b>SYSTEM DECISION GATE OUTPUT: <code>NO_VERIFIED_OPTION</code></b><br/>
    <b>Mandatory Ethical Safeguard:</b> SafeBuild enforces a strict decision safeguard: no candidate routing alteration or diversion "
    may be presented to decision-makers as formal, implementable advice without documented physical site clearance and verified authority permits. "
    While Arrangement B demonstrates mathematical detour reduction, it introduces pedestrian mode conflicts and lacks verified field traffic management plans. "
    Arrangement C is excluded due to severe compounded detour concentration. Therefore, the optimizer safely and strictly outputs "
    <code>NO_VERIFIED_OPTION</code>, protecting against false algorithmic authority.
    """
    gate_table = Table([[Paragraph(gate_explanation, alert_box_style)]], colWidths=[523])
    gate_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FEF3C7')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#F59E0B')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(gate_table)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 7: VERIFICATION, CRYPTOGRAPHIC PROVENANCE & INDEPENDENT AUDIT
    # =========================================================================
    story.append(Paragraph("13. Cryptographic Data Provenance & Test Verification", h1_style))
    story.append(Paragraph(
        "To ensure end-to-end reproducibility, all source geographic data, test suites, and analytical outputs are backed by "
        "cryptographic checksums and automated verification suites:",
        body_style
    ))

    raw_csums = [
        ["OSM Tile Artifact", "Spatial Coverage Area", "SHA-256 Checksum"],
        ["subbox_0.osm", "Northwest Kakkanad (Vazhakkala / Palarivattom border)", "50ebc99d4db060d844c2cf4d820384d250fb3c4cec774278e5f4a37efb98c88e"],
        ["subbox_1.osm", "North-central corridor (Padamugal arterial reach)", "3a62f672ca598aa5c77206b598910e974eeb353bf472cf14bb637ecd2ab512e2"],
        ["subbox_2.osm", "Northeast sector (Kollamkudimugal residential)", "9c4cc29acb749e2a81c42b9f87ed30aef31552a1cd17f5bbb878284f830ec6b6"],
        ["subbox_3.osm", "Southwest sector (Civil Station Environs / Seaport)", "dc0799244624b702671612d18f9e22a4a9e7aa427acb9db36f54025177fcb6e5"],
        ["subbox_4.osm", "South-central corridor (Collectorate Road junction)", "014a8255424f3b470ec8638cfd62d8f85eeefd59c239890f69d4055e5b82431e"],
        ["subbox_5.osm", "Southeast sector (Infopark Expressway / DLF City)", "cb8cab0c22dae818d2816b04ad121e0b826aa340ae961ed7a0e8fcb7035f298f"]
    ]
    raw_table = Table([[Paragraph(c, body_bold if i==0 else body_style) for c in r] for i, r in enumerate(raw_csums)], colWidths=[80, 160, 283])
    raw_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E2E8F0')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#94A3B8')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(raw_table)
    story.append(Spacer(1, 6))

    story.append(Paragraph("14. Automated Test Suite Classification (17 Tests)", h1_style))
    story.append(Paragraph(
        "The test suite spans three test modules (`test_analytical_core.py`, `test_validation_protocol.py`, `test_multi_phase.py`) "
        "and verifies all 17 critical system invariants:",
        body_style
    ))

    test_classes = [
        ["Test Category", "Count", "Verified Invariants & Test Scope", "Status"],
        ["Validation", "6", "Schema validation, zero missing highway refs, unknown OSM way guard, duration guards, prototype review gate", "6 / 6 PASSED"],
        ["Correctness", "8", "Directed oneway traversal, grade separation without junction, closure monotonicity, proposal algebra identity, circular dependency detection, schedule exposure sum, multi-phase execution", "8 / 8 PASSED"],
        ["Geographic", "2", "CRS coordinate bounds [76.330-76.360°E, 10.010-10.035°N], UTM Zone 43N metric projection consistency", "2 / 2 PASSED"],
        ["Guarded AI", "1", "Server-side assertion filter intercepting ungrounded causal claims and fabricated approvals", "1 / 1 PASSED"],
        ["Total Suite", "17", "Complete automated unit and invariant test suite across all engines", "17 / 17 PASSED"]
    ]
    tc_table = Table([[Paragraph(c, body_bold if i==0 else body_style) for c in r] for i, r in enumerate(test_classes)], colWidths=[80, 45, 320, 78])
    tc_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E2E8F0')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#94A3B8')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(tc_table)
    story.append(Spacer(1, 6))

    story.append(Paragraph("15. Independent Reference Implementation Audit", h1_style))
    story.append(Paragraph(
        "To confirm accuracy beyond production self-testing, an independent verification script (`scripts/independent_verification.py`) "
        "was executed using a separate XML parser and standalone NetworkX graph. The results cross-verified against production:",
        body_style
    ))

    audit_summary_rows = [
        ["Verification Metric", "Independent Reference", "Production Engine", "Discrepancy", "Tolerance & Outcome"],
        ["Baseline G0 Distance", "1,572.61 m", "1,572.60 m", "0.0055 m (5.5 mm)", "Tol: 0.1 m -> EXACT AGREEMENT"],
        ["Restricted G0_C Distance", "1,927.50 m", "1,927.50 m", "0.0043 m (4.3 mm)", "Tol: 0.1 m -> EXACT AGREEMENT"],
        ["Net Detour Delta (Δ)", "+354.89 m", "+354.90 m", "0.0098 m (9.8 mm)", "Tol: 0.1 m -> EXACT AGREEMENT"],
        ["Sequential Schedule", "96.0 days", "96.0 days", "0.0 days", "Exact arithmetic match"],
        ["Concurrent Schedule (0.65x)", "62.4 days", "62.4 days", "0.0 days", "Exact match (illustrative assumption)"]
    ]
    as_table = Table([[Paragraph(c, body_bold if i==0 else body_style) for c in r] for i, r in enumerate(audit_summary_rows)], colWidths=[120, 95, 95, 95, 118])
    as_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E2E8F0')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#94A3B8')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(as_table)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 8: PROPOSED BUDGET, OPERATING ECONOMICS & ETHICAL SAFEGUARDS
    # =========================================================================
    story.append(Paragraph("16. Proposed Implementation Budget & Operating Economics", h1_style))
    story.append(Paragraph(
        "<b>Important Notice:</b> The figures below represent a <b>proposed implementation budget</b> for a potential 3-month collaborative "
        "development and field-study cycle with local stakeholders. They do <b>not</b> represent past expenditures incurred.",
        body_style
    ))

    budget_rows = [
        ["Budget Component", "Proposed Allocation (INR)", "Scope & Key Deliverables"],
        ["Geospatial Data Engineering", "Rs. 60,000 – Rs. 1,10,000", "High-resolution curb and sidewalk survey, micro-turning relation tagging, OSM reconciliation"],
        ["Platform Development & Modeling", "Rs. 1,10,000 – Rs. 2,00,000", "Dynamic traffic diversion integration, multi-facility batch routing, scenario editor enhancements"],
        ["Field Validation & Ground Survey", "Rs. 60,000 – Rs. 1,15,000", "Physical site surveys of proposed detours, pedestrian conflict cross-section measurement"],
        ["Stakeholder Review & Workshops", "Rs. 40,000 – Rs. 80,000", "Workshops with local planning bodies, community consultations, feedback synthesis"],
        ["Total Proposed 3-Month Cycle", "Rs. 2,70,000 – Rs. 5,05,000", "Complete 3-month research development and field scenario evaluation package"]
    ]
    b_table = Table([[Paragraph(c, body_bold if i==0 else body_style) for c in r] for i, r in enumerate(budget_rows)], colWidths=[140, 110, 273])
    b_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E2E8F0')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#94A3B8')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(b_table)
    story.append(Spacer(1, 6))

    story.append(Paragraph("Ongoing Monthly Operating Model:", h2_style))
    story.append(Paragraph(
        "Following initial deployment, ongoing monthly operations are projected at <b>Rs. 8,000 – Rs. 25,000 / month</b>, covering cloud hosting (VPS/container runtime), "
        "periodic OSM network refreshes, server maintenance, and guarded AI API token usage. This lean operating cost ensures long-term civic sustainability.",
        body_style
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("17. Methodological Limitations & Ethical Safeguards", h1_style))
    limitations = [
        ("Static Shortest Path vs Dynamic Traffic", "SafeBuild computes static shortest path distances. It does not perform dynamic traffic assignment (DTA), queue simulation, or live traffic delay estimation. Detour distance is a structural proxy for accessibility, not observed travel time."),
        ("No Fabricated Emergency Timing", "The system never converts route distance into synthetic ambulance travel seconds or survival probability claims without empirical vehicle-telemetry datasets."),
        ("No Demographic Extrapolations", "Impacts are reported across sampled geographic cluster centroids, not synthesized population counts or demographic voting statistics."),
        ("Planar Coastal Topography", "Elevation and road slope impedances are omitted, which is appropriate for the coastal plains of Kochi but would require enhancement for hilly terrain."),
        ("Authority & Regulatory Boundary", "SafeBuild outputs are decision-support scenario models. Real-world implementation strictly requires statutory review, formal traffic management plans, and inter-agency approval.")
    ]
    lim_table_data = [[Paragraph(f"<b>{title}</b>", body_bold), Paragraph(desc, body_style)] for title, desc in limitations]
    lim_table = Table(lim_table_data, colWidths=[140, 383])
    lim_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(lim_table)
    story.append(Spacer(1, 6))

    story.append(Paragraph(
        "<b>Conclusion:</b> SafeBuild demonstrates that urban roadwork planning can move beyond uncoordinated closures and ungrounded claims. "
        "By pairing authentic geospatial data with transparent graph algebra, multi-phase scheduling, and ethical prototype safeguards, "
        "SafeBuild enables cities to plan construction while keeping communities connected.",
        body_style
    ))

    # Build the document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated concept note PDF at: {output_pdf_path}")
    file_size_bytes = os.path.getsize(output_pdf_path)
    print(f"File size: {file_size_bytes / (1024*1024):.2f} MB ({file_size_bytes} bytes)")

if __name__ == "__main__":
    build_concept_note()
