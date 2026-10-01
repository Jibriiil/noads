
#%%
# Importations
from pathlib import Path
# import os
# os.environ["NOADS_RESULTS_DIR"] = str(Path(__file__).resolve().parents[5] / "results")
# print("NOADS_RESULTS_DIR =", os.environ["NOADS_RESULTS_DIR"])
from noads.application.examples import single_policy_scenario_optimization
from noads.application.visualization import (
    plot_tech_scenarios_trends,
    plot_tech_scenario_jet_fuel,
    plot_tech_scenario_fleet_carriers,
)

# FIG_DIR = Path(__file__).resolve().parent / "breakthrough_GeoH2"
# FIG_DIR.mkdir(exist_ok=True)

#%%
BACKGROUND = "SSP2-26"

def load_results_for_geoh2(include_geologic_h2=True, geologic_h2_option="Optimistic", preferential_energy=False, low_demand_formulation=False):
    return [
        single_policy_scenario_optimization(
            global_scenario_name=BACKGROUND,
            technology_index=tech_idx,
            include_geologic_h2=include_geologic_h2,
            geologic_h2_availability=geologic_h2_option,
            drop_in_only=False,
            low_demand_formulation=low_demand_formulation,
            preferential_energy=preferential_energy,
            load_optimum=True,
            plot_optimum=False,
            save_optimum=True,
            save_figs=False,
        )
        for tech_idx in range(2)
    ]

scenario_tech_outputs = {
    "Breakth.": load_results_for_geoh2(include_geologic_h2=False, preferential_energy=False),
    "Breakth. - Pess GeoH2": load_results_for_geoh2(include_geologic_h2=True, geologic_h2_option="Pessimistic", preferential_energy=False),
    "Breakth. - Mod GeoH2": load_results_for_geoh2(include_geologic_h2=True, geologic_h2_option="Moderate", preferential_energy=False),
    "Breakth. - Opt GeoH2": load_results_for_geoh2(include_geologic_h2=True, geologic_h2_option="Optimistic", preferential_energy=False),
}

colors = ["#d62728", "#ff7f0e","#1f77b4", "#50df50"]
#,"#bc87ea"

#%%#
plot_tech_scenarios_trends(scenario_tech_outputs, colors, save_fig=True)
#%%

plot_tech_scenario_jet_fuel(scenario_tech_outputs, colors, save_fig=True)


#%%
plot_tech_scenario_fleet_carriers(scenario_tech_outputs, colors, save_fig=True,zoom_battery=True)
# %%
