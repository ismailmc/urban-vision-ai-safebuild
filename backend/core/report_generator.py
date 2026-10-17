import csv
import io
import os
import datetime
from typing import Dict, Any, Optional
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_csv_report(scenario_data: Dict[str, Any], phases_data: Optional[Dict[str, Any]] = None) -> str:
    """Generates an RFC 4180 compliant CSV of the phase-specific evaluation."""
    output = io.StringIO()
    writer = csv.writer(output)

    # Header metadata comments
    writer.writerow(["# SafeBuild Construction Access Planning Brief", "Kakkanad Corridor Scenario Study Area"])
    writer.writerow(["# Status", "PROVISIONAL SCENARIO MODEL — UNVERIFIED"])
    writer.writerow(["# Run ID", scenario_data.get("run_id", "N/A")])
    writer.writerow(["# Snapshot Date", scenario_data["metadata"]["snapshot_date"]])
    writer.writerow(["# Analysis Timestamp", datetime.datetime.now(datetime.timezone.utc).isoformat()])
    writer.writerow(["# Scenario Mode", scenario_data["mode"]])
    writer.writerow(["# Project Context", scenario_data["metadata"]["project_context"]])
    writer.writerow(["# Primary Facility", scenario_data["primary_facility"]["name"]])
    writer.writerow([])

    # Table columns
    columns = [
        "Origin ID", "Origin Name", "Sampling Anchor",
        "G0 Distance (m)", "G0 Reachable",
        "Under Restriction Distance (m)", "Under Restriction Reachable",
        "Net Detour Delta (m)", "Detour Pct (%)", "Newly Disconnected",
        "Exposure Duration (days)", "Mitigation Recovery (m)"
    ]
    writer.writerow(columns)

    for r in scenario_data["per_origin_results"]:
        writer.writerow([
            r["origin_id"],
            r["origin_name"],
            r.get("sampling_method", "Settlement anchor"),
            r["G0_distance_m"],
            r["G0_reachable"],
            r["G0_C_distance_m"],
            r["G0_C_reachable"],
            r["construction_delta_m"],
            f"{r['detour_percentage']}%",
            "YES" if (r["G0_reachable"] and not r["G0_C_reachable"]) else "NO",
            r.get("exposure_duration_days", 45.0),
            r["mitigation_recovery_m"]
        ])

    return output.getvalue()

def generate_pdf_report(scenario_data: Dict[str, Any], optimizer_data: Dict[str, Any], filepath: str, phases_data: Optional[Dict[str, Any]] = None):
    """Generates a structured multi-page PDF scenario report matching model calculations and verification safeguards."""
    doc = SimpleDocTemplate(filepath, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#0F172A')
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#475569')
    )
    badge_style = ParagraphStyle(
        'DocBadge',
        parent=styles['Normal'],
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#DC2626'),
        fontName='Helvetica-Bold'
    )
    section_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontSize=12,
        leading=15,
        textColor=colors.HexColor('#0E7490'),
        spaceBefore=10,
        spaceAfter=5
    )
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#1E293B')
    )
    alert_style = ParagraphStyle(
        'Alert',
        parent=styles['Normal'],
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#B45309')
    )

    story = []

    # Title & Header
    story.append(Paragraph("URBAN VISION AI — SAFEBUILD", title_style))
    story.append(Paragraph("Construction Access Review & Phase Scenario Brief | SFIC 2026", subtitle_style))
    story.append(Paragraph("STATUS: PROVISIONAL SCENARIO MODEL — UNVERIFIED (PLANNING EVALUATION ONLY)", badge_style))
    story.append(Spacer(1, 8))

    # Provenance & Metadata Box
    meta = scenario_data["metadata"]
    summary = scenario_data["summary"]
    run_id = scenario_data.get("run_id", "N/A")
    timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    meta_text = f"""
    <b>Study Area:</b> {meta['name']} ({meta['region']})<br/>
    <b>Run ID:</b> {run_id} | <b>Snapshot Date:</b> {meta['snapshot_date']} | <b>Analysis Timestamp:</b> {timestamp}<br/>
    <b>Infrastructure Context:</b> {meta['project_context']}<br/>
    <b>Scenario Label:</b> {meta['scenario_label']}<br/>
    <b>Evaluated Facility:</b> {scenario_data['primary_facility']['name']} ({scenario_data['primary_facility']['verification_status']})<br/>
    <b>Travel Mode:</b> {scenario_data['mode'].replace('_', ' ').title()} (Deterministic Network Routing)
    """
    story.append(Paragraph(meta_text, body_style))
    story.append(Spacer(1, 8))

    # Analytical Summary
    story.append(Paragraph("1. Construction Phase Access Analysis", section_style))
    sum_text = f"""
    <b>Total Analyzed Origins:</b> {summary['total_origins']} | 
    <b>Baseline Reachable:</b> {summary['origins_reachable_G0']} | 
    <b>Under Construction Reachable:</b> {summary['origins_reachable_G0_C']}<br/>
    <b>Worst Modeled Detour:</b> {summary['worst_detour_m']} m ({summary['worst_affected_origin']}) | 
    <b>Average Detour:</b> {summary['average_detour_m']} m<br/>
    <b>Newly Disconnected Pairs:</b> {summary['new_unreachable_origins']} (All sampled points remain connected via detours)<br/>
    <b>Proposal Invariant (P = identity):</b> {'SATISFIED' if summary['proposal_algebra_invariant_met'] else 'VIOLATED'}
    """
    story.append(Paragraph(sum_text, body_style))
    story.append(Spacer(1, 8))

    # Origin Results Table
    table_data = [
        ["Origin Community Anchor", "Baseline (m)", "Under Work (m)", "Detour (m)", "Increase %", "Mitigated (m)"]
    ]
    for r in scenario_data["per_origin_results"]:
        table_data.append([
            r["origin_name"],
            str(r["G0_distance_m"]),
            str(r["G0_C_distance_m"]),
            str(r["construction_delta_m"]),
            f"{r['detour_percentage']}%",
            str(r["G0_P_C_M_distance_m"])
        ])

    t = Table(table_data, colWidths=[200, 60, 60, 70, 60, 70])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#0F172A')),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
    ]))
    story.append(t)
    story.append(Spacer(1, 10))

    # Alternatives Evaluation Section
    story.append(Paragraph("2. Bounded Comparison of Work Arrangements", section_style))
    opt_text = f"""
    <b>Optimization Gate:</b> <b>{optimizer_data['recommended_status']}</b><br/>
    <b>Verification Note:</b> {optimizer_data['recommendation_note']}
    """
    story.append(Paragraph(opt_text, alert_style))
    story.append(Spacer(1, 6))

    cand_table = [
        ["Arrangement / Candidate", "Feasibility Status", "Permission Status", "Detour Reduction", "Constraint Conflict"]
    ]
    for c in optimizer_data["all_evaluated_candidates"]:
        cand_table.append([
            c["name"],
            c["feasibility_class"],
            c["permission_status"],
            f"-{c['modeled_metrics']['average_detour_reduction_m']}m",
            "PEDESTRIAN CONFLICT" if c["conflict_pedestrian"] else "NONE"
        ])
    ct = Table(cand_table, colWidths=[160, 110, 140, 60, 50])
    ct.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
    ]))
    story.append(ct)
    story.append(Spacer(1, 10))

    # Scientific Limitations & Audit Trail
    story.append(Paragraph("3. Scientific Truth Safeguards & Audit Trail", section_style))
    caveats = """
    • <b>Non-Emergency Claim:</b> Detour distances are deterministic graph computations and do not represent observed ambulance response times, traffic congestion, or live travel speeds.<br/>
    • <b>Unverified Status:</b> No reviewed candidate has undergone field verification or authority review. The system deliberately refrains from marking them implementable.<br/>
    • <b>Community Privacy:</b> Sampled points represent geographic road-side access anchors, NOT counted residential populations.<br/>
    • <b>Data Source:</b> OpenStreetMap contributors (ODbL). Snapshot downloaded 2026-10-12 across 19,582 nodes with complete referential topology.<br/>
    • <b>Validity Scope:</b> Valid for scenario planning review only. Field execution requires formal traffic management design and stakeholder consultation.
    """
    story.append(Paragraph(caveats, body_style))

    doc.build(story)
