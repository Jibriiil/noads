#%%
import os
from pathlib import Path

# Results of the GCAM runs in this folder ("update" added to the name)
try:
    GEOH2_DIR = Path(__file__).resolve().parent
except NameError:  # interactive window
    GEOH2_DIR = Path.cwd()
if GEOH2_DIR.name != "geologic_h2":  # launched from the repository root
    GEOH2_DIR = Path.cwd() / "docs" / "examples" / "optimization" / "geologic_h2"
os.environ["NOADS_RESULTS_DIR"] = str(GEOH2_DIR)

FIG_DIR = GEOH2_DIR / "Figures_breakthrough_gcam_geoh2"  
FIG_DIR.mkdir(exist_ok=True)
#%%

from noads.application.examples import single_policy_scenario_optimization
from noads.application.visualization import (
    plot_tech_scenarios_trends,
    plot_tech_scenario_jet_fuel,
    plot_tech_scenario_fleet_carriers,
)

#%%
TECH_SCENARIOS = [1]


def load_results(world, drop_in_only=False):
    return [
        single_policy_scenario_optimization(
            global_scenario_name=world,
            technology_index=tech_idx,
            include_geologic_h2=world != "NoGeoH2",
            drop_in_only=drop_in_only,
            preferential_energy=True,
            aircraft_model="update",
            timeline="paper",
            load_optimum=True,
            plot_optimum=False,
            save_optimum=False,
            save_figs=False,
        )
        for tech_idx in TECH_SCENARIOS
    ]


scenario_tech_outputs = {
    "Breakthrough avail. - No GeoH2": load_results("NoGeoH2"),
    "Breakthrough avail. - GeoH2 $2/kg": load_results("GeoH2-2"),
    "Breakthrough avail. - GeoH2 LowAlt $2/kg": load_results("GeoH2-LowAlt-2"),
}
colors = ["#d62728", "#1f77b4", "#50df50"]

#%%
plot_tech_scenarios_trends(scenario_tech_outputs, colors, save_fig=True)

#%%
plot_tech_scenario_jet_fuel(scenario_tech_outputs, colors, save_fig=True)

#%%
plot_tech_scenario_fleet_carriers(scenario_tech_outputs, colors, zoom_battery=True, save_fig=True)
# %%