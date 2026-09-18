
# Test: Geological hydrogen

import itertools
from noads.application.examples import single_policy_scenario_optimization


# # results_per_tech = []
tech_scenarios=[0,1,2]
geo_h2_options=["pessimistic","moderate", "optimistic"]
for tech, geo_h2_option in itertools.product(tech_scenarios, geo_h2_options):
# for geo_h2_option in geo_h2_options:
    result = single_policy_scenario_optimization(
    global_scenario_name="SSP2-26",
    carbon_budget_percent=3.0,
    technology_index=1,  # tech scenario
    include_geologic_h2= True,
    geologic_h2_availability=geo_h2_option,  # "pessimistic", "moderate"
    drop_in_only= False,       
    fossil_kerosene_only= False,
    low_demand_formulation=False,
    preferential_energy= False,
    load_optimum= False,        # False to force a complete run, not a reload
    plot_optimum=True,
    save_optimum= True,
    save_figs= True,
    save_history_view=False,)
    # results_per_tech.append(result)
# print(results)
# print(results)
