import rasterio
import numpy as np
import matplotlib.pyplot as plt
import sys
import os

sys.path.append('src')
import sea_level_rise as slr

tif_path = "data/output_be.tif"

def load_and_process_dem(tif_path):
    with rasterio.open(tif_path) as dataset:
        elevation = dataset.read(1)
        transform = dataset.transform
        nodata = dataset.nodata
        
    elevation = np.clip(elevation, 0, 200)
    elevation_rot = elevation.T
    elevation_rot = np.rot90(elevation_rot, k=1)
    
    return elevation_rot, transform, nodata

def generate_current_elevation_map(elevation_rot, output_dir):
    fig = plt.figure(figsize=(12, 10))
    
    height_px, width_px = elevation_rot.shape
    width_km = 300
    height_km = 200
    
    extent = [0, width_km, 0, height_km]
    
    plt.imshow(elevation_rot, cmap="terrain", origin='lower', extent=extent)
    plt.colorbar(label="Elevation (m above NAP)", shrink=0.8)
    plt.title("Netherlands Digital Elevation Model\n(Normal Amsterdam Peil - NAP)", fontsize=16, fontweight='bold')
    
    plt.xlabel("Distance (km)", fontsize=12, fontweight='bold')
    plt.ylabel("Distance (km)", fontsize=12, fontweight='bold')
    
    plt.grid(True, alpha=0.3, color='white', linewidth=0.5)
    
    plt.tight_layout()
    
    filename = "netherlands_current_elevation.png"
    fig.savefig(os.path.join(output_dir, filename), dpi=300, bbox_inches='tight')
    plt.close(fig)

def generate_sea_level_projections(output_dir):
    scenarios_2100 = slr.sea_level_data['projections_meters']['2100'] 
    scenarios_2150 = slr.sea_level_data['projections_meters']['2150']
    
    low_rate = (scenarios_2150['low_emissions'][1] - scenarios_2100['low_emissions'][1]) / 5
    high_rate = (scenarios_2150['high_emissions'][1] - scenarios_2100['high_emissions'][1]) / 5
    
    scenarios_2300 = {
        'low_emissions': scenarios_2150['low_emissions'][1] + low_rate * 15,
        'high_emissions': scenarios_2150['high_emissions'][1] + high_rate * 15
    }
    scenarios_2500 = {
        'low_emissions': scenarios_2150['low_emissions'][1] + low_rate * 35,
        'high_emissions': scenarios_2150['high_emissions'][1] + high_rate * 35
    }
    
    projection_years = [2050, 2100, 2150, 2300, 2500]
    
    low_emissions_2050 = slr.sea_level_data['projections_meters']['2050']['low_emissions'][1]
    low_emissions_2100 = slr.sea_level_data['projections_meters']['2100']['low_emissions'][1]
    low_emissions_2150 = slr.sea_level_data['projections_meters']['2150']['low_emissions'][1]
    
    high_emissions_2050 = slr.sea_level_data['projections_meters']['2050']['high_emissions'][1]
    high_emissions_2100 = slr.sea_level_data['projections_meters']['2100']['high_emissions'][1]
    high_emissions_2150 = slr.sea_level_data['projections_meters']['2150']['high_emissions'][1]
    
    low_emissions_2300 = scenarios_2300['low_emissions']
    low_emissions_2500 = scenarios_2500['low_emissions']
    high_emissions_2300 = scenarios_2300['high_emissions']
    high_emissions_2500 = scenarios_2500['high_emissions']
    
    low_scenario = [low_emissions_2050, low_emissions_2100, low_emissions_2150, low_emissions_2300, low_emissions_2500]
    high_scenario = [high_emissions_2050, high_emissions_2100, high_emissions_2150, high_emissions_2300, high_emissions_2500]
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    ax.plot(projection_years[:3], low_scenario[:3], 'b-', linewidth=3, marker='o', markersize=8, 
            label='Low Emissions (SSP1-1.9) - IPCC Data', alpha=0.9, zorder=3)
    ax.plot(projection_years[:3], high_scenario[:3], 'r-', linewidth=3, marker='s', markersize=8, 
            label='High Emissions (SSP5-8.5) - IPCC Data', alpha=0.9, zorder=3)
    
    ax.plot(projection_years[2:], low_scenario[2:], 'b--', linewidth=2, marker='o', markersize=6, 
            label='Low Emissions - Extrapolated', alpha=0.7, zorder=2)
    ax.plot(projection_years[2:], high_scenario[2:], 'r--', linewidth=2, marker='s', markersize=6, 
            label='High Emissions - Extrapolated', alpha=0.7, zorder=2)
    
    ax.fill_between(projection_years, low_scenario, high_scenario, 
                    alpha=0.2, color='gray', label='Projection Range')
    
    ax.axvline(x=2150, color='gray', linestyle=':', alpha=0.7, linewidth=2)
    ax.text(2150, max(high_scenario) * 0.5, 'IPCC | Extrapolation', 
            rotation=90, ha='right', va='center', fontsize=10, alpha=0.7)
    
    ax.set_xlabel('Year', fontsize=14, fontweight='bold')
    ax.set_ylabel('Sea Level Rise (meters above current level)', fontsize=14, fontweight='bold')
    ax.set_title('IPCC AR6 Sea Level Rise Projections\n(with Linear Extrapolations to 2500)', 
                fontsize=16, fontweight='bold', pad=20)
    
    ax.grid(True, alpha=0.3)
    ax.legend(loc='upper left', fontsize=11, framealpha=0.9)
    
    ax.set_ylim(0, max(high_scenario) * 1.1)
    ax.set_xlim(2040, 2520)
    
    key_points = [
        (2100, low_emissions_2100, f'{low_emissions_2100:.2f}m'),
        (2100, high_emissions_2100, f'{high_emissions_2100:.2f}m'),
        (2500, low_emissions_2500, f'{low_emissions_2500:.2f}m'),
        (2500, high_emissions_2500, f'{high_emissions_2500:.2f}m')
    ]
    
    for year, rise, label in key_points:
        ax.annotate(label, (year, rise), xytext=(10, 10), textcoords='offset points',
                   fontsize=10, fontweight='bold', 
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8),
                   arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
    
    plt.tight_layout()
    
    filename = "sea_level_rise_projections.png"
    fig.savefig(os.path.join(output_dir, filename), dpi=300, bbox_inches='tight')
    plt.close(fig)

def generate_flooding_mosaic(elevation_rot, output_dir):
    scenarios_2100 = slr.sea_level_data['projections_meters']['2100'] 
    scenarios_2150 = slr.sea_level_data['projections_meters']['2150']
    
    low_rate = (scenarios_2150['low_emissions'][1] - scenarios_2100['low_emissions'][1]) / 5
    high_rate = (scenarios_2150['high_emissions'][1] - scenarios_2100['high_emissions'][1]) / 5
    
    scenarios_2300 = {
        'low_emissions': scenarios_2150['low_emissions'][1] + low_rate * 15,
        'high_emissions': scenarios_2150['high_emissions'][1] + high_rate * 15
    }
    scenarios_2500 = {
        'low_emissions': scenarios_2150['low_emissions'][1] + low_rate * 35,
        'high_emissions': scenarios_2150['high_emissions'][1] + high_rate * 35
    }
    
    scenarios = {
        '2100': {
            'low': scenarios_2100['low_emissions'][0],
            'medium': np.mean([scenarios_2100['low_emissions'][1], scenarios_2100['high_emissions'][0]]),
            'high': scenarios_2100['high_emissions'][1]
        },
        '2300': {
            'low': scenarios_2300['low_emissions'],
            'medium': np.mean([scenarios_2300['low_emissions'], scenarios_2300['high_emissions']]),
            'high': scenarios_2300['high_emissions']
        },
        '2500': {
            'low': scenarios_2500['low_emissions'],
            'medium': np.mean([scenarios_2500['low_emissions'], scenarios_2500['high_emissions']]),
            'high': scenarios_2500['high_emissions']
        }
    }
    
    total_coverage_area_km2 = 49667
    pixel_area_km2 = total_coverage_area_km2 / elevation_rot.size
    
    fig, axes = plt.subplots(3, 3, figsize=(18, 15))
    
    years = ['2100', '2300', '2500']
    scenario_names = ['Optimistic\n(Low Emissions)', 'Medium\n(Mixed Action)', 'Pessimistic\n(High Emissions)']
    scenario_keys = ['low', 'medium', 'high']
    
    for i, year in enumerate(years):
        for j, (scenario_name, scenario_key) in enumerate(zip(scenario_names, scenario_keys)):
            ax = axes[j, i]
            
            sea_level_rise = scenarios[year][scenario_key]
            
            initial_land = elevation_rot > 0
            remaining_land = elevation_rot > sea_level_rise
            
            initial_land_area_km2 = np.sum(initial_land) * pixel_area_km2
            remaining_land_area_km2 = np.sum(remaining_land) * pixel_area_km2
            land_lost_km2 = initial_land_area_km2 - remaining_land_area_km2
            
            visualization = np.zeros((elevation_rot.shape[0], elevation_rot.shape[1], 3))
            
            visualization[remaining_land] = [0.0, 0.0, 0.0]
            
            ocean_mask = ~initial_land
            visualization[ocean_mask] = [1.0, 1.0, 1.0]
            
            land_lost_mask = initial_land & ~remaining_land
            visualization[land_lost_mask] = [1.0, 0.0, 0.0]
            
            ax.imshow(visualization, origin='lower')
            
            if j == 0:
                ax.set_title(f'Year {year}', fontsize=16, fontweight='bold', color='black')
            ax.set_xticks([])
            ax.set_yticks([])
            
            if land_lost_km2 < 1 and sea_level_rise < 1.0:
                land_lost_text = "Unknown"
            else:
                land_lost_text = f"{land_lost_km2:,.0f} km²"
            
            info_text = f'+{sea_level_rise:.2f}m rise\n{land_lost_text} lost'
            ax.text(0.02, 0.98, info_text, transform=ax.transAxes, fontsize=10, 
                   fontweight='bold', color='black', verticalalignment='top',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
            
            for spine in ax.spines.values():
                spine.set_linewidth(1)
                spine.set_color('black')
    
    for j, scenario_name in enumerate(scenario_names):
        axes[j, 0].set_ylabel(scenario_name, fontsize=16, fontweight='bold', 
                             rotation=90, labelpad=25, color='black')
    
    legend_elements = [
        plt.Rectangle((0,0),1,1, facecolor=[0.0, 0.0, 0.0], label='Remaining Land', edgecolor='black'),
        plt.Rectangle((0,0),1,1, facecolor=[1.0, 1.0, 1.0], label='Ocean', edgecolor='black'),
        plt.Rectangle((0,0),1,1, facecolor=[1.0, 0.0, 0.0], label='Land Lost', edgecolor='black')
    ]
    fig.legend(handles=legend_elements, loc='lower center', ncol=3, fontsize=12, 
               bbox_to_anchor=(0.5, 0.02), frameon=True, fancybox=True, shadow=True)
    
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.12)
    
    filename = "flooding_scenarios_mosaic.png"
    fig.savefig(os.path.join(output_dir, filename), dpi=300, bbox_inches='tight')
    plt.close(fig)

def main():
    output_dir = "../visuals"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    print("Generating visualizations")
    
    elevation_rot, transform, nodata = load_and_process_dem(tif_path)
    
    print("\nElevation map")
    generate_current_elevation_map(elevation_rot, output_dir)
    
    print("\nSea level rise projections")
    generate_sea_level_projections(output_dir)
    
    print("\nFlooding scenarios mosaic")
    generate_flooding_mosaic(elevation_rot, output_dir)

if __name__ == "__main__":
    main()
