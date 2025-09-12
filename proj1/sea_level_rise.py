import numpy as np

ssp1_1p9_2050 = np.array([0.15, 0.23])
ssp5_8p5_2050 = np.array([0.20, 0.29])

ssp1_1p9_2100 = np.array([0.28, 0.55])
ssp5_8p5_2100 = np.array([0.63, 1.01])

ssp1_1p9_2150 = np.array([0.37, 0.86])
ssp5_8p5_2150 = np.array([0.98, 1.88])

ipcc_projections = np.array([
    [0.15, 0.23],
    [0.20, 0.29],
    [0.28, 0.55],
    [0.63, 1.01],
    [0.37, 0.86],
    [0.98, 1.88]
])

time_periods = ['2050', '2050', '2100', '2100', '2150', '2150']
scenarios = ['SSP1-1.9', 'SSP5-8.5', 'SSP1-1.9', 'SSP5-8.5', 'SSP1-1.9', 'SSP5-8.5']

high_end_2100 = 2.0
high_end_2150 = 5.0

historical_rise_1900_2018 = 0.20
current_rate_mm_per_year = 3.7
historical_rate_mm_per_year = 1.3
baseline_adjustment_1900 = 0.158

scenario_temps = {
    'SSP1-1.9': 1.4,
    'SSP2-4.5': 2.7,
    'SSP5-8.5': 4.4
}

ipcc_projections_cm = ipcc_projections * 100
ssp1_1p9_2050_cm = ssp1_1p9_2050 * 100
ssp5_8p5_2050_cm = ssp5_8p5_2050 * 100
ssp1_1p9_2100_cm = ssp1_1p9_2100 * 100
ssp5_8p5_2100_cm = ssp5_8p5_2100 * 100
ssp1_1p9_2150_cm = ssp1_1p9_2150 * 100
ssp5_8p5_2150_cm = ssp5_8p5_2150 * 100

high_end_2100_cm = high_end_2100 * 100
high_end_2150_cm = high_end_2150 * 100
historical_rise_1900_2018_cm = historical_rise_1900_2018 * 100

sea_level_data = {
    'projections_meters': {
        '2050': {
            'low_emissions': ssp1_1p9_2050,
            'high_emissions': ssp5_8p5_2050
        },
        '2100': {
            'low_emissions': ssp1_1p9_2100,
            'high_emissions': ssp5_8p5_2100
        },
        '2150': {
            'low_emissions': ssp1_1p9_2150,
            'high_emissions': ssp5_8p5_2150
        }
    },
    'high_end_scenarios': {
        '2100': high_end_2100,
        '2150': high_end_2150
    },
    'historical': {
        'total_rise_since_1900': historical_rise_1900_2018,
        'current_rate_mm_year': current_rate_mm_per_year,
        'historical_rate_mm_year': historical_rate_mm_per_year,
        'baseline_adjustment': baseline_adjustment_1900
    },
    'scenario_definitions': scenario_temps
}

