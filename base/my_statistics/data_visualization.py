import pandas as pd
import os
from django.conf import settings
import plotly.express as px
import numpy as np
import plotly.graph_objs as go  # Import for go.Scatter
import statsmodels.api as sm  # Import statsmodels for additional statistics


# Step 1: Create a fictional dataset
def generate_fertilizer_growth_data():
    data = {
        'Day': [20, 40, 60, 70] * 4,  # Days repeated for each fertilizer
        'Fertilizer': ['Fertilizer A'] * 4 + ['Fertilizer B'] * 4 + ['Fertilizer C'] * 4 + ['Fertilizer D'] * 4,
        'Plant_Height_cm': [
            10, 15, 20, 25,  # Growth for Fertilizer A
            12, 20, 30, 35,  # Growth for Fertilizer B
            8, 18, 35, 45,   # Growth for Fertilizer C
            5, 12, 20, 30    # Growth for Fertilizer D
        ]
    }
    return pd.DataFrame(data)


# Step 2: Create a bar plot using the fictional dataset
def bar_plot():
    # Generate the dataset
    data = generate_fertilizer_growth_data()
    data = data.groupby('Fertilizer')  # creates a GroupBy object, not a Dataset
    avg_growth = data['Plant_Height_cm'].mean()
    avg_growth = avg_growth.reset_index()  #  converts the Series into a DataFrame with Fertilizer as a column and
    # Plant_Height_cm as another column. This is essential because px.bar() needs a DataFrame with clear x and y mappings.

    # Create a bar plot using Plotly Express
    fig = px.bar(
        avg_growth,
        x='Fertilizer',  # Fertilizers on the x-axis
        y='Plant_Height_cm',  # Final plant growth on the y-axis
        color='Fertilizer',  # Color bars by Fertilizer
        title='Effect of Fertilizers on Plant Growth',
        labels={
            'Plant_Height_cm': 'Average Plant Height (cm)',
            'Fertilizer': 'Fertilizer Type',
        },
        barmode='group',  # Bars for each fertilizer grouped together
        color_discrete_map = {
        'Fertilizer A': '#15688a',  # Standard blue
        'Fertilizer B': '#a53e44',  # Dark red
        'Fertilizer C': '#007147',  # Green
        'Fertilizer D': '#ed982a'  # Orange
    }
    )

    # Show the plot
    return fig.to_html(full_html=False)

def filled_plot():
    data = generate_fertilizer_growth_data()

    fig = px.area(data, x='Day',
                  y='Plant_Height_cm',
                  color='Fertilizer',
                  title='Effect of Fertilizers on Plant Growth',
                  labels={
                      'Plant_Height_cm': 'Plant Height (cm)',
                      'Fertilizer': 'Fertilizer Type',
                      "Day": "Days"
                  },
                  color_discrete_map={
                      'Fertilizer A': '#15688a',  # Standard blue
                      'Fertilizer B': '#a53e44',  # Dark red
                      'Fertilizer C': '#007147',  # Green
                      'Fertilizer D': '#ed982a'  # Orange
                  }
                  )
    return fig.to_html(full_html=False)



