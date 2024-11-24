import numpy as np
from scipy.stats import mode
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
import plotly.io as pio

# Colors: standard blue: #15688a, dark red: #a53e44, green: #007147, orange: #ed982a
def numerical(input_string):
    """
    Process numerical data from a comma-separated string.
    ----------
    Parameters:
    input_string : str
        Comma-separated string of numerical data (e.g., "1,2,3,4,5").
    Returns:
    list
        List of floats if input is valid.
    Raises:
        ValueError: If input contains non-numeric values or exceeds length limit.
    """
    try:
        # Split the string into a list of values
        lis = input_string.split(",")

        # Validate length
        if len(lis) > 1000:
            raise ValueError("The length of the list should not exceed 1000.")

        # Convert each value to float after stripping spaces
        lis = [float(i.strip()) for i in lis if i.strip()]

    except ValueError as e:
        # Handle conversion errors or invalid inputs
        return str(e)

    return lis


def categorical(lis):
    lis = lis.split(",")
    try:
        if len(lis) > 1000:
            raise ValueError("The lenght of the list should not exceed 1000.")

    except ValueError as e:
        return e
    lis = [i.strip() for i in lis if i.strip()]
    print("this is", lis)
    return lis


def choice(option, lis):
    if option == "numerical":
        return numerical(lis)
    else:
        return categorical(lis)


def calculate_descriptions(lis):
    # Calculations
    mean = np.mean(lis)
    median = np.median(lis)

    # Handle mode calculation robustly
    mode_result = mode(lis, keepdims=True)
    mode_value = mode_result.mode[0] if mode_result.count[0] > 0 else None

    variance = np.var(lis)
    std_dev = np.std(lis)
    range_value = max(lis) - min(lis)

    # 1. Histogram with Mean, Median, Mode
    fig_histogram = go.Figure()
    fig_histogram.add_trace(go.Histogram(
        x=lis,
        nbinsx=10,
        marker=dict(color="#4486a1"),
        name="Data"
    ))
    # Colors: standard blue: #15688a, dark red: #a53e44, green: #007147, orange: #ed982a

    fig_histogram.add_trace(go.Scatter(
        x=[mean, mean], y=[0, max(np.histogram(lis, bins=10)[0])],
        mode="lines", line=dict(color="#a53e44", dash="solid"),  # Options: "solid", "dot", "dash", "longdash", etc.
        # "lines", "markers", "lines+markers", "text"
        name=f"Mean: {mean:.2f}"
        # Example of np.histogram(lis, bins=3):
        #
        # Bin Ranges:
        # The range of the data (1 to 10) is divided into 3 equal intervals:
        #   Bin 1: [1.0, 4.0)  -> Includes values 1.0 up to (but not including) 4.0
        #   Bin 2: [4.0, 7.0)  -> Includes values 4.0 up to (but not including) 7.0
        #   Bin 3: [7.0, 10.0] -> Includes values 7.0 up to and including 10.0
        #
        # Example Data: [1, 2, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        #
        # Counts (frequencies in each bin):
        #   Bin 1: 4 values (1, 2, 2, 3)
        #   Bin 2: 3 values (4, 5, 6)
        #   Bin 3: 4 values (7, 8, 9, 10)
    ))
    fig_histogram.add_trace(go.Scatter(
        x=[median, median], y=[0, max(np.histogram(lis, bins=10)[0])],
        mode="lines", line=dict(color="#007147", dash="solid"),  # Options: "solid", "dot", "dash", "longdash", etc.
        name=f"Median: {median:.2f}"
    ))
    if mode_value is not None:
        fig_histogram.add_trace(go.Scatter(
            x=[mode_value, mode_value], y=[0, max(np.histogram(lis, bins=10)[0])],
            mode="lines", line=dict(color="#ed982a", dash="solid"),  # Options: "solid", "dot", "dash", "longdash", etc.
            name=f"Mode: {mode_value}"
        ))
    fig_histogram.update_layout(
        title="Histogram with Mean, Median, and Mode",
        xaxis_title="Data",
        yaxis_title="Frequency",
        template="plotly_white"
    )

    # 2. Box Plot
    fig_boxplot = go.Figure()
    fig_boxplot.add_trace(go.Box(
        y=lis,
        boxmean="sd",
        marker=dict(color='#4486a1'),
        name="Box Plot"
    ))
    fig_boxplot.update_layout(
        title="Box Plot",
        yaxis_title="Values",
        template="plotly_white"
    )
    # Colors: standard blue: #15688a, dark red: #a53e44, green: #007147, orange: #ed982a

    # 3. Density Plot
    fig_density = ff.create_distplot(
        [lis], group_labels=["Data"], show_hist=False
    )
    for trace in fig_density.data:
        fig_density.add_trace(trace)
    fig_density.add_trace(go.Scatter(
        x=[mean + std_dev, mean + std_dev],
        y=[0, max(fig_density.data[0].y)],
        mode="lines", line=dict(color="#007147", dash="dash"),
        name=f"+1 Std Dev: {mean + std_dev:.2f}"
    ))
    fig_density.add_trace(go.Scatter(
        x=[mean - std_dev, mean - std_dev],
        y=[0, max(fig_density.data[0].y)],
        mode="lines", line=dict(color="#a53e44", dash="dash"),
        name=f"-1 Std Dev: {mean - std_dev:.2f}"
    ))
    fig_density.update_layout(
        title="Density Plot with Standard Deviation",
        xaxis_title="Data",
        yaxis_title="Density",
        template="plotly_white"
    )

    # 4. Spread Metrics Bar Chart
    fig_spread = go.Figure()
    metrics = ["Variance", "Standard Deviation", "Range"]
    values = [variance, std_dev, range_value]
    fig_spread.add_trace(go.Bar(
        x=metrics,
        y=values,
        text=[f"{v:.2f}" for v in values],
        textposition='outside',
        marker=dict(color=['#15688a', '#a53e44', '#007147'])
    ))
    fig_spread.update_layout(
        title="Spread Metrics",
        xaxis_title="Metrics",
        yaxis_title="Values",
        template="plotly_white"
    )

    # Convert figures to HTML strings
    html_histogram = pio.to_html(fig_histogram, full_html=False)
    html_boxplot = pio.to_html(fig_boxplot, full_html=False)
    html_density = pio.to_html(fig_density, full_html=False)
    html_spread = pio.to_html(fig_spread, full_html=False)

    return {
        "histogram": html_histogram,
        "boxplot": html_boxplot,
        "density": html_density,
        "spread": html_spread
    }


from collections import Counter
import plotly.graph_objects as go


def mode_st(lis, plot=False):
    """
    Calculate and optionally plot the mode for a list of categorical or numerical data.

    Parameters:
    lis (list): The input data, either numeric or categorical.
    plot (bool): If True, generate a bar chart of the counts.

    Returns:
    dict or str: If plot=False, returns a dictionary with the mode and count.
                 If plot=True, returns an HTML string of the plot.
    """
    # Count occurrences of each value
    category_counts = Counter(lis)

    # Find the mode(s) and their count
    mode_value, mode_count = category_counts.most_common(1)[0]  # Get the most common item

    # If no plot is needed, return the mode
    if not plot:
        return {"mode": mode_value, "count": mode_count}

    # Create a bar chart for categorical data
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=list(category_counts.keys()),  # Categories
        y=list(category_counts.values()),  # Counts
        marker=dict(color='lightblue'),
        name="Category Counts"
    ))

    # Highlight the mode category in a different color
    fig.add_trace(go.Bar(
        x=[mode_value],
        y=[mode_count],
        marker=dict(color='orange'),
        name=f"Mode: {mode_value} ({mode_count} occurrences)"
    ))

    # Update layout
    fig.update_layout(
        title="Categorical Data Distribution",
        xaxis_title="Categories",
        yaxis_title="Counts",
        template="plotly_white",
        showlegend=False
    )

    # Return HTML for the plot
    return go.Figure.to_html(fig, full_html=False)
