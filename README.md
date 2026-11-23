# Mapping the Global Diffusion of K-Pop: A Geospatial Analysis of Stray Kids' International Audience
This project investigates the global spread of K-pop through a geospatial analysis of Stray Kids' international audience. Using Python, web APIs, demographic datasets, and GIS techniques, the project explores how the group's popularity has expanded from South Korea into established and emerging markets across the world.

The workflow combines data collection, data engineering, statistical analysis, spatial analysis, and cartographic design to produce a series of publication-quality maps and analytical outputs.

# Research Question:

**How has K-pop diffused globally from South Korea, and where are Stray Kids' strongest international audiences when adjusted for population?**

## Objectives

- Retrieve artist and track information from Spotify.
- Gather audience statistics from public music data sources.
- Combine music data with demographic and geographic datasets.
- Calculate population-normalised listener metrics.
- Analyse spatial clustering of K-pop popularity.
- Create professional cartographic outputs.
- Build a reproducible Python-based GIS workflow.

---

## Data Sources

### Music Data

- <s>Spotify Web API</s> - now requires premium features so being changed to
- Last.fm API

### Demographic Data

- World Bank Population Data

### Geographic Data

- Natural Earth Admin 0 Countries

---

## Proposed Methodology

### 1. Data Collection

Python scripts retrieve:

- Artist metadata
- Top tracks
- Popularity metrics
- Listener statistics by country

### 2. Data Processing

Data is cleaned, validated and standardised using:

- Pandas
- NumPy

### 3. Geographic Integration

Country-level listener statistics are joined to global administrative boundaries using:

- GeoPandas
- Shapely

### 4. Spatial Analysis

The project calculates:

- Listeners per million population
- Country rankings
- Spatial clustering statistics
- Hotspot patterns

### 5. Cartographic Production

Outputs are produced using:

- Matplotlib
- GeoPandas
- MapClassify

---

## Repository Structure

```text
stray-kids-kpop-analysis/

├── data/
│   ├── raw/
│       ├── stray_kids_artist_info.csv
│       ├── stray_kids_top_tracks.csv
│       ├── world_bank_population.csv
│   ├── processed/
│       ├── stray_kids_country_stats.csv
│   └── boundaries/
│
├── docs/
├── figures/
│   ├── maps
│       ├── draft
│           ├── stray_kids_market_strength_world_01.png
│       ├── final
│           ├── stray_kids_market_strength_world.png
│
├── scripts/
│   ├── 00_archive
│       ├── 01_spotify_data.py
│       ├── test_spotify_connection.py
│   ├── 00a_test
│       ├── test_korea.py
│       ├── test_lastfm_connection.py
│       ├── test_boundaries.py
│       ├── test_join_boundaries.py
│       ├── check_missing_country.py
│   ├── 01_lastfm_artist_data.py
│   ├── 02_lastfm_top_tracks.py
│   ├── 03_lastfm_country_stats.py
│   ├── 03a_get_population_data.py
│   ├── 04_world_chloropleth_map.py
│   └── 05_diffusion_flow_map.py
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

## Planned Outputs

### Map 1: Global Listener Distribution

Country-level choropleth showing estimated Stray Kids listener density.

    Natural Earth Countries
        +
    Stray Kids Market Strength
        ↓
    GeoPandas Join
        ↓
    Choropleth
        ↓
    PNG Export

### Map 2: Population-Normalised Popularity

Listeners per million population.

### Map 3: K-Pop Diffusion Flow Map

Flow lines originating from Seoul, South Korea and connecting to major listener markets.

### Map 4: Global K-Pop Hotspots

Spatial clustering of audiences using statistical measures.

### Charts

- Top songs
- Top listener countries
- Popularity trends

---

## Software and Libraries

- Python
- Pandas
- GeoPandas
- Matplotlib
- Seaborn
- Spotipy
- Requests
- Shapely
- PySAL
- ESDA

---

## Future Development

Potential extensions include:

- Temporal analysis of K-pop growth by album release.
- Fan audience comparisons between multiple K-pop groups.
- Interactive web mapping using Folium or Kepler.gl.
- Dashboard development with Plotly Dash.

---

## Data Limitations

The results presented in this project should be interpreted with several important limitations in mind.

### Audience Data Availability

Spotify does not provide publicly accessible listener counts or audience geography through its Web API. As a result, audience statistics are obtained from alternative public sources such as Last.fm, which may reflect platform-specific listening behaviour rather than the complete global audience of Stray Kids.

### Representation Bias

Listener data is derived from users who actively use and interact with the source platforms. This may underrepresent audiences in regions where Spotify or Last.fm adoption is lower and overrepresent regions with higher platform usage.

### Temporal Variability

Music popularity changes over time due to factors such as album releases, world tours, media appearances, and viral social media trends. The analysis represents a snapshot of audience activity at the time of data collection and may not reflect future listening patterns.

### Population Normalisation Assumptions

Population-adjusted metrics are used to facilitate comparison between countries of different sizes. While this improves comparability, it assumes listener distribution is proportional across the national population and does not account for variations in internet access, streaming adoption, age structure, or cultural preferences.

### Country-Level Aggregation

The analysis is conducted at national scale due to data availability constraints. Significant regional, metropolitan, and local variations within countries cannot be identified using the available datasets.

### Artist Selection

Stray Kids are used as a case study to examine the international diffusion of K-pop. Findings should not be interpreted as representative of all K-pop artists, groups, or genres, as audience distributions may vary substantially between performers.

### Data Matching and Geographic Boundaries

Country names obtained from music APIs may differ from those used within administrative boundary datasets. Data cleaning and standardisation procedures are applied to minimise inconsistencies; however, some discrepancies may remain.

### Interpretation of Diffusion

The project uses current audience geography as an indicator of K-pop's global reach. While spatial patterns can suggest cultural diffusion processes, they should not be interpreted as direct evidence of how, when, or why K-pop spread into individual markets without additional historical and qualitative analysis.

---

# Issues that came up

1. Spotify API is now only for paid subscribers even for the Developer API usage therefore changed over to lastfm who still allow data extraction for all with a valid account.

2. During the getting of artist data from the lastfm API it was needed to find how South Korea was being recorded therefore a test_korea.py script was added to find if this was 'South Korea', 'Republic of Korea' or 'Korea, Republic of' in their data. Originally started with 'South Korea' within scripting but returned 'NaN' therefore had to create this to find the error. 

3. Only 12 countries found instead of 13 as France didn't join within the test_join_boundaries.py script. Therefore created a check_missing_countries.py script to find this out as it was unable to find from "ISO_A3" code 'FRA' as it is in data as '-99'. Change of join to "ADMO_A3".

---

## Installation

```bash
python -m venv venv

source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Author

Sian Lake

GIS Analyst

This project was developed to demonstrate skills in GIS, spatial data science, Python automation, cartographic design, and geospatial analytics.
