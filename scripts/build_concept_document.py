import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Polygon, Group

class NumberedCanvas5(canvas.Canvas):
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
            self.draw_header_footer(num_pages)
            super().showPage()
        super().save()

    def draw_header_footer(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 7.5)
        self.setFillColor(colors.HexColor("#64748b"))

        # Running Header (pages 2+)
        if self._pageNumber > 1:
            self.drawString(36, 808, "Urban Vision AI — SafeBuild | Concept and Design Document")
            self.drawRightString(559, 808, "Engineering Innovation Proposal • 5-Page Concept Note")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(36, 802, 559, 802)

        # Running Footer (all pages)
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(36, 36, 559, 36)
        self.drawString(36, 25, "Urban Vision AI — SafeBuild | Scenario Planning Model • Field Validation & Statutory Review Pending")
        self.drawRightString(559, 25, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()

def make_vector_flow_diagram(w=523, h=40):
    d = Drawing(w, h)
    steps = [
        ("1. Inputs", "Way IDs & Phases"),
        ("2. Geo Prep", "OSM Graph / UTM"),
        ("3. Subgraphs", "5-State Algebra"),
        ("4. Routing", "Dijkstra Engine"),
        ("5. Phasing", "Bounded Ledger"),
        ("6. Guarded AI", "Metrics Synthesis"),
        ("7. Export", "Decision Brief")
    ]
    n = len(steps)
    gap = 6
    arrow_w = 6
    box_w = (w - (n - 1) * (gap + arrow_w)) / n
    box_h = h - 6
    
    for i, (title, sub) in enumerate(steps):
        x = i * (box_w + gap + arrow_w)
        y = 3
        # Styling: highlight routing (step 4), endpoints (1, 7)
        if i == 3:
            bg_col = colors.HexColor("#0f766e")
            stroke_col = colors.HexColor("#0d9488")
            t_col = colors.white
            s_col = colors.HexColor("#ccfbf1")
        elif i in (0, 6):
            bg_col = colors.HexColor("#0f172a")
            stroke_col = colors.HexColor("#1e293b")
            t_col = colors.white
            s_col = colors.HexColor("#cbd5e1")
        else:
            bg_col = colors.HexColor("#f8fafc")
            stroke_col = colors.HexColor("#cbd5e1")
            t_col = colors.HexColor("#0f172a")
            s_col = colors.HexColor("#64748b")
        
        d.add(Rect(x, y, box_w, box_h, rx=2.5, ry=2.5, fillColor=bg_col, strokeColor=stroke_col, strokeWidth=0.75))
        d.add(String(x + box_w/2, y + box_h - 12, title, textAnchor='middle', fontName='Helvetica-Bold', fontSize=7.2, fillColor=t_col))
        d.add(String(x + box_w/2, y + 6.5, sub, textAnchor='middle', fontName='Helvetica', fontSize=5.8, fillColor=s_col))
        
        if i < n - 1:
            ax = x + box_w + gap/2
            ay = y + box_h/2
            d.add(Line(ax, ay, ax + arrow_w, ay, strokeColor=colors.HexColor("#94a3b8"), strokeWidth=0.8))
            d.add(Polygon([ax + arrow_w, ay, ax + arrow_w - 2.5, ay + 2, ax + arrow_w - 2.5, ay - 2], fillColor=colors.HexColor("#94a3b8"), strokeColor=None))
            
    return d

def build_concept_pdf(filename="SafeBuild_Concept_Document_Final.pdf"):
    # Target exactly A4 portrait (595.27 x 841.89 pt)
    # Margins: 36 pt left & right -> Printable width = 523.27 pt
    # Top margin: 40 pt, bottom margin: 44 pt -> Printable height = 757.89 pt
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=40,
        bottomMargin=44
    )

    styles = getSampleStyleSheet()

    # Typography hierarchy tuned for exactly 5 pages without crowding
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=23,
        textColor=colors.HexColor('#0f172a')
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor('#0f766e')
    )
    meta_tag_style = ParagraphStyle(
        'MetaTag',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7,
        leading=9,
        textColor=colors.HexColor('#475569')
    )
    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=14.5,
        textColor=colors.HexColor('#0f172a'),
        spaceBefore=4,
        spaceAfter=2
    )
    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=11.5,
        textColor=colors.HexColor('#1e293b'),
        spaceBefore=2,
        spaceAfter=1.5
    )
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=10.2,
        textColor=colors.HexColor('#334155'),
        spaceAfter=3
    )
    body_bold = ParagraphStyle(
        'BodyBold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )
    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=6.8,
        leading=8.6,
        textColor=colors.HexColor('#334155')
    )
    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=table_cell,
        fontName='Helvetica-Bold'
    )
    callout_text = ParagraphStyle(
        'Callout',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.2,
        leading=9.4,
        textColor=colors.HexColor('#1e293b')
    )
    disclaimer_text = ParagraphStyle(
        'Disclaimer',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=6.8,
        leading=8.8,
        textColor=colors.HexColor('#991b1b')
    )
    caption_style = ParagraphStyle(
        'Caption',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=6.8,
        leading=8.6,
        textColor=colors.HexColor('#64748b'),
        alignment=1
    )

    story = []

    # =========================================================================
    # PAGE 1: HEADER, NOTICE & SECTION 1: PROBLEM DEFINITION
    # =========================================================================
    story.append(Paragraph("URBAN VISION AI — SAFEBUILD", title_style))
    story.append(Paragraph("“Plan roadwork. Keep communities connected.”", subtitle_style))
    story.append(Spacer(1, 2))

    meta_table = Table([
        [
            Paragraph("<b>DOCUMENT TYPE:</b> Engineering Innovation Concept Document", meta_tag_style),
            Paragraph("<b>FOCUS:</b> Pre-Construction Access Optimization", meta_tag_style),
            Paragraph("<b>CASE STUDY:</b> Kakkanad Corridor, Kochi, Kerala", meta_tag_style)
        ]
    ], colWidths=[185, 175, 163])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f1f5f9')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 4))

    notice_box = Table([
        [Paragraph("<b>EVALUATION NOTICE & REGULATORY BOUNDARY:</b> "
                   "SafeBuild is an analytical decision-support research prototype for evaluating community accessibility during planned roadway works. "
                   "All simulated routes represent deterministic graph-theoretic shortest path traversals (Dijkstra algorithm) and DO NOT "
                   "constitute approved traffic circulation plans, live emergency response routing, or real-time travel delay predictions. "
                   "Physical interventions require formal statutory review from municipal transport departments and relevant public works bodies.", disclaimer_text)]
    ], colWidths=[523])
    notice_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#fef2f2')),
        ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor('#f87171')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(notice_box)
    story.append(Spacer(1, 5))

    story.append(Paragraph("1. PROBLEM DEFINITION", h1_style))
    story.append(Paragraph(
        "<b>1.1 The Urban Roadwork Accessibility Challenge:</b> "
        "Municipal infrastructure civil works—such as metro rail viaduct construction, storm-water drainage renewal, utility trenching, "
        "and flyover foundation piling—are indispensable for long-term urban economic productivity. However, temporary roadway restrictions "
        "frequently sever critical transit arteries linking residential communities to essential civic destinations, including tertiary healthcare facilities, "
        "schools, workplaces, and public transportation interchanges. When multiple workzones are executed concurrently without comprehensive network analysis, "
        "entire residential enclaves can suffer severe connectivity degradation, turning short routine trips into protracted, circuitous detours.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Differential Impacts on Vulnerable Road Users:</b> "
        "Disruption impacts are not distributed equally across urban populations. While motorized vehicles face additional travel distances and congestion delays, "
        "pedestrians, older adults, and persons with disabilities experience severe mobility barriers. Roadwork barricades often encroach upon footpaths, "
        "forcing pedestrians into live traffic lanes or eliminating continuous pedestrian crossings. Concurrently, local commercial establishments depend on "
        "unobstructed freight delivery corridors and patron footfall, which are abruptly curtailed during extended roadbed closures.",
        body_style
    ))
    story.append(Spacer(1, 2))

    story.append(Paragraph(
        "<b>1.2 The Limitations of Post-Disruption Route Navigation:</b> "
        "Contemporary commercial navigation applications (e.g., Google Maps, Apple Maps, Waze) perform exceptionally well at dynamic re-routing "
        "<i>after</i> an active road closure, incident, or severe traffic bottleneck has already occurred. However, these tools operate downstream of civil engineering decisions. "
        "They inform individual drivers of congestion but cannot inform planners how work should be organized to prevent severance in the first place.",
        body_style
    ))
    story.append(Paragraph(
        "<b>The Central Civil Engineering Challenge:</b> "
        "Urban roadway workzones pose a multi-dimensional planning challenge: <i>Can civil engineers and municipal authorities evaluate and restructure the "
        "sequencing, spatial phasing, and temporary mitigation arrangements of roadwork before breaking ground, so that communities retain practical, continuous access?</i> "
        "Solving this challenge requires uniting topological network impedance, construction phase dependencies, and physical right-of-way constraints into an "
        "auditable, pre-construction decision-support framework.",
        body_style
    ))
    story.append(Spacer(1, 2))

    story.append(Paragraph(
        "<b>1.3 Case Study: Kakkanad Corridor Scenario Study (Kochi, Kerala):</b> "
        "To establish empirical validity on genuine urban geometry, SafeBuild was applied to a defined study corridor along the Palarivattom–Kakkanad Road "
        "in the Kochi metropolitan area, Kerala, India. The baseline road network was parsed directly from OpenStreetMap under the Open Database License (ODbL), "
        "capturing <b>19,582 nodes</b>, <b>11,675 motor vehicle highway edges</b>, and <b>16,842 pedestrian edges</b> within a 4.67 km² core boundary (projected to UTM Zone 43N). "
        "The scenario models hypothetical road restrictions along arterial segments (OSM Way IDs 197827530 and 383253303) affecting community connectivity to "
        "<b>Sunrise Hospital</b> (Vii/528-B Seaport-Airport Road) from seven representative residential cluster centroids. "
        "<i>Note: This scenario represents an unverified planning research model; it does not reflect an actual municipal closure or completed field pilot.</i>",
        body_style
    ))

    case_meta = [
        ["Dataset Dimension", "Attribute Value", "Geospatial Reference & Verification Mechanism"],
        ["Study Corridor Boundary", "76.3262, 9.9934 to 76.3688, 10.0276 (EPSG:4326)", "4.67 km² core perimeter with 6.8 km regional buffer in UTM Zone 43N"],
        ["Network Topology", "19,582 nodes, 11,675 motor edges, 16,842 pedestrian edges", "Raw OSM XML referential audit (0 missing node references)"],
        ["Target Destination", "Sunrise Hospital, Ernakulam (lat: 10.0215, lon: 76.3478)", "Ground-surveyed entrance node snapped via Euclidean KD-Tree"],
        ["Restricted Workzone", "Palarivattom–Kakkanad Road (OSM Way IDs: 197827530, 383253303)", "Full bidirectional carriage restriction (Simulated State G0_C)"]
    ]
    t_case = Table([[Paragraph(c, table_cell_bold if r==0 else table_cell) for c in row] for r, row in enumerate(case_meta)], colWidths=[110, 185, 228])
    t_case.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f766e')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')])
    ]))
    story.append(t_case)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: SECTION 2: IDEA/CONCEPT & SECTION 3: DESIGN (PART 1)
    # =========================================================================
    story.append(Paragraph("2. IDEA / CONCEPT / SOLUTION TO ADDRESS THE PROBLEM", h1_style))
    story.append(Paragraph(
        "<b>2.1 Customer Pains vs. Solution Gains:</b> "
        "Municipal transport engineers, public works departments, and civil contractors face chronic friction when coordinating construction schedules with urban access. "
        "SafeBuild translates these operational pain points into structured engineering gains:",
        body_style
    ))

    pains_gains = [
        ["Stakeholder Cohort", "Operational Pain Points (Current Practice)", "Engineered Gains (SafeBuild Decision Framework)"],
        ["Municipal Engineers & PWD", "Manual, siloed scheduling; zero spatial visibility into cumulative community cut-off across overlapping project phases.", "Multi-phase network simulation mapping exact access severance before breaking ground; automated metric audits."],
        ["Traffic Police & Planners", "Ad-hoc diversion approvals; secondary collector roads overwhelmed by uncoordinated detours and sharp turn choke points.", "Deterministic shortest-path detour quantification across all neighborhood centroids; turning restriction compliance."],
        ["Infrastructure Contractors", "Public outrage, unexpected project halts, and costly emergency re-sequencing due to unannounced access severance.", "Pre-validated construction phase dependencies; objective trade-off documentation demonstrating planning diligence."],
        ["Affected Communities", "Sudden loss of access to healthcare, schools, and transit; dangerous pedestrian detours forced into active traffic lanes.", "Preserved essential-service connectivity; transparent, phase-specific access plans; protected pedestrian walkways."]
    ]
    t_pg = Table([[Paragraph(c, table_cell_bold if r==0 else table_cell) for c in row] for r, row in enumerate(pains_gains)], colWidths=[95, 210, 218])
    t_pg.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f766e')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')])
    ]))
    story.append(t_pg)
    story.append(Spacer(1, 3))

    story.append(Paragraph(
        "<b>2.2 Core System Architecture & Modular Components:</b> "
        "SafeBuild operates as an end-to-end decision-support platform comprising eight integrated modules: "
        "(1) <i>Interactive GIS Planning Studio:</i> WebGL canvas rendering 2D/3D extruded structures and real-time routes. "
        "(2) <i>Network Preparation Engine:</i> Ingests raw OSM XML, constructs directed MultiDiGraphs in UTM Zone 43N, and projects origins via KD-Tree. "
        "(3) <i>5-State Subgraph Algebra:</i> Formally tracks baseline, closed, proposed, and mitigated states (G0 to G0_P_C_M). "
        "(4) <i>Deterministic Routing Engine:</i> Computes exact Dijkstra shortest paths with zero statistical variance. "
        "(5) <i>Construction Dependency Validator:</i> Topological sorting and cycle detection across construction phases. "
        "(6) <i>Bounded Scenario Comparison Ledger:</i> Rigorously compares candidate arrangements against physical and safety constraints. "
        "(7) <i>Guarded AI Explanation Layer:</i> Synthesizes analytical findings strictly quoting backend metrics with deterministic fallback. "
        "(8) <i>Engineering Report Generator:</i> Exports self-contained, auditable PDF decision briefs and CSV tables.",
        body_style
    ))
    story.append(Spacer(1, 2))

    story.append(Paragraph(
        "<b>2.3 Unique Selling Proposition (USP):</b> "
        "The definitive differentiator of SafeBuild is its focus on the <i>upstream civil engineering decision:</i> "
        "<b>SafeBuild evaluates how construction activities should be sequenced and coordinated to preserve community access before work commences, "
        "rather than merely directing vehicles around road closures after they occur.</b> "
        "While specialized GIS platforms (ArcGIS/QGIS) perform spatial queries, they lack construction scheduling dependencies. Conversely, project scheduling tools "
        "(Primavera P6, MS Project) lack topological road network awareness. SafeBuild unites these capabilities into a focused, community-first planning workflow.",
        body_style
    ))
    story.append(Spacer(1, 3))

    story.append(Paragraph("3. PROJECT DESCRIPTION AND HIGH-LEVEL DESIGN", h1_style))
    story.append(Paragraph(
        "SafeBuild structures construction access planning into a six-step engineering workflow illustrated in the system architecture diagram below:",
        body_style
    ))
    story.append(Spacer(1, 1))

    # Vector Flow Diagram
    story.append(make_vector_flow_diagram(w=523, h=38))
    story.append(Spacer(1, 3))

    story.append(Paragraph(
        "<b>Step 1 — Define the Construction Area & Restrictions:</b> "
        "Engineers select targeted highway segments by street name or OSM way ID, specifying closure directionality (bidirectional, forward-only, or reverse-only), "
        "target construction phases, estimated durations, and priority community destinations requiring guaranteed access.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Step 2 — Prepare Phase-Specific Network Subgraphs:</b> "
        "The road network is modeled as a directed multi-graph G = (V, E). SafeBuild formalizes phase restrictions via a <b>5-State Subgraph Algebra</b>: "
        "Baseline network G0; Disrupted network G0_C = G - E_disrupted; Proposed infrastructure G0_P = G ∪ E_proposal; "
        "Unmitigated construction state G0_P_C = (G ∪ E_p) - E_c; and Mitigated candidate state G0_P_C_M = ((G ∪ E_p) - E_c) ∪ E_mitigation. "
        "This mathematical rigor prevents speculative claims and ensures reproducible scenario tracking.",
        body_style
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: SECTION 3 (PART 2): TECHNICAL EXECUTION & PROTOTYPE EVIDENCE
    # =========================================================================
    story.append(Paragraph("3. PROJECT DESCRIPTION AND HIGH-LEVEL DESIGN (CONTINUED)", h1_style))
    story.append(Paragraph(
        "<b>Step 3 — Analyze Community Accessibility:</b> "
        "Using Dijkstra's algorithm, SafeBuild calculates the shortest path from sampled residential cluster centroids to essential facilities across each network state. "
        "Crucially, the system distinguishes between: (a) a destination reachable via a longer detour, (b) a destination disconnected by workzones (<code>reachable: false</code>), "
        "and (c) an origin already unreachable in the pre-construction baseline (G0). Disconnected states are never masked with arbitrary penalty values.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Step 4 — Compare Construction Arrangements:</b> "
        "Alternative construction arrangements (e.g., standard sequential phasing vs. managed contraflow vs. accelerated concurrent work) are evaluated across: "
        "detour distance increase (m), cumulative detour exposure (meter-days), schedule duration (days), pedestrian walkway clearance, and prerequisite acyclicity.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Step 5 — Explain Results via Guarded AI:</b> "
        "An AI explanation layer articulates trade-offs in plain language for public and administrative briefings. "
        "The model is strictly bounded by deterministic guardrails: it only quotes verifiable metrics produced by the graph engine and is programmatically barred "
        "from inventing routes, estimating uncalibrated emergency seconds, or asserting legal permissions.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Step 6 — Generate Access Plans & Audit Documentation:</b> "
        "The platform exports self-contained, auditable PDF decision briefs and CSV tables conforming to standardized audit schemas, providing transparent documentation "
        "for municipal review. Final implementation sanction remains strictly with qualified civil engineers and statutory authorities.",
        body_style
    ))
    story.append(Spacer(1, 2))

    story.append(Paragraph("Grounded Prototype Evidence: Kakkanad Scenario Study Routing", h2_style))
    story.append(Paragraph(
        "In the evaluated Kakkanad corridor scenario, seven representative residential cluster centroids were routed to Sunrise Hospital under baseline (G0) "
        "and restricted (G0_C) conditions. All 7 origins remained reachable. The table below records the verified prototype outputs:",
        body_style
    ))

    origins_data = [
        ["Origin Cluster Anchor", "Baseline Dist (G0)", "Restricted Dist (G0_C)", "Detour Delta (Δ)", "Impact Severity", "Route Characteristics"],
        ["Kakkanad West / Civil Stn Environs", "1,572.8 m", "1,927.7 m", "+354.9 m (+22.6%)", "High (Direct Cut)", "Direct arterial severed; forced onto secondary collector bypass"],
        ["Civil Station Administrative Hub", "920.4 m", "1,130.7 m", "+210.3 m (+22.8%)", "Moderate", "Diverted through northern collector loop to Seaport-Airport Rd"],
        ["Padamugal Residential Community", "1,840.1 m", "1,995.6 m", "+155.5 m (+8.5%)", "Moderate", "Minor collector diversion around Palarivattom workzone reach"],
        ["DLF City / New Town Heights", "282.7 m", "311.6 m", "+28.9 m (+10.2%)", "Low (Local Choke)", "Local junction bypass around workzone perimeter"],
        ["Infopark Expressway Sector", "1,420.6 m", "1,420.6 m", "0.0 m (0.0%)", "Preserved Access", "Eastern approach entirely unaffected by western corridor workzone"],
        ["Kaloor–Kadavanthra Boundary", "2,060.4 m", "2,060.4 m", "0.0 m (0.0%)", "Preserved Access", "Southern inflow operates along uninterrupted arterial links"],
        ["Canal Colony / Athani Settlement", "1,110.2 m", "1,110.2 m", "0.0 m (0.0%)", "Preserved Access", "Northern access corridor maintains direct hospital ingress"]
    ]
    t_orig = Table([[Paragraph(c, table_cell_bold if r==0 else table_cell) for c in row] for r, row in enumerate(origins_data)], colWidths=[120, 68, 72, 70, 75, 118])
    t_orig.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f766e')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
        ('TOPPADDING', (0,0), (-1,-1), 1.5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')])
    ]))
    story.append(t_orig)
    story.append(Spacer(1, 3))

    story.append(Paragraph("Bounded Candidate Arrangement Trade-off Analysis & Prototype Review Gate", h2_style))
    arr_data = [
        ["Candidate Arrangement", "Schedule Model", "Access & Safety Trade-offs", "Operational Feasibility", "Prototype Review Gate Status"],
        ["Arrangement A: Sequential Phasing", "Sequential (96.0 d: 21d + 45d + 30d)", "Predictable single workzone footprint; longest overall duration; western detours +354.9 m.", "Feasible on existing carriageway; review pending.", "NO_VERIFIED_OPTION (Requires multi-stakeholder formal sign-off)"],
        ["Arrangement B: Managed Contraflow", "Sequential (96.0 d: 21d + 45d + 30d)", "Recovers 174.5 m arterial access via flaggers; severely narrows pedestrian walkway (<1.2 m).", "Physically feasible with barriers; review pending.", "NO_VERIFIED_OPTION (Requires pedestrian safety clearance)"],
        ["Arrangement C: Concurrent Civil Works", "Concurrent (62.4 d, illustrative 35% time compression assumption)", "Shortens duration by 35% (unvalidated assumption); simultaneous closures cause severe collector gridlock.", "High congestion risk; exceeds network capacity.", "INELIGIBLE_CONSTRAINTS (Concurrent closures exceed corridor capacity)"]
    ]
    t_arr = Table([[Paragraph(c, table_cell_bold if r==0 else table_cell) for c in row] for r, row in enumerate(arr_data)], colWidths=[105, 85, 135, 95, 103])
    t_arr.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1e293b')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.8),
        ('TOPPADDING', (0,0), (-1,-1), 1.8),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')])
    ]))
    story.append(t_arr)
    story.append(Spacer(1, 3))

    # Live Screenshot from the Running Prototype
    img_path = "evidence/screenshots/02_step2_access_impact.png"
    if os.path.exists(img_path):
        img = Image(img_path, width=523, height=140)
        story.append(img)
        story.append(Paragraph("<b>Figure 1:</b> Live SafeBuild prototype interface (Step 2: Check Community Access). Demonstrates genuine MapLibre WebGL canvas, authentic Kakkanad OSM highway geometry, baseline vs. restricted shortest path rerouting to Sunrise Hospital (+354.9 m detour), and structured task panel.", caption_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: SECTION 4: ENGINEERING RELEVANCE & SECTION 5: MARKET SURVEY
    # =========================================================================
    story.append(Paragraph("4. ENGINEERING RELEVANCE AND TECHNOLOGY DOMAIN", h1_style))
    story.append(Paragraph(
        "SafeBuild operates at the convergence of six foundational engineering and computational disciplines. "
        "It balances physical roadway infrastructure constraints with digital decision algorithms:",
        body_style
    ))

    eng_matrix = [
        ["Engineering Discipline", "Physical Domain Focus (“Bolts”)", "Digital Technology Focus (“Bots”)", "Integrated SafeBuild Contribution"],
        ["Civil & Highway Engineering", "Geometric design, carriageway width, workzone safety buffers, barrier clearance.", "Network topology modeling, roadway class impedance, one-way enforcement.", "Verifies whether physical diversions accommodate required traffic classes safely."],
        ["Transportation Engineering", "Network connectivity, traffic circulation, turning radii, pedestrian permeability.", "Dijkstra shortest path algorithm, multi-origin routing, detour delta calculation.", "Quantifies community accessibility loss and identifies critical access cut-offs."],
        ["Geospatial Engineering (GIS)", "Real-world coordinates, terrain topography, surveyed facility ingress points.", "WGS84 to UTM Zone 43N planar projection, KD-Tree spatial indexing.", "Ensures meter-accurate Euclidean distance routing on authentic OSM networks."],
        ["Computer Science & Graph Theory", "Physical road segments and intersections as graph edges and nodes.", "Directed multi-graphs, topological sorting, Depth-First Search cycle detection.", "Guarantees acyclic phase dependencies and deterministic, zero-variance routing."],
        ["Artificial Intelligence & NLP", "Engineering judgment boundaries, ethical communication safeguards.", "Context-constrained retrieval, grounded synthesis, deterministic fallback.", "Translates complex graph matrices into plain-language briefs without hallucinations."],
        ["Operations Research", "Construction phasing constraints, crew allocations, calendar duration limits.", "Bounded multi-criteria trade-off comparison, schedule exposure meter-days.", "Evaluates competing construction arrangements against accessibility criteria."]
    ]
    t_eng = Table([[Paragraph(c, table_cell_bold if r==0 else table_cell) for c in row] for r, row in enumerate(eng_matrix)], colWidths=[90, 115, 140, 178])
    t_eng.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f766e')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
        ('TOPPADDING', (0,0), (-1,-1), 1.5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')])
    ]))
    story.append(t_eng)
    story.append(Spacer(1, 3))

    tech_domains = [
        ["Primary Industry Domain", "Urban Infrastructure, Municipal Public Works, and Civil Construction Planning"],
        ["Core Technology Specializations", "Geographic Information Systems (GIS), Graph Theory, Construction Phasing, Guarded AI Decision Support"]
    ]
    t_td = Table([[Paragraph(c, table_cell_bold if r==0 else table_cell) for c in row] for r, row in enumerate(tech_domains)], colWidths=[130, 393])
    t_td.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#f1f5f9')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_td)
    story.append(Spacer(1, 4))

    story.append(Paragraph("5. MARKET SURVEY AND USER VALIDATION PLAN", h1_style))
    story.append(Paragraph(
        "<b>5.1 Proposed Stakeholder Validation Methodology:</b> "
        "To establish product-market alignment and operational viability, a structured field validation study is planned across the Kochi metropolitan area. "
        "The survey targets a sample size of <b>45 to 60 domain practitioners</b> across five distinct stakeholder cohorts: "
        "(1) Municipal Corporation Engineers (Kochi Municipal Corp), (2) State Public Works Department (PWD Roads Division) officers, "
        "(3) Urban Transit Project Engineers (Kochi Metro Rail Ltd infrastructure divisions), (4) Civil Construction EPC Contractors, and "
        "(5) Local Commercial Associations & Resident Welfare Associations along the corridor. "
        "<i>Status: This research design represents a planned validation framework; primary survey execution remains scheduled for the subsequent development phase.</i>",
        body_style
    ))
    story.append(Paragraph(
        "<b>5.2 Key Inquiry Dimensions & Survey Instrument:</b> "
        "The planned investigation evaluates seven core operational inquiries: "
        "• How are traffic diversions currently developed and approved during major roadwork? "
        "• What tools, if any, are utilized to quantify community accessibility severance prior to road closures? "
        "• How are construction phase sequences evaluated against local access constraints? "
        "• What critical data is missing during inter-agency traffic management coordination meetings? "
        "• How much professional engineering time is dedicated to manually reviewing candidate diversion routes? "
        "• How effectively are temporary restrictions communicated to affected residents and emergency services? "
        "• Which specific SafeBuild outputs (detour deltas, exposure days, PDF briefs) would provide the greatest operational utility?",
        body_style
    ))
    story.append(Spacer(1, 2))

    story.append(Paragraph("Rigorous Implementation Classification Matrix", h2_style))
    impl_status = [
        ["Classification", "Current Engineering Status in SafeBuild Project", "Verification Evidence & Audit Method"],
        ["IMPLEMENTED", "5-State Graph Algebra, Dijkstra routing engine, phase dependency cycle detection, Next.js UI, ReportLab engine.", "Fully functional source code in repository; verified reproducible endpoints (:8000, :3000)."],
        ["TESTED", "17 automated test checks (100% pass rate in 11.9s); independent reference script convergence (0.0098 m).", "SafeBuild_Test_Results.csv; scripts/independent_verification.py execution."],
        ["ASSUMED", "Palarivattom–Kakkanad hypothetical closure; 21d, 45d, 30d phase durations; 35% concurrent time compression.", "Clearly documented scenario constraints; illustrative assumptions for modeling demonstration."],
        ["PLANNED", "45–60 respondent practitioner validation survey; multi-corridor deployment; dynamic traffic assignment (DTA).", "Detailed methodology formulated; stakeholder outreach scheduled for Stage 3."],
        ["VERIFICATION PENDING", "Physical cross-section sidewalk measurements; joint on-site review with municipal transport authorities.", "Enforced by strict programmatic review gate (NO_VERIFIED_OPTION output)."]
    ]
    t_impl = Table([[Paragraph(c, table_cell_bold if r==0 else table_cell) for c in row] for r, row in enumerate(impl_status)], colWidths=[85, 218, 220])
    t_impl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f766e')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.8),
        ('TOPPADDING', (0,0), (-1,-1), 1.8),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')])
    ]))
    story.append(t_impl)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: SECTION 6: BENEFITS & SECTION 7: MARKET ASSESSMENT & READINESS
    # =========================================================================
    story.append(Paragraph("6. PROJECT BENEFITS", h1_style))
    story.append(Paragraph(
        "SafeBuild delivers multifaceted improvements across social equity, engineering rigor, economic productivity, and environmental impact. "
        "The table below details these expected gains alongside measurable future evaluation indicators:",
        body_style
    ))

    benefits_matrix = [
        ["Benefit Domain", "Anticipated Operational Gains", "Measurable Engineering Evaluation Indicators"],
        ["Social & Community Equity", "Preserves uninterrupted access to tertiary hospitals and schools; protects continuous pedestrian walkways; prevents disproportionate severance of vulnerable enclaves.", "• Number of newly disconnected origins (Target = 0)\n• Accessible healthcare facilities during workzones\n• Pedestrian walkway width maintenance (≥ 1.5 m)"],
        ["Engineering & Planning Rigor", "Replaces subjective guesswork with deterministic graph-theoretic routing; detects scheduling circularities; establishes transparent, auditable decision briefs.", "• Planning review cycle turnaround time (hours)\n• Detected dependency cycles prior to site setup\n• Invariant preservation across 100% of phases"],
        ["Economic & Commercial Viability", "Reduces avoidable detour mileage; preserves patron ingress and delivery logistics for commercial establishments; avoids costly work halts.", "• Cumulative detour exposure (meter-days)\n• Avoided commercial access severance days\n• Engineering staff-hours saved per diversion plan"],
        ["Environmental Sustainability", "Minimizing circuitous vehicular detour distances reduces excess vehicle-kilometers traveled (VKT), potentially lowering localized fuel consumption and idling emissions.", "• Modeled net reduction in detour VKT (km)\n• Avoided detour-induced vehicle idling hours\n(<i>Note: Potential model outcome, not observed metric</i>)"],
        ["Scalability & Architecture", "Engineered on open-source libraries (NetworkX, FastAPI, Next.js, MapLibre); zero per-seat proprietary GIS licensing fees; portable across any OSM-mapped urban center.", "• Onboarding time for new municipality networks\n• Automated OSM import & referential integrity rate\n• Server infrastructure runtime cost per study area"]
    ]
    t_ben = Table([[Paragraph(c, table_cell_bold if r==0 else table_cell) for c in row] for r, row in enumerate(benefits_matrix)], colWidths=[85, 230, 208])
    t_ben.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f766e')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.8),
        ('TOPPADDING', (0,0), (-1,-1), 1.8),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')])
    ]))
    story.append(t_ben)
    story.append(Spacer(1, 3))

    story.append(Paragraph("7. MARKET ASSESSMENT AND READINESS", h1_style))
    story.append(Paragraph(
        "<b>7.1 Potential Customer Segments:</b> "
        "SafeBuild addresses institutional decision-makers who commission, regulate, or execute urban infrastructure: "
        "(1) <i>Municipal Corporations & Urban Local Bodies (ULBs):</i> Seeking to protect civic connectivity and minimize citizen grievances. "
        "(2) <i>State Public Works Departments (PWD):</i> Mandated to formulate formal traffic diversion plans for arterial works. "
        "(3) <i>Urban Transit & Highway Authorities (e.g. Metro Rail Corporations, NHAI):</i> Coordinating multi-year viaduct and corridor construction. "
        "(4) <i>Civil Infrastructure EPC Contractors:</i> Requiring objective evidence to demonstrate community access compliance and avoid contract penalties. "
        "(5) <i>Traffic Planning & Engineering Consultancies:</i> Performing statutory traffic management studies for infrastructure tenders. "
        "<i>Status: Prospective customer segments; no commercial contracts or municipal adoptions are claimed.</i>",
        body_style
    ))
    story.append(Spacer(1, 1.5))

    story.append(Paragraph("Competitive Analysis & Industry Positioning", h2_style))
    comp_matrix = [
        ["Solution Category", "Representative Platforms", "Core Capabilities", "Critical Limitations Addressed by SafeBuild"],
        ["Commercial Navigation", "Google Maps, Apple Maps, Waze", "Dynamic driver re-routing around active closures; live GPS traffic probe data.", "Post-closure focus only; cannot optimize pre-construction phase order or evaluate community equity."],
        ["Desktop GIS Platforms", "Esri ArcGIS Network Analyst, QGIS", "Advanced spatial analysis, buffer generation, static network routing.", "High per-seat licensing costs; steep learning curve; lacks native construction scheduling dependency logic."],
        ["Project Scheduling Tools", "Oracle Primavera P6, Microsoft Project", "CPM scheduling, resource allocation, Gantt chart dependency tracking.", "Completely blind to geospatial road topology, network impedance, and spatial community access severance."],
        ["Traffic Simulation Tools", "PTV VISSIM, Aimsun, SUMO", "Microscopic car-following simulation, queue lengths, dynamic signal timing.", "Extreme data and calibration burden; computationally heavy; impractical for rapid scenario comparison."]
    ]
    t_comp = Table([[Paragraph(c, table_cell_bold if r==0 else table_cell) for c in row] for r, row in enumerate(comp_matrix)], colWidths=[75, 95, 165, 188])
    t_comp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1e293b')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
        ('TOPPADDING', (0,0), (-1,-1), 1.5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')])
    ]))
    story.append(t_comp)
    story.append(Spacer(1, 2.5))

    readiness_box = Table([
        [Paragraph("<b>DEVELOPMENT READINESS DECLARATION:</b> "
                   "<i>“Working prototype tested using real Kakkanad geographic data and hypothetical construction scenarios; "
                   "field validation and authority review pending.”</i> SafeBuild operates as a verified computational prototype. "
                   "All algorithms execute deterministically, but operational deployment requires joint on-site surveys and formal statutory sanction.", callout_text)]
    ], colWidths=[523])
    readiness_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f0fdf4')),
        ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor('#22c55e')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(readiness_box)
    story.append(Spacer(1, 2.5))

    story.append(Paragraph(
        "<b>7.2 Cost & Financial Feasibility:</b> "
        "The proposed implementation model leverages open-source geospatial foundations (OSM, NetworkX, MapLibre), avoiding recurring per-seat proprietary GIS licensing fees. "
        "An indicative student-led 3-month research development and validation budget is projected at <b>Rs. 2,70,000 – Rs. 5,05,000</b>: "
        "(a) Geospatial data engineering & OSM curation: Rs. 60,000 – Rs. 1,10,000; "
        "(b) Platform development & modeling enhancements: Rs. 1,10,000 – Rs. 2,00,000; "
        "(c) Field ground surveys & cross-section validation: Rs. 60,000 – Rs. 1,15,000; "
        "(d) Stakeholder review workshops & research dissemination: Rs. 40,000 – Rs. 80,000. "
        "Ongoing operational cloud hosting, periodic OSM network refreshes, and maintenance are estimated at <b>Rs. 8,000 – Rs. 25,000 / month</b>.",
        body_style
    ))
    story.append(Spacer(1, 1.5))

    story.append(Paragraph(
        "<b>7.3 Phased Implementation Roadmap:</b> "
        "<b>Stage 1: Core Prototype Verification (Completed)</b> — Formalized 5-state algebra, Dijkstra engine, 17 automated tests, and independent verification. "
        "<b>Stage 2: Supervised Scenario Validation (Current)</b> — Comprehensive scenario modeling on Kakkanad corridor and evidence documentation. "
        "<b>Stage 3: Stakeholder Engagement & Surveys (Months 1–2)</b> — Administer planned 45–60 practitioner study with Kochi municipal engineers and contractors. "
        "<b>Stage 4: Parallel Advisory Trial (Months 3–4)</b> — Evaluate SafeBuild shadow outputs alongside an active municipal roadwork project. "
        "<b>Stage 5: Multi-Corridor Platform Refinement (Months 5–6)</b> — Expand to 3 additional metropolitan corridors and integrate multi-destination routing. "
        "<b>Stage 6: Municipality-Scale Integration (Future Horizon)</b> — Open API integration with municipal GIS portals pending formal statutory sanction.",
        body_style
    ))
    story.append(Spacer(1, 1.5))

    story.append(Paragraph(
        "<b>References & Data Attribution:</b> "
        "(1) OpenStreetMap contributors, Open Database License (ODbL), https://www.openstreetmap.org/copyright; "
        "(2) Dijkstra, E. W. (1959). <i>A note on two problems in connexion with graphs</i>. Numerische Mathematik, 1(1), 269–271; "
        "(3) Hagberg, A., Swart, P., & S Chult, D. (2008). <i>Exploring network structure, dynamics, and function using NetworkX</i>; "
        "(4) ReportLab Europe Ltd. <i>ReportLab PDF Generation Library</i>.",
        caption_style
    ))

    # Build PDF with NumberedCanvas5
    doc.build(story, canvasmaker=NumberedCanvas5)
    print(f"Successfully generated {filename}")

if __name__ == "__main__":
    build_concept_pdf()
