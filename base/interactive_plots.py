import pandas as pd
from sklearn.linear_model import LinearRegression
import os
from django.conf import settings
import plotly.express as px
import numpy as np
import plotly.graph_objs as go  # Import for go.Scatter



# Construct the full file path relative to BASE_DIR
file_path = os.path.join(settings.BASE_DIR, 'base', 'Ecological_cleaned_data.txt')

# Load the file
df = pd.read_csv(file_path, delimiter='\t')


def interactive_plot(request):
    # Use the first 90 rows for both x and y, and hover data for the species
    x = df[['Body_Mass']].values  # Independent variable (first 90 rows)
    y = df['Max_Longevity'].values  # Dependent variable (first 90 rows)
    species = df['Species'].values  # Species names for hover data

    # Create a linear regression model
    model = LinearRegression()
    model.fit(x, y)  # Fit the model to the data

    # Predict y values based on the model
    y_pred = model.predict(x)

    # Get the slope (coefficient) and intercept
    slope = model.coef_[0]
    intercept = model.intercept_

    # Calculate the R-squared value to measure fit quality
    r_squared = model.score(x, y)

    # Create a Plotly scatter plot with the original data points, including species in hover data
    fig = px.scatter(
        x=x.flatten(),
        y=y,
        hover_data={'Species': species},  # Add species as hover data
        labels={'x': 'Body Mass', 'y': 'Max Longevity'},
        title='Linear Regression with Hover Info'
    )

    # Add the regression line (predicted values)
    fig.add_traces(px.line(x=x.flatten(), y=y_pred).data)

    fig.update_layout(
        width=1000,  # Adjust width (in pixels)
        height=600  # Adjust height (in pixels)
    )

    # Add annotations for slope, intercept, and R-squared
    # Add annotations outside the plot area by setting x and y to a value outside the plot range
    fig.add_annotation(xref="paper", yref="paper", x=1.12, y=1, text=f"Slope: {slope:.2f}", showarrow=False,
                       font=dict(size=12))
    fig.add_annotation(xref="paper", yref="paper", x=1.12, y=0.95, text=f"Intercept: {intercept:.2f}", showarrow=False,
                       font=dict(size=12))
    fig.add_annotation(xref="paper", yref="paper", x=1.12, y=0.90, text=f"R²: {r_squared:.2f}", showarrow=False,
                       font=dict(size=12))

    # Highlight the residuals (differences between actual points and predicted values)
    #for i in range(len(x)):
        #fig.add_shape(type="line",
                      #x0=x[i][0], y0=y[i],
                      #x1=x[i][0], y1=y_pred[i],
                      #line=dict(color="Red", width=1, dash="dash"))

    # Convert the plot to HTML
    graph_html = fig.to_html(full_html=False)

    # Return the graph HTML to be embedded in the template
    return graph_html


# Interactive user-modifiable plot data
data_points = []


# Function to add multiple points with limits on values and list length
def add_points(x_list, y_list):
    global data_points

    # Check if x_list and y_list have the same length
    if len(x_list) != len(y_list):
        raise ValueError("x_list and y_list must have the same number of elements")

    # Check the length of the lists
    if len(x_list) > 100 or len(y_list) > 100:
        raise ValueError("Please do not add more than 100 comma-separated values")

    # Check each value in x_list and y_list
    for i, j in zip(x_list, y_list):
        if i >= 1000 or j >= 1000:
            raise ValueError("Please do not add values larger than 1,000")
        if i >= 1000 or j >= 1000:
            raise ValueError("Please add numerical values")
    # Append each (x, y) pair to data_points if all checks pass
    for x, y in zip(x_list, y_list):
        data_points.append((x, y))


# Function to clear all points
def clear_points():
    global data_points
    data_points = []


# Generates plot based on user-modifiable data_points
def generate_plot(data_points):
    x_vals = np.array([point[0] for point in data_points]).reshape(-1, 1)
    y_vals = np.array([point[1] for point in data_points])

    if len(data_points) > 1:
        model = LinearRegression()
        model.fit(x_vals, y_vals)
        y_pred = model.predict(x_vals)
        slope, intercept = model.coef_[0], model.intercept_
    else:
        y_pred = y_vals
        slope, intercept = 0, 0

    scatter = go.Scatter(x=x_vals.flatten(), y=y_vals, mode='markers', name='Data Points')
    line = go.Scatter(x=x_vals.flatten(), y=y_pred, mode='lines',
                      name=f'Regression Line: y = {slope:.2f}x + {intercept:.2f}')
    layout = go.Layout(title="Interactive Linear Regression", xaxis=dict(title='X'), yaxis=dict(title='Y'))
    figure = go.Figure(data=[scatter, line], layout=layout)
    return figure.to_html(full_html=False)