import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=80, bottom=80, left=100, right=100):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'''
        <w:tcMar {nsdecls("w")}>
            <w:top w:w="{top}" w:type="dxa"/>
            <w:bottom w:w="{bottom}" w:type="dxa"/>
            <w:left w:w="{left}" w:type="dxa"/>
            <w:right w:w="{right}" w:type="dxa"/>
        </w:tcMar>
    ''')
    tcPr.append(tcMar)

def set_cell_border(cell, **kwargs):
    """
    kwargs: top, bottom, left, right
    values: dict(val='single', sz='4', color='CBD5E1', space='0')
    """
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(f'<w:tcBorders {nsdecls("w")}/>')
    for edge in ('top', 'left', 'bottom', 'right'):
        edge_data = kwargs.get(edge)
        if edge_data:
            tag = f'<w:{edge} {nsdecls("w")} w:val="{edge_data.get("val", "single")}" w:sz="{edge_data.get("sz", "4")}" w:space="0" w:color="{edge_data.get("color", "CBD5E1")}"/>'
            tcBorders.append(parse_xml(tag))
        else:
            tag = f'<w:{edge} {nsdecls("w")} w:val="none"/>'
            tcBorders.append(parse_xml(tag))
    tcPr.append(tcBorders)

def build_docx(filename="SafeBuild_Concept_Document_Final.docx"):
    doc = Document()

    # Set standard A4 portrait margins (18mm = 0.71 in)
    sections = doc.sections
    for section in sections:
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)
        section.top_margin = Inches(0.65)
        section.bottom_margin = Inches(0.65)
        section.left_margin = Inches(0.65)
        section.right_margin = Inches(0.65)

    # Styles
    navy = RGBColor(15, 23, 42)
    teal = RGBColor(15, 118, 110)
    slate = RGBColor(51, 65, 85)
    light_slate = RGBColor(100, 116, 139)

    # Base Normal Style
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Calibri'
    style_normal.font.size = Pt(9.5)
    style_normal.font.color.rgb = slate
    style_normal.paragraph_format.line_spacing = 1.15
    style_normal.paragraph_format.space_after = Pt(4)

    # Header / Title Block
    p_title = doc.add_paragraph()
    r_title = p_title.add_run("URBAN VISION AI — SAFEBUILD")
    r_title.bold = True
    r_title.font.size = Pt(20)
    r_title.font.color.rgb = navy
    p_title.paragraph_format.space_after = Pt(1)

    p_sub = doc.add_paragraph()
    r_sub = p_sub.add_run("“Plan roadwork. Keep communities connected.”")
    r_sub.font.size = Pt(11)
    r_sub.font.color.rgb = teal
    p_sub.paragraph_format.space_after = Pt(4)

    # Meta banner
    p_meta = doc.add_paragraph()
    p_meta.add_run("DOCUMENT TYPE: ").bold = True
    p_meta.add_run("Engineering Innovation Concept Document  |  ")
    p_meta.add_run("FOCUS: ").bold = True
    p_meta.add_run("Pre-Construction Access Optimization  |  ")
    p_meta.add_run("CASE STUDY: ").bold = True
    p_meta.add_run("Kakkanad Corridor, Kochi, Kerala")
    p_meta.runs[0].font.size = Pt(8)
    for r in p_meta.runs[1:]:
        r.font.size = Pt(8)
        r.font.color.rgb = light_slate
    p_meta.paragraph_format.space_after = Pt(6)

    # Notice callout
    tbl_notice = doc.add_table(rows=1, cols=1)
    tbl_notice.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_notice = tbl_notice.cell(0, 0)
    c_notice.width = Inches(6.97)
    set_cell_background(c_notice, "FEF2F2")
    set_cell_border(c_notice, top=dict(color="F87171", sz="8"), bottom=dict(color="F87171", sz="8"), left=dict(color="F87171", sz="8"), right=dict(color="F87171", sz="8"))
    set_cell_margins(c_notice, top=100, bottom=100, left=140, right=140)
    p_not = c_notice.paragraphs[0]
    p_not.paragraph_format.space_after = Pt(0)
    r_not_b = p_not.add_run("EVALUATION NOTICE & REGULATORY BOUNDARY: ")
    r_not_b.bold = True
    r_not_b.font.size = Pt(8)
    r_not_b.font.color.rgb = RGBColor(185, 28, 28)
    r_not_t = p_not.add_run(
        "SafeBuild is an analytical decision-support research prototype for evaluating community accessibility during planned roadway works. "
        "All simulated routes represent deterministic graph-theoretic shortest path traversals (Dijkstra algorithm) and DO NOT "
        "constitute approved traffic circulation plans, live emergency response routing, or real-time travel delay predictions. "
        "Physical interventions require formal statutory review from municipal transport departments and relevant public works bodies."
    )
    r_not_t.font.size = Pt(8)
    r_not_t.font.color.rgb = RGBColor(153, 27, 27)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # 1. PROBLEM DEFINITION
    h1 = doc.add_paragraph()
    r_h1 = h1.add_run("1. PROBLEM DEFINITION")
    r_h1.bold = True
    r_h1.font.size = Pt(13)
    r_h1.font.color.rgb = navy
    h1.paragraph_format.space_before = Pt(6)
    h1.paragraph_format.space_after = Pt(3)

    p1 = doc.add_paragraph()
    p1.add_run("1.1 The Urban Roadwork Accessibility Challenge: ").bold = True
    p1.add_run(
        "Municipal infrastructure civil works—such as metro rail viaduct construction, storm-water drainage renewal, utility trenching, "
        "and flyover foundation piling—are indispensable for long-term urban economic productivity. However, temporary roadway restrictions "
        "frequently sever critical transit arteries linking residential communities to essential civic destinations, including tertiary healthcare facilities, "
        "schools, workplaces, and public transportation interchanges. When multiple workzones are executed concurrently without comprehensive network analysis, "
        "entire residential enclaves can suffer severe connectivity degradation, turning short routine trips into protracted, circuitous detours."
    )

    p2 = doc.add_paragraph()
    p2.add_run("Differential Impacts on Vulnerable Road Users: ").bold = True
    p2.add_run(
        "Disruption impacts are not distributed equally across urban populations. While motorized vehicles face additional travel distances and congestion delays, "
        "pedestrians, older adults, and persons with disabilities experience severe mobility barriers. Roadwork barricades often encroach upon footpaths, "
        "forcing pedestrians into live traffic lanes or eliminating continuous pedestrian crossings. Concurrently, local commercial establishments depend on "
        "unobstructed freight delivery corridors and patron footfall, which are abruptly curtailed during extended roadbed closures."
    )

    p3 = doc.add_paragraph()
    p3.add_run("1.2 The Limitations of Post-Disruption Route Navigation: ").bold = True
    p3.add_run(
        "Contemporary commercial navigation applications (e.g., Google Maps, Apple Maps, Waze) perform exceptionally well at dynamic re-routing "
        "after an active road closure, incident, or severe traffic bottleneck has already occurred. However, these tools operate downstream of civil engineering decisions. "
        "They inform individual drivers of congestion but cannot inform planners how work should be organized to prevent severance in the first place."
    )

    p4 = doc.add_paragraph()
    p4.add_run("The Central Civil Engineering Challenge: ").bold = True
    p4.add_run(
        "Urban roadway workzones pose a multi-dimensional planning challenge: Can civil engineers and municipal authorities evaluate and restructure the "
        "sequencing, spatial phasing, and temporary mitigation arrangements of roadwork before breaking ground, so that communities retain practical, continuous access? "
        "Solving this challenge requires uniting topological network impedance, construction phase dependencies, and physical right-of-way constraints into an "
        "auditable, pre-construction decision-support framework."
    )

    p5 = doc.add_paragraph()
    p5.add_run("1.3 Case Study: Kakkanad Corridor Scenario Study (Kochi, Kerala): ").bold = True
    p5.add_run(
        "To establish empirical validity on genuine urban geometry, SafeBuild was applied to a defined study corridor along the Palarivattom–Kakkanad Road "
        "in the Kochi metropolitan area, Kerala, India. The baseline road network was parsed directly from OpenStreetMap under the Open Database License (ODbL), "
        "capturing 19,582 nodes, 11,675 motor vehicle highway edges, and 16,842 pedestrian edges within a 4.67 km² core boundary (projected to UTM Zone 43N). "
        "The scenario models hypothetical road restrictions along arterial segments (OSM Way IDs 197827530 and 383253303) affecting community connectivity to "
        "Sunrise Hospital (Vii/528-B Seaport-Airport Road) from seven representative residential cluster centroids. "
        "(Note: This scenario represents an unverified planning research model; it does not reflect an actual municipal closure or completed field pilot)."
    )

    # Table 1: Case study metadata
    tbl_case = doc.add_table(rows=5, cols=3)
    tbl_case.alignment = WD_TABLE_ALIGNMENT.CENTER
    case_headers = ["Dataset Dimension", "Attribute Value", "Geospatial Reference & Verification Mechanism"]
    case_data = [
        ["Study Corridor Boundary", "76.3262, 9.9934 to 76.3688, 10.0276 (EPSG:4326)", "4.67 km² core perimeter with 6.8 km regional buffer in UTM Zone 43N"],
        ["Network Topology", "19,582 nodes, 11,675 motor edges, 16,842 pedestrian edges", "Raw OSM XML referential audit (0 missing node references)"],
        ["Target Destination", "Sunrise Hospital, Ernakulam (lat: 10.0215, lon: 76.3478)", "Ground-surveyed entrance node snapped via Euclidean KD-Tree"],
        ["Restricted Workzone", "Palarivattom–Kakkanad Road (OSM Way IDs: 197827530, 383253303)", "Full bidirectional carriage restriction (Simulated State G0_C)"]
    ]
    col_w = [Inches(1.5), Inches(2.4), Inches(3.07)]
    for j, h in enumerate(case_headers):
        cell = tbl_case.cell(0, j)
        cell.width = col_w[j]
        set_cell_background(cell, "0F766E")
        set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(8)
        r.font.color.rgb = RGBColor(255, 255, 255)

    for i, row in enumerate(case_data):
        bg = "FFFFFF" if i % 2 == 0 else "F8FAFC"
        for j, val in enumerate(row):
            cell = tbl_case.cell(i+1, j)
            cell.width = col_w[j]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=50, bottom=50, left=80, right=80)
            set_cell_border(cell, top=dict(color="CBD5E1", sz="4"), bottom=dict(color="CBD5E1", sz="4"), left=dict(color="CBD5E1", sz="4"), right=dict(color="CBD5E1", sz="4"))
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(val)
            r.font.size = Pt(7.5)
            if j == 0:
                r.bold = True

    doc.add_page_break()

    # 2. IDEA / CONCEPT / SOLUTION TO ADDRESS THE PROBLEM
    h2 = doc.add_paragraph()
    r_h2 = h2.add_run("2. IDEA / CONCEPT / SOLUTION TO ADDRESS THE PROBLEM")
    r_h2.bold = True
    r_h2.font.size = Pt(13)
    r_h2.font.color.rgb = navy
    h2.paragraph_format.space_before = Pt(4)
    h2.paragraph_format.space_after = Pt(3)

    p_pg_intro = doc.add_paragraph()
    p_pg_intro.add_run("2.1 Customer Pains vs. Solution Gains: ").bold = True
    p_pg_intro.add_run(
        "Municipal transport engineers, public works departments, and civil contractors face chronic friction when coordinating construction schedules with urban access. "
        "SafeBuild translates these operational pain points into structured engineering gains:"
    )

    tbl_pg = doc.add_table(rows=5, cols=3)
    tbl_pg.alignment = WD_TABLE_ALIGNMENT.CENTER
    pg_headers = ["Stakeholder Cohort", "Operational Pain Points (Current Practice)", "Engineered Gains (SafeBuild Decision Framework)"]
    pg_data = [
        ["Municipal Engineers & PWD", "Manual, siloed scheduling; zero spatial visibility into cumulative community cut-off across overlapping project phases.", "Multi-phase network simulation mapping exact access severance before breaking ground; automated metric audits."],
        ["Traffic Police & Planners", "Ad-hoc diversion approvals; secondary collector roads overwhelmed by uncoordinated detours and sharp turn choke points.", "Deterministic shortest-path detour quantification across all neighborhood centroids; turning restriction compliance."],
        ["Infrastructure Contractors", "Public outrage, unexpected project halts, and costly emergency re-sequencing due to unannounced access severance.", "Pre-validated construction phase dependencies; objective trade-off documentation demonstrating planning diligence."],
        ["Affected Communities", "Sudden loss of access to healthcare, schools, and transit; dangerous pedestrian detours forced into active traffic lanes.", "Preserved essential-service connectivity; transparent, phase-specific access plans; protected pedestrian walkways."]
    ]
    col_w_pg = [Inches(1.4), Inches(2.7), Inches(2.87)]
    for j, h in enumerate(pg_headers):
        cell = tbl_pg.cell(0, j)
        cell.width = col_w_pg[j]
        set_cell_background(cell, "0F766E")
        set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(8)
        r.font.color.rgb = RGBColor(255, 255, 255)

    for i, row in enumerate(pg_data):
        bg = "FFFFFF" if i % 2 == 0 else "F8FAFC"
        for j, val in enumerate(row):
            cell = tbl_pg.cell(i+1, j)
            cell.width = col_w_pg[j]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=50, bottom=50, left=80, right=80)
            set_cell_border(cell, top=dict(color="CBD5E1", sz="4"), bottom=dict(color="CBD5E1", sz="4"), left=dict(color="CBD5E1", sz="4"), right=dict(color="CBD5E1", sz="4"))
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(val)
            r.font.size = Pt(7.5)
            if j == 0:
                r.bold = True

    doc.add_paragraph().paragraph_format.space_after = Pt(3)

    p_arch = doc.add_paragraph()
    p_arch.add_run("2.2 Core System Architecture & Modular Components: ").bold = True
    p_arch.add_run(
        "SafeBuild operates as an end-to-end decision-support platform comprising eight integrated modules: "
        "(1) Interactive GIS Planning Studio: WebGL canvas rendering 2D/3D extruded structures and real-time routes. "
        "(2) Network Preparation Engine: Ingests raw OSM XML, constructs directed MultiDiGraphs in UTM Zone 43N, and projects origins via KD-Tree. "
        "(3) 5-State Subgraph Algebra: Formally tracks baseline, closed, proposed, and mitigated states (G0 to G0_P_C_M). "
        "(4) Deterministic Routing Engine: Computes exact Dijkstra shortest paths with zero statistical variance. "
        "(5) Construction Dependency Validator: Topological sorting and cycle detection across construction phases. "
        "(6) Bounded Scenario Comparison Ledger: Rigorously compares candidate arrangements against physical and safety constraints. "
        "(7) Guarded AI Explanation Layer: Synthesizes analytical findings strictly quoting backend metrics with deterministic fallback. "
        "(8) Engineering Report Generator: Exports self-contained, auditable PDF decision briefs and CSV tables."
    )

    p_usp = doc.add_paragraph()
    p_usp.add_run("2.3 Unique Selling Proposition (USP): ").bold = True
    p_usp.add_run(
        "The definitive differentiator of SafeBuild is its focus on the upstream civil engineering decision: "
        "SafeBuild evaluates how construction activities should be sequenced and coordinated to preserve community access before work commences, "
        "rather than merely directing vehicles around road closures after they occur. "
        "While specialized GIS platforms (ArcGIS/QGIS) perform spatial queries, they lack construction scheduling dependencies. Conversely, project scheduling tools "
        "(Primavera P6, MS Project) lack topological road network awareness. SafeBuild unites these capabilities into a focused, community-first planning workflow."
    )

    # 3. PROJECT DESCRIPTION AND HIGH-LEVEL DESIGN
    h3 = doc.add_paragraph()
    r_h3 = h3.add_run("3. PROJECT DESCRIPTION AND HIGH-LEVEL DESIGN")
    r_h3.bold = True
    r_h3.font.size = Pt(13)
    r_h3.font.color.rgb = navy
    h3.paragraph_format.space_before = Pt(4)
    h3.paragraph_format.space_after = Pt(3)

    p_flow_intro = doc.add_paragraph()
    p_flow_intro.add_run(
        "SafeBuild structures construction access planning into a six-step engineering workflow: "
        "1. Define Construction Area & Restrictions (target OSM ways, duration, phases) → "
        "2. Prepare Phase-Specific Subgraphs (formal 5-state algebra G0 to G0_P_C_M) → "
        "3. Analyze Community Accessibility (Dijkstra shortest paths, reachability distinction) → "
        "4. Compare Construction Arrangements (schedule exposure, candidate trade-offs) → "
        "5. Explain Results via Guarded AI (grounded metric citations, strict refusal of hallucinations) → "
        "6. Generate Access Plans & Audit Documentation (self-contained briefs, review gates)."
    )

    doc.add_page_break()

    # SECTION 3 (PART 2): PROTOTYPE EVIDENCE & CASE STUDY
    h3_2 = doc.add_paragraph()
    r_h3_2 = h3_2.add_run("3. PROJECT DESCRIPTION AND HIGH-LEVEL DESIGN (CONTINUED)")
    r_h3_2.bold = True
    r_h3_2.font.size = Pt(13)
    r_h3_2.font.color.rgb = navy
    h3_2.paragraph_format.space_before = Pt(4)
    h3_2.paragraph_format.space_after = Pt(3)

    p_evi_intro = doc.add_paragraph()
    p_evi_intro.add_run("Grounded Prototype Evidence: Kakkanad Scenario Study Routing: ").bold = True
    p_evi_intro.add_run(
        "In the evaluated Kakkanad corridor scenario, seven representative residential cluster centroids were routed to Sunrise Hospital under baseline (G0) "
        "and restricted (G0_C) conditions. All 7 origins remained reachable. The table below records the verified prototype outputs:"
    )

    tbl_orig = doc.add_table(rows=8, cols=6)
    tbl_orig.alignment = WD_TABLE_ALIGNMENT.CENTER
    orig_headers = ["Origin Cluster Anchor", "Baseline (G0)", "Restricted (G0_C)", "Detour Delta (Δ)", "Impact Severity", "Route Characteristics"]
    orig_data = [
        ["Kakkanad West / Civil Stn Environs", "1,572.8 m", "1,927.7 m", "+354.9 m (+22.6%)", "High (Direct Cut)", "Direct arterial severed; forced onto secondary collector bypass"],
        ["Civil Station Administrative Hub", "920.4 m", "1,130.7 m", "+210.3 m (+22.8%)", "Moderate", "Diverted through northern collector loop to Seaport-Airport Rd"],
        ["Padamugal Residential Community", "1,840.1 m", "1,995.6 m", "+155.5 m (+8.5%)", "Moderate", "Minor collector diversion around Palarivattom workzone reach"],
        ["DLF City / New Town Heights", "282.7 m", "311.6 m", "+28.9 m (+10.2%)", "Low (Local Choke)", "Local junction bypass around workzone perimeter"],
        ["Infopark Expressway Sector", "1,420.6 m", "1,420.6 m", "0.0 m (0.0%)", "Preserved Access", "Eastern approach entirely unaffected by western corridor workzone"],
        ["Kaloor–Kadavanthra Boundary", "2,060.4 m", "2,060.4 m", "0.0 m (0.0%)", "Preserved Access", "Southern inflow operates along uninterrupted arterial links"],
        ["Canal Colony / Athani Settlement", "1,110.2 m", "1,110.2 m", "0.0 m (0.0%)", "Preserved Access", "Northern access corridor maintains direct hospital ingress"]
    ]
    col_w_orig = [Inches(1.6), Inches(0.9), Inches(1.0), Inches(1.0), Inches(1.0), Inches(1.47)]
    for j, h in enumerate(orig_headers):
        cell = tbl_orig.cell(0, j)
        cell.width = col_w_orig[j]
        set_cell_background(cell, "0F766E")
        set_cell_margins(cell, top=50, bottom=50, left=60, right=60)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(7.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    for i, row in enumerate(orig_data):
        bg = "FFFFFF" if i % 2 == 0 else "F8FAFC"
        for j, val in enumerate(row):
            cell = tbl_orig.cell(i+1, j)
            cell.width = col_w_orig[j]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=40, bottom=40, left=60, right=60)
            set_cell_border(cell, top=dict(color="CBD5E1", sz="4"), bottom=dict(color="CBD5E1", sz="4"), left=dict(color="CBD5E1", sz="4"), right=dict(color="CBD5E1", sz="4"))
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(val)
            r.font.size = Pt(7)
            if j == 0:
                r.bold = True

    doc.add_paragraph().paragraph_format.space_after = Pt(3)

    p_arr_intro = doc.add_paragraph()
    p_arr_intro.add_run("Bounded Candidate Arrangement Trade-off Analysis & Prototype Review Gate: ").bold = True
    p_arr_intro.add_run(
        "Candidate arrangements were evaluated against physical right-of-way constraints, schedule duration, and worker safety:"
    )

    tbl_arr = doc.add_table(rows=4, cols=5)
    tbl_arr.alignment = WD_TABLE_ALIGNMENT.CENTER
    arr_headers = ["Candidate Arrangement", "Schedule Model", "Access & Safety Trade-offs", "Operational Feasibility", "Review Gate Status"]
    arr_data = [
        ["Arrangement A: Sequential Phasing", "Sequential (96.0 d: 21d + 45d + 30d)", "Predictable single workzone footprint; longest overall duration; western detours +354.9 m.", "Feasible on existing carriageway; review pending.", "NO_VERIFIED_OPTION (Requires multi-stakeholder formal sign-off)"],
        ["Arrangement B: Managed Contraflow", "Sequential (96.0 d: 21d + 45d + 30d)", "Recovers 174.5 m arterial access via flaggers; severely narrows pedestrian walkway (<1.2 m).", "Physically feasible with barriers; review pending.", "NO_VERIFIED_OPTION (Requires pedestrian safety clearance)"],
        ["Arrangement C: Concurrent Civil Works", "Concurrent (62.4 d, illustrative 35% time compression assumption)", "Shortens duration by 35% (unvalidated assumption); simultaneous closures cause severe collector gridlock.", "High congestion risk; exceeds network capacity.", "INELIGIBLE_CONSTRAINTS (Concurrent closures exceed corridor capacity)"]
    ]
    col_w_arr = [Inches(1.4), Inches(1.2), Inches(1.8), Inches(1.2), Inches(1.37)]
    for j, h in enumerate(arr_headers):
        cell = tbl_arr.cell(0, j)
        cell.width = col_w_arr[j]
        set_cell_background(cell, "1E293B")
        set_cell_margins(cell, top=50, bottom=50, left=60, right=60)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(7.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    for i, row in enumerate(arr_data):
        bg = "FFFFFF" if i % 2 == 0 else "F8FAFC"
        for j, val in enumerate(row):
            cell = tbl_arr.cell(i+1, j)
            cell.width = col_w_arr[j]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=40, bottom=40, left=60, right=60)
            set_cell_border(cell, top=dict(color="CBD5E1", sz="4"), bottom=dict(color="CBD5E1", sz="4"), left=dict(color="CBD5E1", sz="4"), right=dict(color="CBD5E1", sz="4"))
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(val)
            r.font.size = Pt(7)
            if j == 0:
                r.bold = True

    # Screenshot
    img_path = "evidence/screenshots/02_step2_access_impact.png"
    if os.path.exists(img_path):
        doc.add_paragraph().paragraph_format.space_after = Pt(2)
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_after = Pt(2)
        p_img.add_run().add_picture(img_path, width=Inches(6.8))

        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_cap = p_cap.add_run(
            "Figure 1: Live SafeBuild prototype interface (Step 2: Check Community Access). Demonstrates genuine MapLibre WebGL canvas, "
            "authentic Kakkanad OSM highway geometry, baseline vs. restricted shortest path rerouting to Sunrise Hospital (+354.9 m detour), and structured task panel."
        )
        r_cap.font.size = Pt(7.5)
        r_cap.font.italic = True
        r_cap.font.color.rgb = light_slate
        p_cap.paragraph_format.space_after = Pt(4)

    doc.add_page_break()

    # 4. ENGINEERING RELEVANCE AND TECHNOLOGY DOMAIN
    h4 = doc.add_paragraph()
    r_h4 = h4.add_run("4. ENGINEERING RELEVANCE AND TECHNOLOGY DOMAIN")
    r_h4.bold = True
    r_h4.font.size = Pt(13)
    r_h4.font.color.rgb = navy
    h4.paragraph_format.space_before = Pt(4)
    h4.paragraph_format.space_after = Pt(3)

    p_eng_intro = doc.add_paragraph()
    p_eng_intro.add_run(
        "SafeBuild operates at the convergence of six foundational engineering and computational disciplines. "
        "It balances physical roadway infrastructure constraints with digital decision algorithms:"
    )

    tbl_eng = doc.add_table(rows=7, cols=4)
    tbl_eng.alignment = WD_TABLE_ALIGNMENT.CENTER
    eng_headers = ["Engineering Discipline", "Physical Domain Focus (“Bolts”)", "Digital Technology Focus (“Bots”)", "Integrated SafeBuild Contribution"]
    eng_data = [
        ["Civil & Highway Engineering", "Geometric design, carriageway width, workzone safety buffers, barrier clearance.", "Network topology modeling, roadway class impedance, one-way enforcement.", "Verifies whether physical diversions accommodate required traffic classes safely."],
        ["Transportation Engineering", "Network connectivity, traffic circulation, turning radii, pedestrian permeability.", "Dijkstra shortest path algorithm, multi-origin routing, detour delta calculation.", "Quantifies community accessibility loss and identifies critical access cut-offs."],
        ["Geospatial Engineering (GIS)", "Real-world coordinates, terrain topography, surveyed facility ingress points.", "WGS84 to UTM Zone 43N planar projection, KD-Tree spatial indexing.", "Ensures meter-accurate Euclidean distance routing on authentic OSM networks."],
        ["Computer Science & Graph Theory", "Physical road segments and intersections as graph edges and nodes.", "Directed multi-graphs, topological sorting, Depth-First Search cycle detection.", "Guarantees acyclic phase dependencies and deterministic, zero-variance routing."],
        ["Artificial Intelligence & NLP", "Engineering judgment boundaries, ethical communication safeguards.", "Context-constrained retrieval, grounded synthesis, deterministic fallback.", "Translates complex graph matrices into plain-language briefs without hallucinations."],
        ["Operations Research", "Construction phasing constraints, crew allocations, calendar duration limits.", "Bounded multi-criteria trade-off comparison, schedule exposure meter-days.", "Evaluates competing construction arrangements against accessibility criteria."]
    ]
    col_w_eng = [Inches(1.2), Inches(1.5), Inches(1.8), Inches(2.47)]
    for j, h in enumerate(eng_headers):
        cell = tbl_eng.cell(0, j)
        cell.width = col_w_eng[j]
        set_cell_background(cell, "0F766E")
        set_cell_margins(cell, top=50, bottom=50, left=60, right=60)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(7.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    for i, row in enumerate(eng_data):
        bg = "FFFFFF" if i % 2 == 0 else "F8FAFC"
        for j, val in enumerate(row):
            cell = tbl_eng.cell(i+1, j)
            cell.width = col_w_eng[j]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=40, bottom=40, left=60, right=60)
            set_cell_border(cell, top=dict(color="CBD5E1", sz="4"), bottom=dict(color="CBD5E1", sz="4"), left=dict(color="CBD5E1", sz="4"), right=dict(color="CBD5E1", sz="4"))
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(val)
            r.font.size = Pt(7)
            if j == 0:
                r.bold = True

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # 5. MARKET SURVEY AND USER VALIDATION PLAN
    h5 = doc.add_paragraph()
    r_h5 = h5.add_run("5. MARKET SURVEY AND USER VALIDATION PLAN")
    r_h5.bold = True
    r_h5.font.size = Pt(13)
    r_h5.font.color.rgb = navy
    h5.paragraph_format.space_before = Pt(4)
    h5.paragraph_format.space_after = Pt(3)

    p_surv1 = doc.add_paragraph()
    p_surv1.add_run("5.1 Proposed Stakeholder Validation Methodology: ").bold = True
    p_surv1.add_run(
        "To establish product-market alignment and operational viability, a structured field validation study is planned across the Kochi metropolitan area. "
        "The survey targets a sample size of 45 to 60 domain practitioners across five distinct stakeholder cohorts: "
        "(1) Municipal Corporation Engineers (Kochi Municipal Corp), (2) State Public Works Department (PWD Roads Division) officers, "
        "(3) Urban Transit Project Engineers (Kochi Metro Rail Ltd infrastructure divisions), (4) Civil Construction EPC Contractors, and "
        "(5) Local Commercial Associations & Resident Welfare Associations along the corridor. "
        "(Status: This research design represents a planned validation framework; primary survey execution remains scheduled for the subsequent development phase)."
    )

    p_surv2 = doc.add_paragraph()
    p_surv2.add_run("5.2 Key Inquiry Dimensions & Survey Instrument: ").bold = True
    p_surv2.add_run(
        "The planned investigation evaluates seven core operational inquiries: "
        "• How are traffic diversions currently developed and approved during major roadwork? "
        "• What tools, if any, are utilized to quantify community accessibility severance prior to road closures? "
        "• How are construction phase sequences evaluated against local access constraints? "
        "• What critical data is missing during inter-agency traffic management coordination meetings? "
        "• How much professional engineering time is dedicated to manually reviewing candidate diversion routes? "
        "• How effectively are temporary restrictions communicated to affected residents and emergency services? "
        "• Which specific SafeBuild outputs (detour deltas, exposure days, PDF briefs) would provide the greatest operational utility?"
    )

    p_impl_intro = doc.add_paragraph()
    p_impl_intro.add_run("Rigorous Implementation Classification Matrix: ").bold = True

    tbl_impl = doc.add_table(rows=6, cols=3)
    tbl_impl.alignment = WD_TABLE_ALIGNMENT.CENTER
    impl_headers = ["Classification", "Current Engineering Status in SafeBuild Project", "Verification Evidence & Audit Method"]
    impl_data = [
        ["IMPLEMENTED", "5-State Graph Algebra, Dijkstra routing engine, phase dependency cycle detection, Next.js UI, ReportLab engine.", "Fully functional source code in repository; verified reproducible endpoints (:8000, :3000)."],
        ["TESTED", "17 automated test checks (100% pass rate in 11.9s); independent reference script convergence (0.0098 m).", "SafeBuild_Test_Results.csv; scripts/independent_verification.py execution."],
        ["ASSUMED", "Palarivattom–Kakkanad hypothetical closure; 21d, 45d, 30d phase durations; 35% concurrent time compression.", "Clearly documented scenario constraints; illustrative assumptions for modeling demonstration."],
        ["PLANNED", "45–60 respondent practitioner validation survey; multi-corridor deployment; dynamic traffic assignment (DTA).", "Detailed methodology formulated; stakeholder outreach scheduled for Stage 3."],
        ["VERIFICATION PENDING", "Physical cross-section sidewalk measurements; joint on-site review with municipal transport authorities.", "Enforced by strict programmatic review gate (NO_VERIFIED_OPTION output)."]
    ]
    col_w_impl = [Inches(1.2), Inches(2.8), Inches(2.97)]
    for j, h in enumerate(impl_headers):
        cell = tbl_impl.cell(0, j)
        cell.width = col_w_impl[j]
        set_cell_background(cell, "0F766E")
        set_cell_margins(cell, top=50, bottom=50, left=60, right=60)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(7.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    for i, row in enumerate(impl_data):
        bg = "FFFFFF" if i % 2 == 0 else "F8FAFC"
        for j, val in enumerate(row):
            cell = tbl_impl.cell(i+1, j)
            cell.width = col_w_impl[j]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=40, bottom=40, left=60, right=60)
            set_cell_border(cell, top=dict(color="CBD5E1", sz="4"), bottom=dict(color="CBD5E1", sz="4"), left=dict(color="CBD5E1", sz="4"), right=dict(color="CBD5E1", sz="4"))
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(val)
            r.font.size = Pt(7)
            if j == 0:
                r.bold = True

    doc.add_page_break()

    # 6. PROJECT BENEFITS
    h6 = doc.add_paragraph()
    r_h6 = h6.add_run("6. PROJECT BENEFITS")
    r_h6.bold = True
    r_h6.font.size = Pt(13)
    r_h6.font.color.rgb = navy
    h6.paragraph_format.space_before = Pt(4)
    h6.paragraph_format.space_after = Pt(3)

    p_ben_intro = doc.add_paragraph()
    p_ben_intro.add_run(
        "SafeBuild delivers multifaceted improvements across social equity, engineering rigor, economic productivity, and environmental impact. "
        "The table below details these expected gains alongside measurable future evaluation indicators:"
    )

    tbl_ben = doc.add_table(rows=6, cols=3)
    tbl_ben.alignment = WD_TABLE_ALIGNMENT.CENTER
    ben_headers = ["Benefit Domain", "Anticipated Operational Gains", "Measurable Engineering Evaluation Indicators"]
    ben_data = [
        ["Social & Community Equity", "Preserves uninterrupted access to tertiary hospitals and schools; protects continuous pedestrian walkways; prevents disproportionate severance of vulnerable enclaves.", "• Number of newly disconnected origins (Target = 0)\n• Accessible healthcare facilities during workzones\n• Pedestrian walkway width maintenance (≥ 1.5 m)"],
        ["Engineering & Planning Rigor", "Replaces subjective guesswork with deterministic graph-theoretic routing; detects scheduling circularities; establishes transparent, auditable decision briefs.", "• Planning review cycle turnaround time (hours)\n• Detected dependency cycles prior to site setup\n• Invariant preservation across 100% of phases"],
        ["Economic & Commercial Viability", "Reduces avoidable detour mileage; preserves patron ingress and delivery logistics for commercial establishments; avoids costly work halts.", "• Cumulative detour exposure (meter-days)\n• Avoided commercial access severance days\n• Engineering staff-hours saved per diversion plan"],
        ["Environmental Sustainability", "Minimizing circuitous vehicular detour distances reduces excess vehicle-kilometers traveled (VKT), potentially lowering localized fuel consumption and idling emissions.", "• Modeled net reduction in detour VKT (km)\n• Avoided detour-induced vehicle idling hours\n(Note: Potential model outcome, not observed metric)"],
        ["Scalability & Architecture", "Engineered on open-source libraries (NetworkX, FastAPI, Next.js, MapLibre); zero per-seat proprietary GIS licensing fees; portable across any OSM-mapped urban center.", "• Onboarding time for new municipality networks\n• Automated OSM import & referential integrity rate\n• Server infrastructure runtime cost per study area"]
    ]
    col_w_ben = [Inches(1.2), Inches(3.0), Inches(2.77)]
    for j, h in enumerate(ben_headers):
        cell = tbl_ben.cell(0, j)
        cell.width = col_w_ben[j]
        set_cell_background(cell, "0F766E")
        set_cell_margins(cell, top=50, bottom=50, left=60, right=60)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(7.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    for i, row in enumerate(ben_data):
        bg = "FFFFFF" if i % 2 == 0 else "F8FAFC"
        for j, val in enumerate(row):
            cell = tbl_ben.cell(i+1, j)
            cell.width = col_w_ben[j]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=40, bottom=40, left=60, right=60)
            set_cell_border(cell, top=dict(color="CBD5E1", sz="4"), bottom=dict(color="CBD5E1", sz="4"), left=dict(color="CBD5E1", sz="4"), right=dict(color="CBD5E1", sz="4"))
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(val)
            r.font.size = Pt(7)
            if j == 0:
                r.bold = True

    doc.add_paragraph().paragraph_format.space_after = Pt(3)

    # 7. MARKET ASSESSMENT AND READINESS
    h7 = doc.add_paragraph()
    r_h7 = h7.add_run("7. MARKET ASSESSMENT AND READINESS")
    r_h7.bold = True
    r_h7.font.size = Pt(13)
    r_h7.font.color.rgb = navy
    h7.paragraph_format.space_before = Pt(4)
    h7.paragraph_format.space_after = Pt(3)

    p_cust = doc.add_paragraph()
    p_cust.add_run("7.1 Potential Customer Segments: ").bold = True
    p_cust.add_run(
        "SafeBuild addresses institutional decision-makers who commission, regulate, or execute urban infrastructure: "
        "(1) Municipal Corporations & Urban Local Bodies (ULBs): Seeking to protect civic connectivity and minimize citizen grievances. "
        "(2) State Public Works Departments (PWD): Mandated to formulate formal traffic diversion plans for arterial works. "
        "(3) Urban Transit & Highway Authorities (e.g. Metro Rail Corporations, NHAI): Coordinating multi-year viaduct and corridor construction. "
        "(4) Civil Infrastructure EPC Contractors: Requiring objective evidence to demonstrate community access compliance and avoid contract penalties. "
        "(5) Traffic Planning & Engineering Consultancies: Performing statutory traffic management studies for infrastructure tenders. "
        "(Status: Prospective customer segments; no commercial contracts or municipal adoptions are claimed)."
    )

    tbl_comp = doc.add_table(rows=5, cols=4)
    tbl_comp.alignment = WD_TABLE_ALIGNMENT.CENTER
    comp_headers = ["Solution Category", "Representative Platforms", "Core Capabilities", "Critical Limitations Addressed by SafeBuild"]
    comp_data = [
        ["Commercial Navigation", "Google Maps, Apple Maps, Waze", "Dynamic driver re-routing around active closures; live GPS traffic probe data.", "Post-closure focus only; cannot optimize pre-construction phase order or evaluate community equity."],
        ["Desktop GIS Platforms", "Esri ArcGIS Network Analyst, QGIS", "Advanced spatial analysis, buffer generation, static network routing.", "High per-seat licensing costs; steep learning curve; lacks native construction scheduling dependency logic."],
        ["Project Scheduling Tools", "Oracle Primavera P6, Microsoft Project", "CPM scheduling, resource allocation, Gantt chart dependency tracking.", "Completely blind to geospatial road topology, network impedance, and spatial community access severance."],
        ["Traffic Simulation Tools", "PTV VISSIM, Aimsun, SUMO", "Microscopic car-following simulation, queue lengths, dynamic signal timing.", "Extreme data and calibration burden; computationally heavy; impractical for rapid scenario comparison."]
    ]
    col_w_comp = [Inches(1.2), Inches(1.3), Inches(2.2), Inches(2.27)]
    for j, h in enumerate(comp_headers):
        cell = tbl_comp.cell(0, j)
        cell.width = col_w_comp[j]
        set_cell_background(cell, "1E293B")
        set_cell_margins(cell, top=50, bottom=50, left=60, right=60)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(7.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    for i, row in enumerate(comp_data):
        bg = "FFFFFF" if i % 2 == 0 else "F8FAFC"
        for j, val in enumerate(row):
            cell = tbl_comp.cell(i+1, j)
            cell.width = col_w_comp[j]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=40, bottom=40, left=60, right=60)
            set_cell_border(cell, top=dict(color="CBD5E1", sz="4"), bottom=dict(color="CBD5E1", sz="4"), left=dict(color="CBD5E1", sz="4"), right=dict(color="CBD5E1", sz="4"))
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(val)
            r.font.size = Pt(7)
            if j == 0:
                r.bold = True

    doc.add_paragraph().paragraph_format.space_after = Pt(3)

    # Readiness Box
    tbl_readiness = doc.add_table(rows=1, cols=1)
    tbl_readiness.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_read = tbl_readiness.cell(0, 0)
    c_read.width = Inches(6.97)
    set_cell_background(c_read, "F0FDF4")
    set_cell_border(c_read, top=dict(color="22C55E", sz="6"), bottom=dict(color="22C55E", sz="6"), left=dict(color="22C55E", sz="6"), right=dict(color="22C55E", sz="6"))
    set_cell_margins(c_read, top=80, bottom=80, left=120, right=120)
    p_read = c_read.paragraphs[0]
    p_read.paragraph_format.space_after = Pt(0)
    r_rb = p_read.add_run("DEVELOPMENT READINESS DECLARATION: ")
    r_rb.bold = True
    r_rb.font.size = Pt(8)
    r_rb.font.color.rgb = RGBColor(21, 128, 61)
    r_rt = p_read.add_run(
        "“Working prototype tested using real Kakkanad geographic data and hypothetical construction scenarios; "
        "field validation and authority review pending.” SafeBuild operates as a verified computational prototype. "
        "All algorithms execute deterministically, but operational deployment requires joint on-site surveys and formal statutory sanction."
    )
    r_rt.font.size = Pt(8)
    r_rt.font.italic = True
    r_rt.font.color.rgb = RGBColor(22, 101, 52)

    doc.add_paragraph().paragraph_format.space_after = Pt(3)

    p_cost = doc.add_paragraph()
    p_cost.add_run("7.2 Cost & Financial Feasibility: ").bold = True
    p_cost.add_run(
        "The proposed implementation model leverages open-source geospatial foundations (OSM, NetworkX, MapLibre), avoiding recurring per-seat proprietary GIS licensing fees. "
        "An indicative student-led 3-month research development and validation budget is projected at Rs. 2,70,000 – Rs. 5,05,000: "
        "(a) Geospatial data engineering & OSM curation: Rs. 60,000 – Rs. 1,10,000; "
        "(b) Platform development & modeling enhancements: Rs. 1,10,000 – Rs. 2,00,000; "
        "(c) Field ground surveys & cross-section validation: Rs. 60,000 – Rs. 1,15,000; "
        "(d) Stakeholder review workshops & research dissemination: Rs. 40,000 – Rs. 80,000. "
        "Ongoing operational cloud hosting, periodic OSM network refreshes, and maintenance are estimated at Rs. 8,000 – Rs. 25,000 / month."
    )

    p_road = doc.add_paragraph()
    p_road.add_run("7.3 Phased Implementation Roadmap: ").bold = True
    p_road.add_run(
        "Stage 1: Core Prototype Verification (Completed) — Formalized 5-state algebra, Dijkstra engine, 17 automated tests, and independent verification. "
        "Stage 2: Supervised Scenario Validation (Current) — Comprehensive scenario modeling on Kakkanad corridor and evidence documentation. "
        "Stage 3: Stakeholder Engagement & Surveys (Months 1–2) — Administer planned 45–60 practitioner study with Kochi municipal engineers and contractors. "
        "Stage 4: Parallel Advisory Trial (Months 3–4) — Evaluate SafeBuild shadow outputs alongside an active municipal roadwork project. "
        "Stage 5: Multi-Corridor Platform Refinement (Months 5–6) — Expand to 3 additional metropolitan corridors and integrate multi-destination routing. "
        "Stage 6: Municipality-Scale Integration (Future Horizon) — Open API integration with municipal GIS portals pending formal statutory sanction."
    )

    p_ref = doc.add_paragraph()
    p_ref.add_run("References & Data Attribution: ").bold = True
    p_ref.add_run(
        "(1) OpenStreetMap contributors, Open Database License (ODbL), https://www.openstreetmap.org/copyright; "
        "(2) Dijkstra, E. W. (1959). A note on two problems in connexion with graphs. Numerische Mathematik, 1(1), 269–271; "
        "(3) Hagberg, A., Swart, P., & S Chult, D. (2008). Exploring network structure, dynamics, and function using NetworkX; "
        "(4) ReportLab Europe Ltd. ReportLab PDF Generation Library."
    )
    p_ref.runs[0].font.size = Pt(7)
    p_ref.runs[1].font.size = Pt(7)
    p_ref.runs[1].font.color.rgb = light_slate

    doc.save(filename)
    print(f"Successfully generated {filename}")

if __name__ == "__main__":
    build_docx()
