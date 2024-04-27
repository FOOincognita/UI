import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.figure_factory as ff

def financial():

    # Set the random seed for reproducibility
    np.random.seed(0)

    # Generate synthetic data over a much longer period
    dates = pd.date_range(start='2008-01-01', end='2023-12-31', freq='M')
    prices = np.random.normal(loc=0, scale=10, size=len(dates)).cumsum() + 100
    sales = np.random.poisson(lam=200, size=len(dates)).cumsum() + np.random.normal(loc=0, scale=1000, size=len(dates)).cumsum()

    data = pd.DataFrame({
        'Date': dates,
        'Price': prices,
        'Sales Volume': sales,
        'Market Share Oxiracetam': np.random.normal(loc=20, scale=5, size=len(dates)),
        'Market Share Other Drugs': np.random.normal(loc=50, scale=15, size=len(dates)),
        'Profit Margins': np.random.normal(loc=30, scale=5, size=len(dates))
    })

    # Set Date as the index
    data.set_index('Date', inplace=True)

    # Displaying the app layout
    st.title("Financial Data Analysis for Oxiracetam")

    # Create a 2x2 grid for the interactive graphs
    col1, col2 = st.columns(2)

    # Plotting Price Trends Over Time using Plotly
    with col1:
        fig = px.line(data.reset_index(), x='Date', y='Price', title='Price Trends of Oxiracetam', template="streamlit")
        st.plotly_chart(fig, use_container_width=True)

    # Distribution plot for financial analysis
    with col2:
        # Add histogram data
        x1 = np.random.randn(200) - 2  # Representing low growth
        x2 = np.random.randn(200)      # Representing average growth
        x3 = np.random.randn(200) + 2  # Representing high growth

        # Group data together
        hist_data = [x1, x2, x3]
        group_labels = ['Low', 'Avg', 'High']  # Labels for financial context

        # Create distplot with custom bin_size
        fig = ff.create_distplot(
                hist_data, group_labels, bin_size=[.1, .25, .5])
        fig.update_layout(
            title='Distribution of Sales Growth Rates',
            showlegend=False,
            hoverlabel=dict(
                bgcolor='red',  # Dark background for the hover label
                font_color='black',  # White text for contrast
                bordercolor='purple'  # Gray border can help the label stand out
            )
        )
        st.plotly_chart(fig, use_container_width=True)



    # Plotting Market Share Compared to Other Medications
    with col1:
        st.write("Market Share Comparison")
        market_share_data = data[['Market Share Oxiracetam', 'Market Share Other Drugs']]
        st.line_chart(market_share_data)

    # Plotting Profit Margins
    with col2:
        st.write("Profit Margins")
        st.area_chart(data['Profit Margins'])
