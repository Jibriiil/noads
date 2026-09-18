
# Test: Geological hydrogen

import itertools
from noads.application.examples import single_policy_scenario_optimization


# # results_per_tech = []
# tech_scenarios=[0,1,2]
# geo_h2_options=["pessimistic","moderate", "optimistic"]
# for tech, geo_h2_option in itertools.product(tech_scenarios, geo_h2_options):
# # for geo_h2_option in geo_h2_options:
#     result = single_policy_scenario_optimization(
#     global_scenario_name="SSP2-26",
#     carbon_budget_percent=3.0,
#     technology_index=1,  # tech scenario
#     include_geologic_h2= True,
#     geologic_h2_availability=geo_h2_option,  # "pessimistic", "moderate"
#     drop_in_only= False,       
#     fossil_kerosene_only= False,
#     low_demand_formulation=False,
#     preferential_energy= False,
#     load_optimum= False,        # False to force a complete run, not a reload
#     plot_optimum=True,
#     save_optimum= True,
#     save_figs= True,
#     save_history_view=False,)
#     # results_per_tech.append(result)
# # print(results)
# # print(results)

"""
Breakthrough aircraft: comparison of all variants

"""

from noads.application.examples import single_policy_scenario_optimization
from noads.application.visualization import plot_tech_scenario_fleet_carriers
from noads.application.visualization import plot_tech_scenario_jet_fuel
from noads.application.visualization import plot_tech_scenarios_trends

BACKGROUND = "SSP2-26"

def load_results(
    include_geologic_h2= False,
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
            geologic_h2_availability=geologic_h2_option,
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
        for geologic_h2_option in ["pessimistic", "moderate", "optimistic"]
    ]


# Load all variants

scenario_tech_outputs = {
    # "Baseline SSP2": load_results(drop_in_only=True, fossil_kerosene_only=True),
    # "Breakthrough trend": load_results(),
    "Breakthrough availability": load_results(preferential_energy=True),
    "Breakthrough trend GeoH2": load_results(include_geologic_h2=True),
    "Breakthrough availability GeoH2": load_results(include_geologic_h2=True, preferential_energy=True),
    # "Breakthrough low-demand GeoH2": load_results(include_geologic_h2=True, low_demand_formulation=True),
}

# Technology scenario trends

plot_tech_scenarios_trends(
    scenario_outputs=scenario_tech_outputs,
    colors=["#7F7F7F", "#FF7F0E", "#1F77B4", "#2CA02C"],
    save_fig=False, directory_filename="noads/result"
)

# # Jet fuel composition over time
# plot_tech_scenario_jet_fuel(
#     scenario_outputs=scenario_tech_outputs,
#     colors=["#7F7F7F", "#FF7F0E", "#1F77B4", "#2CA02C"],
#     save_fig=False,
#     zoom_efuel=True,
# )

# # Fleet energy carriers
# plot_tech_scenario_fleet_carriers(
#     scenario_outputs=scenario_tech_outputs,
#     colors=["#7F7F7F", "#FF7F0E", "#1F77B4", "#2CA02C"],
#     save_fig=False,
#     zoom_battery=True,
# )

