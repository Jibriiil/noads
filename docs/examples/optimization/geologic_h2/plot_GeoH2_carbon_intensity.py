"""
Carbon intensity vs. resource intensity, extended with geological hydrogen
=============================================================================

Reproduces the style of Fig. 16 of the NOADS paper
(https://iancostalves.github.io/noads/paper/models/energy.html), with two
side-by-side panels:

- Left  : biomass-based biofuels (HEFA, FT, ATJ), constant in time.
- Right : liquid-hydrogen routes (Electrolysis -> H2 liquefaction vs.
  Geological extraction -> H2 liquefaction), evaluated at 2025, 2035, 2050,
  2065 (marker size grows with the year), with the SSP2-2.6 background grid.

Fossil kerosene (Refinery pathway) is shown as the reference (star) on both
panels, using Table 5 of the paper (88.7 g CO2/MJ).

Impact factor of a pathway (Eq. 13 of the paper):
    IF_pathway = IF_direct_pathway + sum_i(CF_pathway,i * IF_i)
where CF_pathway,i = 1 / efficiency_pathway,i is the consumption of input i
per unit of output produced.
"""

import matplotlib.pyplot as plt
import numpy as np

from noads.application.background_scenario_data import get_ar6_input_data
from noads.core.models.interpolation import interpolate_data

YEARS = np.array([2025.0, 2035.0, 2050.0, 2065.0])
FOSSIL_CO2_INDEX = 88.7  # g CO2 / MJ, Table 5 (Refinery pathway)

# ---------------------------------------------------------------------------
# Background grid: SSP2-2.6 electricity carbon intensity (g CO2 / MJ)
# ---------------------------------------------------------------------------
ar6_data, ar6_years = get_ar6_input_data(start_year=2010, end_year=2080, plot_data=False)
grid_co2 = np.interp(
    YEARS, np.array(ar6_years), np.array(ar6_data["ELECTRICITY.CO2_index"]["SSP2-26"])
)


def interp_2025_2035_2050(tup):
    """Same interpolation convention used by NOADS for technology maturing."""
    return interpolate_data(
        x=YEARS,
        x_data=np.array([2025.0, 2035.0, 2050.0]),
        y_data=np.array(tup),
    )


# ---------------------------------------------------------------------------
# Left panel: biomass-based biofuels (static, Table 5)
# ---------------------------------------------------------------------------
biofuel_pathways = {
    "HEFA": {"co2_index": 62.75, "biomass_efficiency": 0.59, "color": "#1f77b4", "marker": "o"},
    "ATJ": {"co2_index": 51.55, "biomass_efficiency": 0.30, "color": "#2ca02c", "marker": "s"},
    "FT": {"co2_index": 35.3, "biomass_efficiency": 0.20, "color": "#9467bd", "marker": "^"},
}
for data in biofuel_pathways.values():
    data["resource_intensity"] = 1.0 / data["biomass_efficiency"]

# ---------------------------------------------------------------------------
# Right panel: all electricity-dependent carriers (time-dependent), with the
# GAS-H2 upstream pathways (Electrolysis / Geological extraction) kept
# SEPARATE for LH2 and E-FUEL: shares between GAS-H2 routes are an
# optimization output, not a fixed physical property, so a single "blended"
# curve cannot be drawn without assuming a share.
# ---------------------------------------------------------------------------
eff_electrolysis = interp_2025_2035_2050((0.71, 0.71 * 1.03, 0.71 * 1.06))
eff_liquefaction_elec = interp_2025_2035_2050((4.54, 4.54 * 1.2, 4.54 * 1.4))
eff_ptl_elec = interp_2025_2035_2050((1.53, 1.53 * 1.08, 1.53 * 1.16))
eff_ptl_gas = interp_2025_2035_2050((0.53, 0.53 * 1.06, 0.53 * 1.12))
eff_charging = 0.98 * np.ones_like(YEARS)  # constant
liquefaction_gas_h2_efficiency = 1.0  # constant, "H2_liquefaction.GAS-H2.efficiency"

# GAS-H2 impact factor per upstream route
if_gas_h2_electrolysis = (1.0 / eff_electrolysis) * grid_co2  # direct = 0
if_gas_h2_geologic = 3.0 * np.ones_like(YEARS)  # direct = 3.0 gCO2/MJ, constant
# electricity consumed per MJ of GAS-H2, per upstream route
ri_gas_h2_electrolysis = 1.0 / eff_electrolysis
ri_gas_h2_geologic = np.zeros_like(YEARS)  # extraction does not consume electricity

lh2_routes = {
    "LH2 (Electrolysis)": {
        "ci": liquefaction_gas_h2_efficiency * if_gas_h2_electrolysis
        + (1.0 / eff_liquefaction_elec) * grid_co2,
        "ri": liquefaction_gas_h2_efficiency * ri_gas_h2_electrolysis
        + (1.0 / eff_liquefaction_elec),
        "color": "#d62728", "marker": "o",
    },
    "LH2 (Geological H2)": {
        "ci": liquefaction_gas_h2_efficiency * if_gas_h2_geologic
        + (1.0 / eff_liquefaction_elec) * grid_co2,
        "ri": liquefaction_gas_h2_efficiency * ri_gas_h2_geologic
        + (1.0 / eff_liquefaction_elec),
        "color": "#d62728", "marker": "D",
    },
    "E-Fuel (Electrolysis)": {
        "ci": (1.0 / eff_ptl_gas) * if_gas_h2_electrolysis
        + (1.0 / eff_ptl_elec) * grid_co2,
        "ri": (1.0 / eff_ptl_gas) * ri_gas_h2_electrolysis + (1.0 / eff_ptl_elec),
        "color": "#ff7f0e", "marker": "o",
    },
    "E-Fuel (Geological H2)": {
        "ci": (1.0 / eff_ptl_gas) * if_gas_h2_geologic
        + (1.0 / eff_ptl_elec) * grid_co2,
        "ri": (1.0 / eff_ptl_gas) * ri_gas_h2_geologic + (1.0 / eff_ptl_elec),
        "color": "#ff7f0e", "marker": "D",
    },
    "Battery": {
        "ci": (1.0 / eff_charging) * grid_co2,
        "ri": 1.0 / eff_charging,
        "color": "#9467bd", "marker": "o",
    },
}

geologic_extraction_efficiency = 0.92  # constant, "Geological_extraction.GEOLOGIC_H2.efficiency"

# Geological H2 intensity (MJ GEOLOGIC_H2 / MJ produced), geological route only
geoh2_routes = {
    "LH2 (Geological H2)": {
        "ci": lh2_routes["LH2 (Geological H2)"]["ci"],
        "ri": liquefaction_gas_h2_efficiency * (1.0 / geologic_extraction_efficiency)
        * np.ones_like(YEARS),
        "color": "#d62728", "marker": "D",
    },
    "E-Fuel (Geological H2)": {
        "ci": lh2_routes["E-Fuel (Geological H2)"]["ci"],
        "ri": (1.0 / eff_ptl_gas) * (1.0 / geologic_extraction_efficiency),
        "color": "#ff7f0e", "marker": "D",
    },
}
fig, (ax_left, ax_mid, ax_right) = plt.subplots(1, 3, figsize=(16, 5))

# Left: biomass
for name, data in biofuel_pathways.items():
    ax_left.scatter(
        data["resource_intensity"], data["co2_index"],
        color=data["color"], marker=data["marker"], s=90, label=name, zorder=3,
    )
ax_left.scatter(0.0, FOSSIL_CO2_INDEX, color="black", marker="*", s=180,
                 label="Fossil kerosene", zorder=3)
ax_left.set_xlabel("Biomass intensity (MJ biomass / MJ fuel)")
ax_left.set_ylabel("Carbon intensity (g CO$_2$ / MJ)")
ax_left.set_title("Biomass-based biofuels")
ax_left.grid(alpha=0.3, linestyle="--")
ax_left.legend()

# Middle: electricity-dependent carriers, marker size shrinks with year
sizes = np.interp(YEARS, [YEARS.min(), YEARS.max()], [200, 30])
for name, data in lh2_routes.items():
    ax_mid.plot(data["ri"], data["ci"], color=data["color"], lw=1.2,
                linestyle="--" if data["marker"] == "D" else "-", zorder=2)
    ax_mid.scatter(
        data["ri"], data["ci"], color=data["color"], marker=data["marker"],
        s=sizes, label=name, zorder=3, edgecolors="white", linewidths=0.5,
    )
ax_mid.scatter(0.0, FOSSIL_CO2_INDEX, color="black", marker="*", s=180,
               label="Fossil kerosene", zorder=3)
ax_mid.set_xlabel("Electricity intensity (MJ elec. / MJ produced)")
ax_mid.set_ylabel("Carbon intensity (g CO$_2$ / MJ)")
ax_mid.set_title("Electricity-dependent carriers (SSP2-2.6)")
ax_mid.grid(alpha=0.3, linestyle="--")
ax_mid.legend()

# Right: geological-route carriers, GEOLOGIC_H2 as the resource axis
for name, data in geoh2_routes.items():
    ax_right.plot(data["ri"], data["ci"], color=data["color"], lw=1.2,
                  linestyle="--", zorder=2)
    ax_right.scatter(
        data["ri"], data["ci"], color=data["color"], marker=data["marker"],
        s=sizes, label=name, zorder=3, edgecolors="white", linewidths=0.5,
    )
ax_right.scatter(0.0, FOSSIL_CO2_INDEX, color="black", marker="*", s=180,
                  label="Fossil kerosene", zorder=3)
ax_right.set_xlabel("Geological H$_2$ intensity (MJ GEO-H2 / MJ produced)")
ax_right.set_ylabel("Carbon intensity (g CO$_2$ / MJ)")
ax_right.set_title("Geological H$_2$ routes: primary resource view")
ax_right.grid(alpha=0.3, linestyle="--")
ax_right.legend()

fig.suptitle("Carbon intensity vs. resource intensity, with geological hydrogen")
fig.tight_layout()
fig.savefig(
    __import__("pathlib").Path(__file__).resolve().parent / "energy_ci_vs_resource_geoh2.png",
    dpi=200,
)
plt.show()

print("Grid CO2 intensity (gCO2/MJ) at", YEARS, ":", grid_co2)
for name, data in lh2_routes.items():
    print(f"{name}: CI={data['ci']}, RI={data['ri']}")