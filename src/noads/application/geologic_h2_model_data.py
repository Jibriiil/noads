"""Built from the shale-gas-analogue model and the analysis of SSPs scenarios . Only the mean/central exponential-decay curve is kept here (no
Monte Carlo, no external CSV dependency).
"""

import numpy as np
from scipy.optimize import curve_fit

# Conversions
H2_LHV_MJ_PER_KG = 120.0
KG_PER_MT = 1e9
J_PER_MJ = 1e6

def get_geologic_h2_resources(noads_start_year=2030, end_year=2080, production_start_year=2030, md0=1.0):
    production_years = np.arange(production_start_year, end_year + 1)
    md_mt_per_year = build_hydrogen_demand_shale_gas_only(
        production_years, min_range=0.8, max_range=1.2, md0=md0
    )[0]
    # pre_years = np.arange(noads_start_year, production_start_year)
    # years = np.concatenate((pre_years, production_years))
    # epsilon_mt = 1e-9  # négligeable physiquement 
    # values_mt_per_year= np.concatenate([np.full_like(pre_years, epsilon_mt, dtype=float), md_mt_per_year])

    production_j_per_year = md_mt_per_year * KG_PER_MT * H2_LHV_MJ_PER_KG * J_PER_MJ
    return production_years, production_j_per_year

def build_hydrogen_demand_shale_gas_only(years, min_range=0.8, max_range=1.2, md0=1.0):
    "Central geological H2 production curve (Mt/year), shale-gas-analogue decay."
    all_rates = fit_exp_decay(years, min_range, max_range)
    all_k = np.log(all_rates + 1)
    all_k_cumsum = all_k.copy()
    all_k_cumsum[:, 0] = 0
    return md0 * np.exp(np.cumsum(all_k_cumsum, axis=1))

def fit_exp_decay(
    eval_years,
    min_range,
    max_range,
    years=np.array([2031, 2045, 2100]),
    growth_rates=np.array([0.7, 0.1, 0.06]),
):
    popt, _ = curve_fit(
        exp_decay, years, growth_rates, p0=[0.7, 0.05, 0.05],
        bounds=([0, 0, 0], [np.inf, 1, 1]), maxfev=5000)

    return np.array([
        exp_decay(eval_years, *popt),
        min_range * exp_decay(eval_years, *popt),
        max_range * exp_decay(eval_years, *popt),
    ])

def exp_decay(t, a, b, c):
    return a * np.exp(-b * (t - 2031)) + c