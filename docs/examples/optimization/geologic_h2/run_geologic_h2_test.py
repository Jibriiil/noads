
# Test: Geological (white) hydrogen, moderate availability


from noads.application.examples import single_policy_scenario_optimization

# Case: Breakthrough trend SSP2-2.6, mid-tech, moderate geological H2 availability
# So, drop_in_only=False, preferential_energy=False, fossil_kerosene_only=False, include_geologic_h2=True, geologic_h2_availability="moderate"
# ie SSP2-26-GeoH2-mod-midTech

# TEST Breakthrough availability SSP2-2.6, mid-tech
# results_per_tech = []

result = single_policy_scenario_optimization(
    global_scenario_name="SSP2-26",
    carbon_budget_percent=3.0,
    technology_index=1,  # mid-tech
    include_geologic_h2= True,
    geologic_h2_availability="optimistic",
    drop_in_only= False,       
    fossil_kerosene_only= False,
    low_demand_formulation=False,
    preferential_energy= True,
    load_optimum= False,        # False to force a complete run, not a reload
    plot_optimum=True,
    save_optimum= True,
    save_figs= True,
    save_history_view=False,
)
    # results_per_tech.append(result)
# print(results)
# print(results)

# TEST GEMSEO