import plotly.express as px
import numpy as np
from sklearn.linear_model import LinearRegression


def interactive_plot(request):
    # Data for the plot (Level of Sunlight and Plant Height)
    x = np.array([1, 3, 4, 12, 10, 3, 5]).reshape(-1, 1)  # Reshape for sklearn
    y = np.array([1.5, 3.0, 4.5, 6.0, 7.5, 9.0, 10.5])

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

    # Create a Plotly scatter plot with the original data points
    fig = px.scatter(x=x.flatten(), y=y, labels={'x': 'Level of Sunlight', 'y': 'Plant Height'},
                     title='Linear Regression Example')

    # Add the regression line (predicted values)
    fig.add_traces(px.line(x=x.flatten(), y=y_pred).data)

    # Add annotations for slope, intercept, and R-squared
    fig.add_annotation(x=1, y=10, text=f"Slope: {slope:.2f}", showarrow=False, font=dict(size=12))
    fig.add_annotation(x=1, y=9, text=f"Intercept: {intercept:.2f}", showarrow=False, font=dict(size=12))
    fig.add_annotation(x=1, y=8, text=f"R²: {r_squared:.2f}", showarrow=False, font=dict(size=12))

    # Add equation of the line in y = mx + b format
    fig.add_annotation(x=1, y=7, text=f"Equation: y = {slope:.2f}x + {intercept:.2f}", showarrow=False,
                       font=dict(size=12))

    # Highlight the residuals (differences between actual points and predicted values)
    for i in range(len(x)):
        fig.add_shape(type="line",
                      x0=x[i][0], y0=y[i],
                      x1=x[i][0], y1=y_pred[i],
                      line=dict(color="Red", width=1, dash="dash"))

    # Convert the plot to HTML
    graph_html = fig.to_html(full_html=False)

    # Return the graph HTML to be embedded in the template
    return graph_html
