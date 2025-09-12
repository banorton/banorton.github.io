# Technical Report: Netherlands Sea Level Rise Impact Analysis

## Sources
- IPCC. (2021). Ocean, cryosphere and sea level change. In Climate change 2021: The physical science basis. Contribution of Working Group I to the Sixth Assessment Report of the Intergovernmental Panel on Climate Change (Chapter 9). Cambridge University Press.
- NASA JPL. (2021). NASADEM merged DEM global 1 arc second V001. Distributed by OpenTopography. https://doi.org/10.5069/G93T9FD9

## Project Overview

This analysis examines potential land loss in the Netherlands under various sea level rise scenarios through 2500. The project uses digital elevation model (DEM) data combined with IPCC AR6 projections to visualize areas that could be affected by different levels of sea level rise.

## Datasets

### 1. Digital Elevation Model (DEM)
- Source: `data/output_be.tif` 
- Coverage: Netherlands region (4.19°E to 7.04°E, 51.37°N to 53.68°N)
- Format: GeoTIFF raster file
- Resolution: 8,445 × 11,019 pixels 
- Total coverage area: ~49,667 km²
- Data type: Integer elevation values in meters

### 2. Sea Level Rise Projections
- Source: IPCC AR6 scenarios implemented in `sea_level_rise.py`
- Time periods: 2050, 2100, 2150 (from IPCC), extended to 2300, 2500 via extrapolation
- Scenarios: 
  - SSP1-1.9 (low emissions): [0.15, 0.23]m (2050), [0.28, 0.55]m (2100), [0.37, 0.86]m (2150)
  - SSP5-8.5 (high emissions): [0.20, 0.29]m (2050), [0.63, 1.01]m (2100), [0.98, 1.88]m (2150)

## Processing

### DEM Processing Pipeline
1. Loading: Used `rasterio` to read GeoTIFF data
3. Spatial transformation: 
   - Transposed matrix (`elevation.T`)
   - Rotated 90° clockwise (`np.rot90(elevation_rot, k=1)`)
4. Area calculation: 
   - Pixel area: 49,667 km² ÷ 93,093,105 pixels = 5.336×10⁻⁴ km²/pixel
   - Land area calculation: `np.sum(elevation > 0) * pixel_area_km2`

### Sea Level Rise Extrapolation
1. Linear trend calculation: 
   - Low emissions rate: `(2150_value - 2100_value) / 5 decades`
   - High emissions rate: Similar calculation for high scenario
2. Projection extension:
   - 2300: 2150 value + rate × 15 decades
   - 2500: 2150 value + rate × 35 decades
3. Scenario matrix creation: 3×3 grid (optimistic/medium/pessimistic × 2100/2300/2500)

### Land Loss Calculation Algorithm
```python
def calculate_land_lost(elevation, sea_level_rise, pixel_area_km2):
    initial_land = elevation > 0  # binary mask for current land
    remaining_land = elevation > sea_level_rise  # land after rise
    
    initial_area = np.sum(initial_land) * pixel_area_km2
    remaining_area = np.sum(remaining_land) * pixel_area_km2
    land_lost = initial_area - remaining_area
    
    return land_lost, flooded_mask
```

## Visualization

### 1. Current Elevation Map
- Chart type: Raster heatmap with terrain colormap
- Rationale: Shows continuous elevation data effectively. Terrain colormap provides intuitive blue-to-brown gradient
- Scale: Converted pixel coordinates to kilometers (0-300km × 0-200km) for geographic context
- Grid overlay: Added white grid for better readability

### 2. Sea Level Rise Projections
- Chart type: Multi-line time series plot
- Design decisions:
  - Solid lines (2050-2150): Represents actual IPCC data
  - Dashed lines (2150-2500): Clearly indicates extrapolated projections
  - Blue/red color scheme: Intuitive association with optimistic/pessimistic scenarios
  - Vertical separator line: Distinguishes IPCC data from extrapolations
  - Fill between lines: Shows uncertainty range
- Annotations: Key values labeled at 2100 and 2500 for reference points

### 3. Flooding Scenarios Mosaic
- Chart type: 3×3 grid of binary maps
- Color scheme:
  - Black: Remaining land
  - White: Ocean
  - Red: Land lost (draws attention to impact areas)
- Layout: Years as columns, scenarios as rows for easy comparison
- Information overlay: Sea level rise and land loss values in white boxes for readability

## Technical Challenges

### DEM Integer Value Limitation
- Problem: Integer elevation values in DEM create stepped data, causing binary land/water classification to show 0 km² loss for small sea level rises
- Solution: 
  - Extended projections to longer time periods (2300, 2500) to show meaningful differences
  - Added "Unknown" label for cases where calculated loss < 1 km² and SLR < 1m
  - Documented this limitation explicitly

## Reflection

### What Worked Well
- The layout of the 3 visualizations effectively tells the story from current state → projections → impacts
- Separate functions for each visualization enable easy iteration
- Distinguishing IPCC data from extrapolations maintains scientific rigor

### What Didn't Work Well
- This is not a dynamic flood model. It only identifies areas below projected sea levels
- Assumes no protective infrastructure improvements or policy responses
- Projections beyond 2150 don't account for potential acceleration or tipping points
- Integer values limit precision for small sea level rises

### What I Would Change With More Time
- Use a dataset with floating point elevation values for more nuanced analysis
- Add city locations and population data to contextualize impacts
- Incorporate subsidence and land uplift data for more accurate local projections
