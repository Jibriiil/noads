"""
Breakthrough aircraft: comparison of all variants

"""

from noads.application.examples import single_policy_scenario_optimization
from noads.application.visualization import plot_tech_scenario_fleet_carriers
from noads.application.visualization import plot_tech_scenario_jet_fuel
from noads.application.visualization import plot_tech_scenarios_trends

# %%
# Breakthrough scenario comparison

# Gather results from all four variants (baseline, trend, availability, low-demand)
# and plot comparisons: technology trends, jet fuel composition, and fleet energy
# carriers.
from noads.application.examples import single_policy_scenario_optimization
from noads.application.visualization import plot_tech_scenario_fleet_carriers
from noads.application.visualization import plot_tech_scenario_jet_fuel
from noads.application.visualization import plot_tech_scenarios_trends
BACKGROUND = "SSP2-26"


def load_results(
    include_geologic_h2= False,
    geologic_h2_availability="moderate",
    drop_in_only=False,
    fossil_kerosene_only=False,
    low_demand_formulation=False,
    preferential_energy=False
):
    """Load saved results for all three technology levels."""
    return [
        single_policy_scenario_optimization(
            global_scenario_name=BACKGROUND,
            technology_index=tech_idx,
            include_geologic_h2=include_geologic_h2,
            geologic_h2_availability=geologic_h2_availability,
            drop_in_only=drop_in_only,
            fossil_kerosene_only=fossil_kerosene_only,
            low_demand_formulation=low_demand_formulation,
            preferential_energy=preferential_energy,
            load_optimum=True,
            plot_optimum=False,
            save_optimum=False,
            save_figs=False,
        )
        for tech_idx in range(3)
    ]


# %%
# Load all variants
# ^^^^^^^^^^^^^^^^^
scenario_tech_outputs = {
    # "Baseline SSP2": load_results(drop_in_only=True, fossil_kerosene_only=True),
    "Breakthrough trend": load_results(),
    "Breakthrough trend GeoH2": load_results(include_geologic_h2=True),
    "Breakthrough availability GeoH2": load_results(include_geologic_h2=True, preferential_energy=True),
    "Breakthrough low-demand GeoH2": load_results(include_geologic_h2=True, low_demand_formulation=True),
}

# %%
# Technology scenario trends
# ^^^^^^^^^^^^^^^^^^^^^^^^^^
plot_tech_scenarios_trends(
    scenario_outputs=scenario_tech_outputs,
    colors=["#7F7F7F", "#FF7F0E", "#1F77B4", "#2CA02C"],
    save_fig=False,
)

# %%
# Jet fuel composition over time
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
plot_tech_scenario_jet_fuel(
    scenario_outputs=scenario_tech_outputs,
    colors=["#7F7F7F", "#FF7F0E", "#1F77B4", "#2CA02C"],
    save_fig=False,
    zoom_efuel=True,
)

# %%
# Fleet energy carriers
# ^^^^^^^^^^^^^^^^^^^^^
plot_tech_scenario_fleet_carriers(
    scenario_outputs=scenario_tech_outputs,
    colors=["#7F7F7F", "#FF7F0E", "#1F77B4", "#2CA02C"],
    save_fig=False,
    zoom_battery=True,
)
