import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

@st.cache_data
def generate_data():
    # Expanded locations with additional cities and rural areas
    locations = {
        'Houston': {'coords': (29.7604, -95.3698), 'population': 2300000},
        'Dallas': {'coords': (32.7767, -96.7970), 'population': 1340000},
        'Austin': {'coords': (30.2672, -97.7431), 'population': 964000},
        'San Antonio': {'coords': (29.4241, -98.4936), 'population': 1530000},
        'El Paso': {'coords': (31.7619, -106.4850), 'population': 682000},
        'Fort Worth': {'coords': (32.7555, -97.3308), 'population': 874000},
        'Amarillo': {'coords': (35.221997, -101.831297), 'population': 199000},
        'Corpus Christi': {'coords': (27.800583, -97.396381), 'population': 325000},
        'Lubbock': {'coords': (33.577863, -101.855166), 'population': 258000},
        'Laredo': {'coords': (27.503561, -99.507552), 'population': 261000},
        'Brownsville': {'coords': (25.901747, -97.497484), 'population': 182000},
        'McAllen': {'coords': (26.203407, -98.230012), 'population': 143000},
        'Waco': {'coords': (31.549333, -97.146670), 'population': 138000},
        'Odessa': {'coords': (31.845681, -102.367643), 'population': 123000},
        'Galveston': {'coords': (29.301348, -94.797696), 'population': 50000},
        'Tyler': {'coords': (32.351260, -95.301062), 'population': 106000},
        'Midland': {'coords': (31.997346, -102.077915), 'population': 146000},
        'Abilene': {'coords': (32.448736, -99.733144), 'population': 124000},
        'Beaumont': {'coords': (30.080174, -94.126556), 'population': 118000},
        'Killeen': {'coords': (31.117119, -97.727796), 'population': 145000},
        # New cities
        'Pasadena': {'coords': (29.691063, -95.209100), 'population': 153000},
        'Mesquite': {'coords': (32.766796, -96.599159), 'population': 143000},
        'McKinney': {'coords': (33.197246, -96.639782), 'population': 191000},
        'Frisco': {'coords': (33.150674, -96.823612), 'population': 200000},
        'Carrollton': {'coords': (32.975642, -96.889964), 'population': 135000},
        # Additional rural areas
        'Rural Area 10': {'coords': (26.956215, -99.101350), 'population': 20000},
        'Rural Area 11': {'coords': (28.707700, -100.531200), 'population': 19000},
        'Rural Area 12': {'coords': (34.962428, -101.931171), 'population': 15000},
        'Rural Area 13': {'coords': (31.422912, -103.493229), 'population': 17000},
        'Rural Area 14': {'coords': (33.577331, -98.618932), 'population': 18000},
        'Rural Area 15': {'coords': (27.506407, -99.507542), 'population': 16000},
        'Rural Area 16': {'coords': (30.045322, -99.140318), 'population': 14000},
        'Rural Area 17': {'coords': (29.209684, -99.786168), 'population': 15000},
        'Rural Area 18': {'coords': (28.036682, -97.509786), 'population': 13000},
        'Rural Area 19': {'coords': (32.738758, -97.431333), 'population': 12000},
    }

    data = []
    for city, info in locations.items():
        # Calculate cases as 10% of the population for cities
        cases = int(info['population'] * 0.10)
        for _ in range(cases):
            data.append([
                info['coords'][0] + np.random.normal(0, 0.03), # Cluster variance
                info['coords'][1] + np.random.normal(0, 0.03), # Cluster variance
                np.random.randint(1, 500)  # Elevation for visual variation
            ])

    return pd.DataFrame(data, columns=['Latitude', 'Longitude', 'Cases'])

df = generate_data()

st.title("Texas Alzheimer's Instances by County")

# Define the PyDeck chart as before
r = pdk.Deck(
    map_style=None,
    initial_view_state=pdk.ViewState(
        latitude=31.9686,
        longitude=-99.9018,
        zoom=5,
        pitch=50,
    ),
    layers=[
        pdk.Layer(
            "HexagonLayer",
            data=df,
            get_position="[Longitude, Latitude]",
            radius=2666,  # For denser grouping
            elevation_scale=112.5,  # Adjusted height scale
            elevation_range=[0, 1350],
            pickable=True,
            extruded=True,
        ),
    ],
)

st.pydeck_chart(r)

if st.button('Refresh Data'):
    st.legacy_caching.clear_cache()
    st.experimental_rerun()
