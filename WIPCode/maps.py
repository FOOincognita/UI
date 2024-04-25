

def research():
    st.subheader("Drug Progress Bar")
    val = stx.stepper_bar(steps=["Phase 1", "Phase 2", "Phase 3", "Phase 4", "Phase 5"])

    # Example population categories (simplified for this example)
    population_categories = {
        'Houston': 'large',
        'San Antonio': 'large',
        'Dallas': 'large',
        'Austin': 'medium',
        'Fort Worth': 'medium',
        'Galveston': 'small',
        'College Station': 'small',
        'El Paso': 'medium',
        'Corpus Christi': 'small',
        'McAllen': 'small',
        'Lubbock': 'small',
    }

    # Coordinates for cities
    cities = {
        'Houston': (29.7604, -95.3698),
        'San Antonio': (29.4241, -98.4936),
        'Dallas': (32.7767, -96.7970),
        'Austin': (30.2672, -97.7431),
        'Fort Worth': (32.7555, -97.3308),
        'Galveston': (29.2998, -94.7946),
        'College Station': (30.6280, -96.3344),
        'El Paso': (31.7619, -106.4850),
        'Corpus Christi': (27.8006, -97.3964),
        'McAllen': (26.2034, -98.2300),
        'Lubbock': (33.5779, -101.8552),
    }

    # Dropdown for city zoom
    selected_city = st.selectbox("Select a city to zoom in:", options=["View All"] + list(cities.keys()))

    # Generate data points considering population size
    all_city_data = pd.DataFrame(columns=['lat', 'lon'])
    for city, coords in cities.items():
        population_size = population_categories[city]
        base_density = 100  # base number of data points
        if population_size == 'small':
            num_points = base_density
        elif population_size == 'medium':
            num_points = base_density * 2
        elif population_size == 'large':
            num_points = base_density * 3

        data_points = np.random.randn(num_points, 2) / [10, 10] + coords
        city_data = pd.DataFrame(data_points, columns=['lat', 'lon'])
        all_city_data = pd.concat([all_city_data, city_data], ignore_index=True)

    # Determine initial view state
    if selected_city == "View All":
        view_state = pdk.ViewState(latitude=31.9686, longitude=-99.9018, zoom=5, pitch=50)
    else:
        city_lat, city_lon = cities[selected_city]
        view_state = pdk.ViewState(latitude=city_lat, longitude=city_lon, zoom=11, pitch=50)

    # Pydeck map
    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/dark-v10',
        initial_view_state=view_state,
        layers=[
            pdk.Layer(
                'HexagonLayer',
                data=all_city_data,
                get_position='[lon, lat]',
                radius=2000,
                elevation_scale=100,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
                get_color="[255 * (1 - elevationValue / maxElevation), 255 * (elevationValue / maxElevation), 0, 160]",
                auto_highlight=True,
            ),
        ],
    ))