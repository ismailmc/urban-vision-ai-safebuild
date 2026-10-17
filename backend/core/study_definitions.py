from typing import Dict, List, Any

# Primary Provisional Study Area: Kakkanad, Kochi (WGS84)
# Core research bounding box: [76.335, 10.015, 76.355, 10.030]
# Full routing buffer: [76.330, 10.010, 76.360, 10.035]

STUDY_AREA_METADATA = {
    "name": "Kakkanad Corridor Scenario Study Area",
    "region": "Kochi, Kerala, India",
    "project_context": "Kakkanad Corridor Scenario Study (Hypothetical Metro Viaduct Construction on Palarivattom-Kakkanad Rd)",
    "scenario_label": "HYPOTHETICAL_CONSTRUCTION_ACCESS_REVIEW_ON_REAL_ROADS",
    "snapshot_date": "2026-10-12",
    "core_bbox": [76.335, 10.015, 76.355, 10.030],
    "buffered_bbox": [76.330, 10.010, 76.360, 10.035],
    "crs_source": "EPSG:4326 (WGS84)",
    "crs_projected": "EPSG:32643 (UTM Zone 43N)",
    "network_status": "MAPPED_ROAD_NETWORK_UNVERIFIED_FIELD_TOPOLOGY"
}

# Verified Essential Facilities (Destinations)
FACILITIES = [
    {
        "id": "fac_sunrise",
        "name": "Sunrise Hospital, Ernakulam",
        "type": "hospital",
        "operator_source": "Sunrise Hospital Operator & OSM Node 343719028",
        "lat": 10.0252315,
        "lon": 76.3388796,
        "address": "Vii/528-B, Seaport - Airport Road, Kakkanad, Kochi, 682030",
        "verification_status": "OPERATOR_ADDRESS_VERIFIED_ENTRANCE_PROVISIONAL",
        "notes": "Emergency receiving tertiary hospital on Seaport-Airport Road. Entrance coordinates provisional."
    },
    {
        "id": "fac_thrikkakara_coop",
        "name": "Thrikkakara Municipal Co-operative Hospital",
        "type": "hospital",
        "operator_source": "OSM Node 343711683",
        "lat": 10.0315,
        "lon": 76.3352,
        "address": "Thrikkakara, Kakkanad",
        "verification_status": "OSM_VERIFIED_SECONDARY",
        "notes": "Municipal hospital serving Thrikkakara and northern Kakkanad."
    }
]

# Residential Community Origin Anchors
# Unverified household counts removed per specification; sampling anchors clearly attributed to OSM features.
COMMUNITY_ORIGINS = [
    {
        "id": "orig_dlf_city",
        "name": "DLF City / New Town Heights Anchor",
        "lat": 10.0210,
        "lon": 76.3392,
        "type": "residential_neighborhood",
        "sampling_method": "Road-side centroid anchor representing surrounding settlement",
        "verification_source": "OSM Node 3837328137 & Way 899147081",
        "status": "PUBLIC_SETTLEMENT_ANCHOR"
    },
    {
        "id": "orig_kollamkudi",
        "name": "Kollamkudimugal Residential Anchor",
        "lat": 10.0165,
        "lon": 76.3440,
        "type": "residential_neighborhood",
        "sampling_method": "Junction access point representing Kollamkudimugal settlement",
        "verification_source": "OSM Node 12302169119 & Way 607226671",
        "status": "PUBLIC_SETTLEMENT_ANCHOR"
    },
    {
        "id": "orig_canal_colony",
        "name": "Canal Colony Settlement Anchor",
        "lat": 10.0142,
        "lon": 76.3485,
        "type": "settlement_colony",
        "sampling_method": "Centroid anchor along canal access road",
        "verification_source": "OSM Way 1076763438",
        "status": "PUBLIC_SETTLEMENT_ANCHOR"
    },
    {
        "id": "orig_padamugal",
        "name": "Padamugal Residential Neighborhood Anchor",
        "lat": 10.0153,
        "lon": 76.3357,
        "type": "residential_neighborhood",
        "sampling_method": "Public post-office road frontage anchor",
        "verification_source": "OSM Node 4292013890",
        "status": "PUBLIC_SETTLEMENT_ANCHOR"
    },
    {
        "id": "orig_ngo_quarters",
        "name": "NGO Quarters Housing Colony Anchor",
        "lat": 10.0275,
        "lon": 76.3465,
        "type": "residential_neighborhood",
        "sampling_method": "Housing colony arterial access connector",
        "verification_source": "OSM Way 368162329",
        "status": "PUBLIC_SETTLEMENT_ANCHOR"
    },
    {
        "id": "orig_kakkanad_west",
        "name": "Kakkanad West / Civil Station Environs Anchor",
        "lat": 10.0220,
        "lon": 76.3325,
        "type": "civic_residential",
        "sampling_method": "Western civic/residential road-side anchor",
        "verification_source": "OSM Way 133755617 & Node 594931695",
        "status": "PUBLIC_SETTLEMENT_ANCHOR"
    }
]

# Baseline Disruption Scenario
CONSTRUCTION_DISRUPTIONS = [
    {
        "id": "c_metro_pier_workzone",
        "name": "Palarivattom-Kakkanad Rd Metro Pier Erection Zone",
        "description": "Hypothetical construction restriction along Metro corridor between Padamugal and Kakkanad junction on mapped road network.",
        "target_way_ids": ["197827530", "383253303", "1011679137", "1011679138"],
        "modes_affected": ["motor_vehicle"],
        "direction": "both",
        "phase": "Pier Foundation Phase (Hypothetical)",
        "status": "HYPOTHETICAL_CONSTRUCTION_SCENARIO",
        "scenario_status": "HYPOTHETICAL_CORRIDOR_CLOSURE_SCENARIO"
    }
]

# Reviewed Candidate Interventions
CANDIDATE_INTERVENTIONS = [
    {
        "id": "cand_m1_phased_contraflow",
        "name": "Single-Lane Managed Contraflow & Signal Priority",
        "description": "Preserve one lane of unidirectional managed vehicle flow through work-zone with flaggers and emergency priority.",
        "type": "operational_management",
        "cost_status": "UNKNOWN_CIVIL_ESTIMATE_NEEDED",
        "permission_status": "UNVERIFIED_MODEL_SCENARIO",
        "physical_status": "PROVISIONAL_GEOMETRY_MODEL",
        "feasibility_tested": False,
        "restores_way_ids": ["197827530", "1011679138"],
        "speed_factor": 0.5,
        "conflict_pedestrian": True,
        "reviewer": "Scenario Modeling Framework"
    },
    {
        "id": "cand_m2_civil_lane_diversion",
        "name": "Civil Lane Road Formal Secondary Diversion",
        "description": "Formalize Civil Lane Road (Way 867276513) with temporary signage, removing on-street parking to absorb diverted traffic.",
        "type": "rerouting_corridor",
        "cost_status": "LOW_SIGNAGE_ONLY",
        "permission_status": "UNVERIFIED_MODEL_SCENARIO",
        "physical_status": "OSM_MAPPED_RESIDENTIAL_ROAD",
        "feasibility_tested": False,
        "restores_way_ids": [],
        "adds_temporary_capacity_way_ids": ["867276513"],
        "conflict_pedestrian": False,
        "reviewer": "Scenario Modeling Framework"
    },
    {
        "id": "cand_m3_unverified_private_easement",
        "name": "Direct Campus Perimeter Cut-Through",
        "description": "Proposed unpaved connection through commercial campus perimeter.",
        "type": "new_unpaved_link",
        "cost_status": "UNKNOWN",
        "permission_status": "INELIGIBLE_PRIVATE_PROPERTY",
        "physical_status": "DISCONTINUOUS_ALIGNMENT_NO_PUBLIC_RIGHT_OF_WAY",
        "feasibility_tested": False,
        "restores_way_ids": [],
        "conflict_pedestrian": True,
        "reviewer": "Scenario Modeling Framework"
    }
]
