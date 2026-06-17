"""Variable meaning, physics-score rationale, and expected-direction metadata."""

from __future__ import annotations

import pandas as pd

from .dataset_config import DatasetSpec


FEATURE_MEANINGS: dict[str, dict[str, str]] = {
    "chf": {
        "D (m)": "flow channel hydraulic diameter",
        "L (m)": "heated length of the channel",
        "P (kPa)": "system pressure",
        "G (kg m-2s-1)": "mass flux",
        "Tin (C)": "inlet coolant temperature",
        "Xe (-)": "exit quality",
    },
    "heat": {
        "qprime": "linear heat generation rate",
        "mdot": "coolant mass flow rate",
        "Tin": "inlet temperature",
        "R": "fuel or heat-source radius",
        "L": "heated length",
        "Cp": "coolant heat capacity",
        "k": "thermal conductivity",
    },
    "xs": {
        "FissionFast": "fast-group fission cross section",
        "CaptureFast": "fast-group capture cross section",
        "FissionThermal": "thermal-group fission cross section",
        "CaptureThermal": "thermal-group capture cross section",
        "Scatter12": "group-1 to group-2 scattering cross section",
        "Scatter11": "within-group scattering cross section for group 1",
        "Scatter21": "group-2 to group-1 scattering cross section",
        "Scatter22": "within-group scattering cross section for group 2",
    },
    "bwr": {
        "PSZ": "BWR core operating or shape parameter from the problem data",
        "DOM": "BWR core operating or shape parameter from the problem data",
        "vanA": "BWR vaned-device or flow-distribution parameter A",
        "vanB": "BWR vaned-device or flow-distribution parameter B",
        "subcool": "coolant inlet subcooling",
        "CRD": "control rod drive or rod insertion state",
        "flow_rate": "core coolant flow rate",
        "power_density": "core power density",
        "VFNGAP": "void or gap-related core parameter from the problem data",
    },
    "fp": {
        "fuel_dens": "fuel density",
        "porosity": "fuel porosity",
        "clad_thick": "cladding thickness",
        "pellet_OD": "fuel pellet outer diameter",
        "pellet_h": "fuel pellet height",
        "gap_thick": "fuel-cladding gap thickness",
        "inlet_T": "coolant inlet temperature",
        "enrich": "fuel enrichment",
        "rough_fuel": "fuel surface roughness",
        "rough_clad": "cladding surface roughness",
        "ax_pow": "axial power factor or axial power level",
        "clad_T": "cladding temperature",
        "pressure": "system pressure",
    },
    "rea": {
        "rod_worth": "reactivity worth of the control rod",
        "beta": "effective delayed neutron fraction",
        "h_gap": "fuel-cladding gap heat-transfer coefficient",
        "gamma_frac": "gamma heating fraction",
    },
    "powery": {
        "CR1": "control rod group 1 position or setting",
        "CR2": "control rod group 2 position or setting",
        "CR3": "control rod group 3 position or setting",
        "CR4": "control rod group 4 position or setting",
        "CR5": "control rod group 5 position or setting",
        "CR6": "control rod group 6 position or setting",
    },
    "htgr": {
        "theta1": "HTGR design or angular parameter 1",
        "theta2": "HTGR design or angular parameter 2",
        "theta3": "HTGR design or angular parameter 3",
        "theta4": "HTGR design or angular parameter 4",
        "theta5": "HTGR design or angular parameter 5",
        "theta6": "HTGR design or angular parameter 6",
        "theta7": "HTGR design or angular parameter 7",
        "theta8": "HTGR design or angular parameter 8",
    },
    "microreactor": {
        "theta1": "microreactor design or angular parameter 1",
        "theta2": "microreactor design or angular parameter 2",
        "theta3": "microreactor design or angular parameter 3",
        "theta4": "microreactor design or angular parameter 4",
        "theta5": "microreactor design or angular parameter 5",
        "theta6": "microreactor design or angular parameter 6",
        "theta7": "microreactor design or angular parameter 7",
        "theta8": "microreactor design or angular parameter 8",
    },
}


TARGET_MEANINGS: dict[str, dict[str, str]] = {
    "chf": {"CHF (kW m-2)": "critical heat flux"},
    "heat": {"T": "temperature response"},
    "xs": {"k": "effective multiplication factor"},
    "bwr": {
        "K-eff": "effective multiplication factor",
        "Max3Pin": "maximum three-pin power indicator",
        "Max4Pin": "maximum four-pin power indicator",
        "F-delta-H": "axial enthalpy rise hot-channel factor",
        "Max-Fxy": "maximum radial power peaking factor",
    },
    "fp": {
        "fis_gas_produced": "fission gas produced",
        "max_fuel_centerline_temp": "maximum fuel centerline temperature",
        "max_fuel_surface_temp": "maximum fuel surface temperature",
        "radial_clad_dia": "radial cladding diameter change",
    },
    "rea": {
        "max_power": "maximum power",
        "burst_width": "power burst width",
        "max_Tf": "maximum fuel temperature",
        "avg_Tcool": "average coolant temperature",
    },
    "powery": {
        "A-2": "local power response at position A-2",
        "B-1": "local power response at position B-1",
        "B-2": "local power response at position B-2",
        "B-4": "local power response at position B-4",
        "B-5": "local power response at position B-5",
        "B-7": "local power response at position B-7",
        "B-8": "local power response at position B-8",
        "C-1": "local power response at position C-1",
        "C-2": "local power response at position C-2",
        "C-3": "local power response at position C-3",
        "C-4": "local power response at position C-4",
        "C-5": "local power response at position C-5",
        "C-6": "local power response at position C-6",
        "C-7": "local power response at position C-7",
        "C-8": "local power response at position C-8",
        "C-9": "local power response at position C-9",
        "C-10": "local power response at position C-10",
        "C-11": "local power response at position C-11",
        "C-12": "local power response at position C-12",
        "C-13": "local power response at position C-13",
        "C-14": "local power response at position C-14",
        "C-15": "local power response at position C-15",
    },
    "htgr": {
        "fluxQ1": "neutron flux or power response in quadrant 1",
        "fluxQ2": "neutron flux or power response in quadrant 2",
        "fluxQ3": "neutron flux or power response in quadrant 3",
        "fluxQ4": "neutron flux or power response in quadrant 4",
    },
    "microreactor": {
        "fluxQ1": "neutron flux or power response in quadrant 1",
        "fluxQ2": "neutron flux or power response in quadrant 2",
        "fluxQ3": "neutron flux or power response in quadrant 3",
        "fluxQ4": "neutron flux or power response in quadrant 4",
    },
}


PHYSICAL_EXPECTED_DIRECTIONS: dict[str, dict[str, dict[str, int]]] = {
    "heat": {
        "T": {
            "qprime": 1,
            "Tin": 1,
            "R": 1,
            "L": 1,
            "k": -1,
            "mdot": -1,
            "Cp": -1,
        }
    },
    "rea": {
        "max_power": {"rod_worth": 1, "beta": -1},
        "burst_width": {"rod_worth": -1, "beta": 1},
        "max_Tf": {"rod_worth": 1, "h_gap": -1},
        "avg_Tcool": {"rod_worth": 1, "gamma_frac": 1},
    },
    "xs": {
        "k": {
            "FissionFast": 1,
            "FissionThermal": 1,
            "CaptureFast": -1,
            "CaptureThermal": -1,
            "Scatter12": 1,
            "Scatter21": -1,
        }
    },
    "chf": {
        "CHF (kW m-2)": {
            "G (kg m-2s-1)": 1,
            "P (kPa)": 1,
            "D (m)": -1,
            "L (m)": -1,
            "Xe (-)": -1,
        }
    },
}


def build_physical_score_rationale(specs: list[DatasetSpec]) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for spec in specs:
        scores = spec.physical_scores or {}
        for feature in spec.input_columns:
            score = float(scores.get(feature, 0.5))
            rows.append(
                {
                    "dataset": spec.name,
                    "feature": feature,
                    "physical_meaning": feature_meaning(spec.name, feature),
                    "physical_score": score,
                    "relevance_level": _score_level(score),
                    "score_rationale": _score_rationale(score, spec.name, feature),
                }
            )
    return pd.DataFrame(rows)


def build_variable_physical_meaning(specs: list[DatasetSpec]) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for spec in specs:
        scores = spec.physical_scores or {}
        for feature in spec.input_columns:
            rows.append(
                {
                    "dataset": spec.name,
                    "role": "input",
                    "variable": feature,
                    "physical_meaning": feature_meaning(spec.name, feature),
                    "physical_score": float(scores.get(feature, 0.5)),
                    "expected_direction_summary": _expected_direction_summary(spec.name, feature),
                }
            )
        for target in spec.output_columns:
            rows.append(
                {
                    "dataset": spec.name,
                    "role": "output",
                    "variable": target,
                    "physical_meaning": target_meaning(spec.name, target),
                    "physical_score": "",
                    "expected_direction_summary": "model output",
                }
            )
    return pd.DataFrame(rows)


def build_expected_direction_table(specs: list[DatasetSpec]) -> pd.DataFrame:
    valid_pairs = {(spec.name, target) for spec in specs for target in spec.output_columns}
    rows: list[dict[str, object]] = []
    for dataset, target_map in PHYSICAL_EXPECTED_DIRECTIONS.items():
        for target, feature_map in target_map.items():
            if (dataset, target) not in valid_pairs:
                continue
            for feature, direction in feature_map.items():
                rows.append(
                    {
                        "dataset": dataset,
                        "feature": feature,
                        "target": target,
                        "feature_meaning": feature_meaning(dataset, feature),
                        "target_meaning": target_meaning(dataset, target),
                        "expected_direction": direction,
                        "expected_effect": _direction_label(direction),
                        "direction_rationale": _direction_rationale(dataset, feature, target, direction),
                    }
                )
    return pd.DataFrame(rows)


def feature_meaning(dataset: str, feature: str) -> str:
    return FEATURE_MEANINGS.get(dataset, {}).get(feature, "problem-defined input variable")


def target_meaning(dataset: str, target: str) -> str:
    return TARGET_MEANINGS.get(dataset, {}).get(target, "problem-defined output variable")


def _score_level(score: float) -> str:
    if score >= 0.95:
        return "direct_physics"
    if score >= 0.75:
        return "clear_operating_relevance"
    if score >= 0.55:
        return "secondary_physics"
    return "weak_or_unspecified"


def _score_rationale(score: float, dataset: str, feature: str) -> str:
    meaning = feature_meaning(dataset, feature)
    if score >= 0.95:
        return f"{meaning}; directly tied to the governing heat-transfer, neutronics, or fuel-behavior mechanism."
    if score >= 0.75:
        return f"{meaning}; has clear operating or control relevance but is less directly mechanistic than primary state variables."
    if score >= 0.55:
        return f"{meaning}; treated as a secondary interface or boundary-condition effect."
    return f"{meaning}; retained mainly when data evidence supports it because explicit physics relevance is limited."


def _expected_direction_summary(dataset: str, feature: str) -> str:
    parts = []
    for target, feature_map in PHYSICAL_EXPECTED_DIRECTIONS.get(dataset, {}).items():
        if feature in feature_map:
            parts.append(f"{target}: {_direction_label(feature_map[feature])}")
    return "; ".join(parts) if parts else "not_configured"


def _direction_label(direction: int) -> str:
    if direction > 0:
        return "positive"
    if direction < 0:
        return "negative"
    return "not_configured"


def _direction_rationale(dataset: str, feature: str, target: str, direction: int) -> str:
    relation = "increase" if direction > 0 else "decrease"
    return (
        f"Based on the expected physical relation, increasing {feature} "
        f"is expected to {relation} {target}."
    )
