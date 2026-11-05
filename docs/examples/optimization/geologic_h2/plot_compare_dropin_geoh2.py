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

FIG_DIR = GEOH2_DIR / "Figures_dropin_gcam_geoh2"  
FIG_DIR.mkdir(exist_ok=True)
#%%

from noads.application.examples import single_policy_scenario_optimization
from noads.application.visualization import (
    plot_tech_scenarios_trends,
    plot_tech_scenario_jet_fuel,
    plot_tech_scenario_fleet_carriers,
    _setup_trend_axes,
    _plot_trend_data,
    _configure_trend_axes,
)
from matplotlib.lines import Line2D
from scipy.integrate import cumulative_trapezoid
#%%
TECH_SCENARIOS = [1]


def load_results(world, drop_in_only=True):
    return [
        single_policy_scenario_optimization(
            global_scenario_name=world,
            technology_index=tech,
            include_geologic_h2=world != "NoGeoH2",
            drop_in_only=drop_in_only,
            preferential_energy= False,
            aircraft_model="update",
            timeline="paper",
            load_optimum=True,
            plot_optimum=False,
            save_optimum=False,
            save_figs=False,
        )
        for tech in TECH_SCENARIOS
    ]


scenario_tech_outputs = {
    r'Dropin trend No GeoH$_2$': load_results("NoGeoH2"),
    r'Dropin trend GeoH$_2$  \$2/kg': load_results("GeoH2-2"),
    r'Dropin trend GeoH$_2$LowAlt \$2/kg': load_results("GeoH2-LowAlt-2"),
}
colors = ["#d62728", "#1f77b4", "#50df50"]

#%%
# Modified functions

def plot_tech_scenarios_trends_GCAM(
    scenario_outputs,
    colors,
    save_fig=False,
    directory_filename=".",
):
    """Plot scenario comparison with mid tech only. Adjust the legend (comments) when plotting the 3 techs"""
    fig, axes, scales = _setup_trend_axes()

    for i, (scenario, output_list) in enumerate(scenario_outputs.items()):
        for j, output_optimal in enumerate(output_list):
            years = output_optimal["year"]
            linestyle = "-" if j == 0 else (":" if j == 1 else "--")
            linewidth = 3.5 - 0.5 * i
            label = scenario if j == 0 else None

            # Skip plotting the line for the last scenario (j == 2)
            if j != 2:
                _plot_trend_data(
                    axes,
                    scales,
                    years,
                    output_optimal,
                    color=colors[i],
                    linestyle=linestyle,
                    linewidth=linewidth,
                    label=label,
                )

        # Add fill_between for lower to upper technology range
        if len(output_list) >= 3:
            years = output_list[0]["year"]

            # RPK fill
            axes["rpk"].fill_between(
                years,
                output_list[0]["rpk"] * 1e-12,
                output_list[2]["rpk"] * 1e-12,
                color=colors[i],
                alpha=0.2,
            )

            # CO2 fill
            axes["co2"].fill_between(
                years,
                output_list[0]["CO2"] * 1e-12,
                output_list[2]["CO2"] * 1e-12,
                color=colors[i],
                alpha=0.2,
            )

            # Energy intensity fill
            axes["energy"].fill_between(
                years,
                output_list[0]["mean_energy_per_ask"],
                output_list[2]["mean_energy_per_ask"],
                color=colors[i],
                alpha=0.2,
            )

            # Carbon intensity fill
            co2_per_ask_lower = (
                output_list[0]["JET-A.mean_consumption_per_ask"]
                * output_list[0]["JET-A.CO2_index"]
            )
            co2_per_ask_upper = (
                output_list[2]["JET-A.mean_consumption_per_ask"]
                * output_list[2]["JET-A.CO2_index"]
            )
            axes["carbon"].fill_between(
                years, co2_per_ask_lower, co2_per_ask_upper, color=colors[i], alpha=0.2
            )

            # Carbon budget fill
            integrated_co2_lower = (
                cumulative_trapezoid(output_list[0]["CO2"], years, initial=0) * 1e-15
            )
            integrated_co2_upper = (
                cumulative_trapezoid(output_list[2]["CO2"], years, initial=0) * 1e-15
            )
            axes["budget"].fill_between(
                years,
                integrated_co2_lower,
                integrated_co2_upper,
                color=colors[i],
                alpha=0.2,
            )

    tech_legend = [
        # Line2D([0], [0], color="k", ls="-", lw=2, label="Lower technology"),
        # Line2D([0], [0], color="k", ls=":", lw=2, label="Mid technology"),
        # Patch(facecolor="k", alpha=0.3, label="Upper to lower tech"),
        # Line2D([0], [0], color="k", ls="-", lw=2, label="Mid technology"),
    ]
    axes["energy"].legend(loc="lower left", framealpha=0.5)
    axes["carbon"].legend(handles=tech_legend, loc="lower left", framealpha=0.5)

    year_start = next(iter(scenario_outputs.values()))[0]["year"][0]
    year_end = next(iter(scenario_outputs.values()))[0]["year"][-1]
    _configure_trend_axes(axes, scales, year_start, year_end)

    fig.canvas.draw()
    fig.tight_layout()

    if save_fig:
        fig.savefig(f"{directory_filename}.pdf")
    else:
        fig.show()

#%%
plot_tech_scenarios_trends_GCAM(scenario_tech_outputs, colors, save_fig=True, directory_filename=str(FIG_DIR / "Dropin_trend_trends_MidTech"))

# %%
plot_tech_scenario_jet_fuel(scenario_tech_outputs, colors, zoom_efuel=True,save_fig=True, directory_filename=str(FIG_DIR / "Dropin_trend_jetfuel_MidTech"))

#%%
plot_tech_scenario_fleet_carriers(scenario_tech_outputs, colors, zoom_battery=True, save_fig=True, directory_filename=str(FIG_DIR / "Dropin_trend_fleet_carriers_MidTech"))
# %%
%%
