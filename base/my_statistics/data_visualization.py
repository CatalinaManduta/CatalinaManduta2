import pandas as pd
import os
from django.conf import settings
import plotly.express as px
import numpy as np
import plotly.graph_objs as go  # Import for go.Scatter
import statsmodels.api as sm  # Import statsmodels for additional statistics


# Step 1: Create a fictional dataset
def generate_fertilizer(data_type: str):
    if data_type == "small":
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
    else:
        np.random.seed(42)  # For reproducibility
        data = {
            'Fertilizer': ['Fertilizer A'] * 50 + ['Fertilizer B'] * 50 + ['Fertilizer C'] * 50,
            'Plant_Height_cm': (
                    list(np.random.normal(15, 5, 50)) +  # Fertilizer A: Mean=15, Std=5
                    list(np.random.normal(25, 7, 50)) +  # Fertilizer B: Mean=25, Std=7
                    list(np.random.normal(35, 10, 50))  # Fertilizer C: Mean=35, Std=10
            )
        }
        return pd.DataFrame(data)



# Step 2: Create a bar plot using the fictional dataset
def bar_plot2():
    # Generate the dataset
    data = generate_fertilizer("small")
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
    fig.update_layout(
        bargap=0.3  # Reduce gap between bars (default is 0.2)
    )

    # Show the plot
    return fig.to_html(full_html=False)


def bar_plot():
    data=generate_fertilizer("small")
    data = data.groupby('Fertilizer')  # creates a GroupBy object, not a Dataset
    avg_growth = data['Plant_Height_cm'].mean()
    avg_growth = avg_growth.reset_index()  # converts the Series into a DataFrame with Fertilizer as a column and
    # Plant_Height_cm as another column. This is essential because px.bar() needs a DataFrame with clear x and y mappings.
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=avg_growth['Fertilizer'],
        y=avg_growth['Plant_Height_cm'],
        name='Plant Growth',  # Legend name
        marker_color=['#15688a', '#a53e44', '#007147', '#ed982a'],  # Custom colors
        width=0.5  # Custom bar width
    ))
    fig.update_layout(
        title='Effect of Fertilizers on Plant Growth',
        xaxis_title='Fertilizer Type',
        yaxis_title='Average Plant Height (cm)',
        bargap=0.2  # Gap between groups of bars
    )
    return fig.to_html(full_html=False)

def filled_plot():
    data = generate_fertilizer("small")

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





# Create the histogram
def histogram_plot():
    data = generate_fertilizer("large")
    fig = px.histogram(
        data,
        x='Plant_Height_cm',  # The continuous variable
        color='Fertilizer',  # Separate distributions by fertilizer
        title='Distribution of Plant Heights by Fertilizer',
        labels={'Plant_Height_cm': 'Plant Height (cm)', 'Fertilizer': 'Fertilizer Type'},
        nbins=6,  # Number of bins
        opacity=0.7  # Transparency for overlapping histograms
    )
    return fig.to_html(full_html=False)


def box_plot():
    data = generate_fertilizer("large")
    fig = go.Figure()
    fig.add_trace(go.Box(
        x=data['Fertilizer'],
        y=data['Plant_Height_cm'],
        name='Plant Growth',  # Legend name
    ))
    fig.update_layout(
        title='Effect of Fertilizers on Plant Growth',
        xaxis_title='Fertilizer Type',
        yaxis_title='Average Plant Height (cm)',
    )
    return fig.to_html(full_html=False)

#box_plot()

def violin():
    # Generate the dataset
    data = generate_fertilizer("large")

    # Define fertilizers
    fertilizers = ['Fertilizer A', 'Fertilizer B', 'Fertilizer C']

    # Create a violin plot
    fig = go.Figure()

    for fert in fertilizers:
        fig.add_trace(go.Violin(
            x=data['Fertilizer'][data['Fertilizer'] == fert],  # Filter Fertilizer column
            y=data['Plant_Height_cm'][data['Fertilizer'] == fert],  # Filter Plant_Height_cm for this fertilizer
            name=fert,  # Legend name
            box_visible=True,  # Show the inner box plot
            meanline_visible=True  # Show the mean line
        ))

    # Update layout
    fig.update_layout(
        title='Plant Growth Distribution by Fertilizer',
        xaxis_title='Fertilizer Type',
        yaxis_title='Plant Height (cm)'
    )

    # Show the plot
    return fig.to_html(full_html=False)


