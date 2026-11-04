
#%%
import os
from pathlib import Path

try:
    GEOH2_DIR = Path(__file__).resolve().parent
except NameError:  # interactive window
    GEOH2_DIR = Path.cwd()
if GEOH2_DIR.name != "geologic_h2":  # launched from the repository root
    GEOH2_DIR = Path.cwd() / "docs" / "examples" / "optimization" / "geologic_h2"
os.environ["NOADS_RESULTS_DIR"] = str(GEOH2_DIR)
FIG_DIR = GEOH2_DIR / "fleet_mix_gcam_geoh2"
FIG_DIR.mkdir(exist_ok=True)
#%%
from noads.application.examples import single_policy_scenario_optimization
from noads.application.scenario_setup import single_scenario_setup
from noads.application.visualization import plot_fleet_mix_variants

WORLDS = ["NoGeoH2", "GeoH2-2", "GeoH2-LowAlt-2"]

VARIANTS_Breakthrough = {
    "Breakthrough trend": {},
    "Breakthrough availability": {"preferential_energy": True},
    "Breakthrough low-demand": {"low_demand_formulation": True},
}
VARIANTS_Dropin = {
    "Drop-in trend": {"drop_in_only": True},
    "Drop-in availability": {"drop_in_only": True, "preferential_energy": True},
    "Drop-in low-demand": {"drop_in_only": True, "low_demand_formulation": True},
}
TECHNOLOGIES = [1]  
TECH_NAMES = ["Lower", "Mid", "Upper"]  # only the technology that was run

TIMELINES = {"paper": ("", "2025-2075")}  # timeline: (file suffix, period)

FAMILIES = {"Drop-in": VARIANTS_Dropin, "Breakthrough": VARIANTS_Breakthrough}
#%%
def load(world, technology_index, timeline, options):
    return single_policy_scenario_optimization(
        global_scenario_name=world,
        technology_index=technology_index,
        include_geologic_h2=world != "NoGeoH2",
        aircraft_model="update",
        timeline=timeline,
        load_optimum=True,
        plot_optimum=False,
        save_optimum=False,
        save_figs=False,
        **options,
    )
#%%
for timeline, (suffix, period) in TIMELINES.items():
    for technology_index in TECHNOLOGIES:
        technology = TECH_NAMES[technology_index]
        for family, variants in FAMILIES.items():
            drop_in_only = family == "Drop-in"
            # The fleet depends on the technology and on drop_in_only, not on the world.
            _, _, _, _, fleet = single_scenario_setup(
                "fleet-mix", "GeoH2-2",
                technology_index=technology_index,
                plot_scenario_data=False,
                integrate_constraints=False,
                aircraft_model="update",
                drop_in_only=drop_in_only,
                end_year=2100.0 if timeline == "extended" else None,
                last_entry_into_service=2080.0 if timeline == "extended" else None,
                compile_jit=False,
            )

            # Type 1: one world, rows = the three variants of the family (trend, availability, low-demand)
            for world in WORLDS:
                variant_outputs = {
                    variant: load(world, technology_index, timeline, options)
                    for variant, options in variants.items()
                }
                plot_fleet_mix_variants(
                    variant_outputs, fleet,
                    title=f"Fleet Mix - {world} - {family} - {technology} ({period})",
                    save_fig=True,
                    directory_filename=str(
                        FIG_DIR / f"fleet_mix_{world}_{family.lower()}_{technology.lower()}{suffix}.png"
                    ),
                )

            # Type 2: one variant, rows = the three worlds
            for variant, options in variants.items():
                world_outputs = {
                    world: load(world, technology_index, timeline, options)
                    for world in WORLDS
                }
                plot_fleet_mix_variants(
                    world_outputs, fleet,
                    title=f"Fleet Mix - {variant} - {technology} ({period})",
                    save_fig=True,
                    directory_filename=str(
                        FIG_DIR / f"fleet_mix_{variant.replace(' ', '_').lower()}_{technology.lower()}{suffix}.png"
                    ),
                )