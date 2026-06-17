"""Dataset definitions for problem 1 feature analysis."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd


@dataclass(frozen=True)
class DatasetSpec:
    name: str
    input_file: str
    output_file: str | None
    input_columns: list[str]
    output_columns: list[str]
    id_columns: list[str] | None = None
    physical_scores: dict[str, float] | None = None


def _score(columns: list[str], value: float = 1.0) -> dict[str, float]:
    return {col: value for col in columns}


DATASET_SPECS: list[DatasetSpec] = [
    DatasetSpec(
        name="chf",
        input_file="chf.csv",
        output_file=None,
        input_columns=["D (m)", "L (m)", "P (kPa)", "G (kg m-2s-1)", "Tin (C)", "Xe (-)"],
        output_columns=["CHF (kW m-2)"],
        physical_scores=_score(["D (m)", "L (m)", "P (kPa)", "G (kg m-2s-1)", "Tin (C)", "Xe (-)"]),
    ),
    DatasetSpec(
        name="heat",
        input_file="heat.csv",
        output_file=None,
        input_columns=["qprime", "mdot", "Tin", "R", "L", "Cp", "k"],
        output_columns=["T"],
        physical_scores=_score(["qprime", "mdot", "Tin", "R", "L", "Cp", "k"]),
    ),
    DatasetSpec(
        name="xs",
        input_file="xs.csv",
        output_file=None,
        input_columns=[
            "FissionFast",
            "CaptureFast",
            "FissionThermal",
            "CaptureThermal",
            "Scatter12",
            "Scatter11",
            "Scatter21",
            "Scatter22",
        ],
        output_columns=["k"],
        physical_scores=_score(
            [
                "FissionFast",
                "CaptureFast",
                "FissionThermal",
                "CaptureThermal",
                "Scatter12",
                "Scatter11",
                "Scatter21",
                "Scatter22",
            ]
        ),
    ),
    DatasetSpec(
        name="bwr",
        input_file="bwr_input.csv",
        output_file="bwr_output.csv",
        input_columns=[
            "PSZ",
            "DOM",
            "vanA",
            "vanB",
            "subcool",
            "CRD",
            "flow_rate",
            "power_density",
            "VFNGAP",
        ],
        output_columns=["K-eff", "Max3Pin", "Max4Pin", "F-delta-H", "Max-Fxy"],
        physical_scores={
            "PSZ": 0.8,
            "DOM": 0.8,
            "vanA": 0.8,
            "vanB": 0.8,
            "subcool": 1.0,
            "CRD": 1.0,
            "flow_rate": 1.0,
            "power_density": 1.0,
            "VFNGAP": 1.0,
        },
    ),
    DatasetSpec(
        name="fp",
        input_file="fp_inp.csv",
        output_file="fp_out.csv",
        input_columns=[
            "fuel_dens",
            "porosity",
            "clad_thick",
            "pellet_OD",
            "pellet_h",
            "gap_thick",
            "inlet_T",
            "enrich",
            "rough_fuel",
            "rough_clad",
            "ax_pow",
            "clad_T",
            "pressure",
        ],
        output_columns=[
            "fis_gas_produced",
            "max_fuel_centerline_temp",
            "max_fuel_surface_temp",
            "radial_clad_dia",
        ],
        physical_scores={
            "fuel_dens": 1.0,
            "porosity": 1.0,
            "clad_thick": 1.0,
            "pellet_OD": 1.0,
            "pellet_h": 1.0,
            "gap_thick": 1.0,
            "inlet_T": 1.0,
            "enrich": 0.8,
            "rough_fuel": 0.6,
            "rough_clad": 0.6,
            "ax_pow": 1.0,
            "clad_T": 1.0,
            "pressure": 0.8,
        },
    ),
    DatasetSpec(
        name="rea",
        input_file="rea_inputs.csv",
        output_file="rea_outputs.csv",
        input_columns=["rod_worth", "beta", "h_gap", "gamma_frac"],
        output_columns=["max_power", "burst_width", "max_Tf", "avg_Tcool"],
        physical_scores=_score(["rod_worth", "beta", "h_gap", "gamma_frac"]),
    ),
    DatasetSpec(
        name="powery",
        input_file="crx.csv",
        output_file="powery.csv",
        input_columns=["CR1", "CR2", "CR3", "CR4", "CR5", "CR6"],
        output_columns=[
            "A-2",
            "B-1",
            "B-2",
            "B-4",
            "B-5",
            "B-7",
            "B-8",
            "C-1",
            "C-2",
            "C-3",
            "C-4",
            "C-5",
            "C-6",
            "C-7",
            "C-8",
            "C-9",
            "C-10",
            "C-11",
            "C-12",
            "C-13",
            "C-14",
            "C-15",
        ],
        physical_scores=_score(["CR1", "CR2", "CR3", "CR4", "CR5", "CR6"]),
    ),
    DatasetSpec(
        name="htgr",
        input_file="htgr.csv",
        output_file=None,
        input_columns=["theta1", "theta2", "theta3", "theta4", "theta5", "theta6", "theta7", "theta8"],
        output_columns=["fluxQ1", "fluxQ2", "fluxQ3", "fluxQ4"],
        id_columns=["index"],
        physical_scores=_score(["theta1", "theta2", "theta3", "theta4", "theta5", "theta6", "theta7", "theta8"]),
    ),
    DatasetSpec(
        name="microreactor",
        input_file="microreactor.csv",
        output_file=None,
        input_columns=["theta1", "theta2", "theta3", "theta4", "theta5", "theta6", "theta7", "theta8"],
        output_columns=["fluxQ1", "fluxQ2", "fluxQ3", "fluxQ4"],
        id_columns=["sample number"],
        physical_scores=_score(["theta1", "theta2", "theta3", "theta4", "theta5", "theta6", "theta7", "theta8"]),
    ),
]


def load_dataset(spec: DatasetSpec, data_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load X and y for one dataset spec."""
    input_path = data_dir / spec.input_file
    x_source = pd.read_csv(input_path)

    if spec.output_file is None:
        y_source = x_source
    else:
        output_path = data_dir / spec.output_file
        y_source = pd.read_csv(output_path)
        if len(x_source) != len(y_source):
            raise ValueError(
                f"{spec.name}: input rows ({len(x_source)}) != output rows ({len(y_source)})"
            )

    missing_x = [col for col in spec.input_columns if col not in x_source.columns]
    missing_y = [col for col in spec.output_columns if col not in y_source.columns]
    if missing_x or missing_y:
        raise KeyError(f"{spec.name}: missing input columns {missing_x}, missing output columns {missing_y}")

    x = x_source[spec.input_columns].copy()
    y = y_source[spec.output_columns].copy()
    return x, y
