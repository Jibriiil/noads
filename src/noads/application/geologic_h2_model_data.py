"""Built from the shale-gas-analogue model and the analysis of SSPs scenarios . Only the mean/central exponential-decay curve is kept here (no
Monte Carlo, no external CSV dependency).
"""

import numpy as np
from scipy.optimize import curve_fit

# Conversions
H2_LHV_MJ_PER_KG = 120.0
KG_PER_MT = 1e9
# J_PER_MJ = 1e6

def get_geologic_h2_resources(Geo_H2_option= "Optimistic", noads_start_year=2030, production_start_year=2030, production_end_year=2080, md0=1.0):
    """Get geological H2 production (MJ/year) from shale-gas-analogue model."""
    
    production_years = np.arange(production_start_year, production_end_year + 1)
    md_mt_per_year = build_GeoH2_production(eval_years= production_years, GeoH2_option= Geo_H2_option, MD0= md0)
    
    # pre_years = np.arange(noads_start_year, production_start_year)
    # years = np.concatenate((pre_years, production_years))
    # epsilon_mt = 1e-9  # négligeable physiquement 
    # values_mt_per_year= np.concatenate([np.full_like(pre_years, epsilon_mt, dtype=float), md_mt_per_year])

    production_j_per_year = md_mt_per_year * KG_PER_MT * H2_LHV_MJ_PER_KG
    return production_years, production_j_per_year

def build_GeoH2_production(eval_years=np.arange(2030,2081), GeoH2_option= "Optimistic", MD0=1.0):
    """
    Building the geological hydrogen production using GeoH2_option which is based on growth rates decay models
    """

    valid_options = ("Pessimistic", "Moderate", "Optimistic")
    
    if GeoH2_option not in valid_options: raise ValueError( f"Invalid GeoH2_option: {GeoH2_option!r}. Must be one of {valid_options}.")

    if GeoH2_option == "Pessimistic":
        all_rates = fit_exp_decay(eval_years, years=np.array([2031, 2039, 2080]), growth_rates=np.array([0.55, 0.1, 0.03]))
    elif GeoH2_option == "Optimistic":
        all_rates = fit_exp_decay(eval_years, years=np.array([2031, 2046, 2080]), growth_rates=np.array([0.85, 0.1, 0.03]))
    else:  # "Moderate"
        all_rates = np.mean([
            fit_exp_decay(eval_years, years=np.array([2031, 2039, 2080]), growth_rates=np.array([0.55, 0.1, 0.03])),
            fit_exp_decay(eval_years, years=np.array([2031, 2046, 2080]), growth_rates=np.array([0.85, 0.1, 0.03])),
        ], axis=0)

    # shale gas analog: exp decay of growth rates
    all_k = np.log(all_rates + 1)
   
    # Copy for not altering the data
    all_k_cumsum=all_k.copy()
    all_k_cumsum[0]=0  # for MD0, 1D.

    MD= MD0 * np.exp(np.cumsum(all_k_cumsum))
    return MD

def fit_exp_decay(eval_years, years, growth_rates):
    popt,pcov= curve_fit(exp_decay, years, growth_rates, p0=[0.7, 0.05, 0.05],bounds=([0,0,0],[np.inf,1,1]), maxfev=5000) 
    
    return np.array(exp_decay(eval_years, *popt))

def exp_decay(t, a, b, c):
    return a * np.exp(-b * (t - 2031)) + c

