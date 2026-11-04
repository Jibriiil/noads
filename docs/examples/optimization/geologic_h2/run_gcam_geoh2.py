# Runs: geological hydrogen with GCAM backgrounds (CMIP7 Low CO2 constraint)
#%%
import itertools
from noads.application.examples import single_policy_scenario_optimization

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

#%%
# All gcam scenarios 
# gcam_scenario_to_model = {
#     "NoGeoH2": GCAM_MODEL,
#     "GeoH2-1": GCAM_MODEL,
#     "GeoH2-2": GCAM_MODEL,
#     "GeoH2-3": GCAM_MODEL,
#     "GeoH2-LowAlt-1": GCAM_MODEL,
#     "GeoH2-LowAlt-2": GCAM_MODEL,
#     "GeoH2-LowAlt-3": GCAM_MODEL,
# }

WORLDS = ["NoGeoH2", "GeoH2-2", "GeoH2-LowAlt-2"]
# WORLDS=["GeoH2-2"]
# DROP_IN_ONLY = [True, False]  # drop-in, breakthrough
DROP_IN_ONLY = [True]  # drop-in, breakthrough
TECH_SCENARIOS = [1]  # 0: Lower, 1: Mid, 2: Upper

for world, drop_in_only, tech in itertools.product(WORLDS, DROP_IN_ONLY, TECH_SCENARIOS):
    single_policy_scenario_optimization(
        global_scenario_name=world,
        carbon_budget_percent=3.0,
        technology_index=tech,
        include_geologic_h2=world != "NoGeoH2",
        drop_in_only=drop_in_only,
        fossil_kerosene_only=False,
        low_demand_formulation=False,
        preferential_energy=True,
        aircraft_model="update",
        timeline="paper",
        load_optimum=True,  # False to force a complete run, not a reload
        plot_optimum=True,
        save_optimum=True,
        save_figs=True,
        save_history_view=False,
    )
# %%