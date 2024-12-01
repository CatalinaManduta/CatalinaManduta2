import numpy as np
from scipy.stats import mode
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
import plotly.io as pio


# Colors: standard blue: #15688a, dark red: #a53e44, green: #007147, orange: #ed982a
def numerical(input_string: str) -> list:
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


def calculate_descriptions(lis: list):
    """
    Calculate descriptive statistics and generate visualizations for a dataset.
    ----------
    Parameters:
    lis : list
        A list of numerical data (e.g., [1, 2, 3, 4, 5]).
    Returns:
    dict
        A dictionary containing HTML strings for various visualizations, including:
        - Histogram with mean, median, and mode
        - Box plot with interquartile range and outliers
        - Density plot with standard deviation markers
        - Spread metrics bar chart for variance, standard deviation, and range
    Raises:
        ValueError: If the input list is empty or contains invalid data.
    """
    # Calculations
    mean = np.mean(lis)
    median = np.median(lis)
    size = len(lis)
    mode_count = None

    q1 = np.percentile(lis, 25)  # 25th percentile (Q1)
    q3 = np.percentile(lis, 75)  # 75th percentile (Q3)
    iqr = q3 - q1  # Interquartile Range (IQR)

    # Handle mode calculation robustly
    mode_result = mode(lis) # When texting it locally use also keepdims=True
    mode_value = mode_result.mode[0] if mode_result.count[0] > 0 else None
    if mode_value is not None:
        mode_count = lis.count(mode_value)

    variance = np.var(lis)
    std_dev = np.std(lis)
    range_value = max(lis) - min(lis)

    # 1. Histogram with Mean, Median, Mode
    fig_histogram = go.Figure()  # initializes an empty figure object that you can add plots (traces) to
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
            name=f"Mode: {mode_value:.2f}"
        ))
    fig_histogram.update_layout(
        title="Histogram with Mean, Median, and Mode",
        xaxis_title="Data",
        yaxis_title="Frequency",
        template="plotly_white"
    )

    # 2. Box Plot
    fig_boxplot = go.Figure()  #  initializes an empty figure object that you can add plots (traces) to
    fig_boxplot.add_trace(go.Box(
        y=lis,  # The dataset to be visualized in the box plot.
        boxmean="sd",  # Includes the mean and standard deviation in the plot.
        marker=dict(color='#4486a1'),  # Specifies the color of the box plot.
        name="Box Plot"  # The label/name for the trace in the legend.
    ))
    fig_boxplot.update_layout(
        title="Box Plot",  # Sets the title of the plot.
        yaxis_title="Values",  # Labels the y-axis as "Values".
        template="plotly_white"  # Uses Plotly's white background theme for a clean look.
    )
    # Colors: standard blue: #15688a, dark red: #a53e44, green: #007147, orange: #ed982a

    # 3. Density Plot
    fig_density = ff.create_distplot(
        [lis], group_labels=["Data"], show_hist=False
    )

    # Add Standard Deviation Lines
    fig_density.add_trace(go.Scatter(
        x=[mean + std_dev, mean + std_dev],  # x-coordinates are the same for both points
        y=[0, max(fig_density.data[0].y)],  # By specifying y=[0, max(fig_density.data[0].y)], you ensure the line
        # starts at y=0 and ends at the maximum density value.
        mode="lines", line=dict(color="#007147", dash="dash"),
        name=f"+1 Std Dev: {mean + std_dev:.2f}"
    ))
    fig_density.add_trace(go.Scatter(
        x=[mean - std_dev, mean - std_dev],  # x-coordinates are the same for both points
        y=[0, max(fig_density.data[0].y)],
        mode="lines", line=dict(color="#ed982a", dash="dash"),
        name=f"-1 Std Dev: {mean - std_dev:.2f}"
    ))
    fig_density.add_trace(go.Scatter(
        x=[mean, mean],   # x-coordinates are the same for both points
        y=[0, max(fig_density.data[0].y)],
        mode="lines", line=dict(color="#a53e44", dash="solid"),
        name=f"Mean: {mean:.2f}"
    ))

    # Update Layout
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
        template="plotly_white",
        margin = dict(l=50, r=50, t=80, b=30)  # Adjust margins (left, right, top, bottom)
    )

    # Convert figures to HTML strings
    html_histogram = pio.to_html(fig_histogram, full_html=False)
    html_boxplot = pio.to_html(fig_boxplot, full_html=False)
    html_density = pio.to_html(fig_density, full_html=False)
    html_spread = pio.to_html(fig_spread, full_html=False)

    explanation_histo = f"""
                <p>This dataset contains <strong>{size}</strong> data points.</p>
                <ul>
                    <li>
                        <strong>Mean:</strong> The mean value is <strong>{mean:.2f}</strong>, which represents the average of the dataset.
                    </li>
                    <li>
                        <strong>Median:</strong> The median value is <strong>{median:.2f}</strong>. The median is the middle value when the data is sorted.
                        {'The median is larger than the mean, suggesting a left-skewed dataset.' if median > mean else 'The mean is larger than the median, suggesting a right-skewed dataset.'}
                    </li>
                    <li>
                        <strong>Mode:</strong> 
                        {'There is no mode in this dataset, indicating all values are unique.' if mode_value is None else f'The mode is <strong>{mode_value:.2f}</strong>, appearing <strong>{mode_count}</strong> times. This suggests {mode_value:.2f} is the most frequent or common value in the dataset.'}
                    </li>
                </ul>
            """

    explanation_boxplot = f"""
        <p>The box plot is a graphical representation of the dataset's distribution.</p>
        <ul>
            <li>
                <strong>Median:</strong> The horizontal line inside the box represents the median (<strong>{median:.2f}</strong>). This value divides the dataset into two equal halves.
            </li>
            <li>
                <strong>Interquartile Range (IQR):</strong> The box spans from the 25th percentile (Q1) to the 75th percentile (Q3), capturing the middle 50% of the data. 
                <ul>
                    <li>
                        <strong>Q1 (25th Percentile):</strong> The value below which 25% of the data points lie. In this dataset, Q1 is <strong>{q1:.2f}</strong>.
                    </li>
                    <li>
                        <strong>Q3 (75th Percentile):</strong> The value below which 75% of the data points lie. In this dataset, Q3 is <strong>{q3:.2f}</strong>.
                    </li>
                    <li>
                        <strong>IQR:</strong> The interquartile range is the difference between Q3 and Q1, calculated as <strong>{iqr:.2f}</strong>. It represents the spread of the central 50% of the data.
                    </li>
                </ul>
            </li>
            <li>
                <strong>Whiskers:</strong> The lines extending from the box (whiskers) represent the range of the data, excluding outliers. They indicate the minimum and maximum values within 1.5 times the IQR from Q1 and Q3, respectively.
            </li>
            <li>
                <strong>Outliers:</strong> Any points outside the whiskers are considered outliers, suggesting extreme values in the dataset. These values are represented as individual dots in the box plot.
            </li>
            <li>
                <strong>Mean and Standard Deviation:</strong> The box plot also includes a marker for the mean (<strong>{mean:.2f}</strong>) and a visual indication of the standard deviation.
            </li>
        </ul>
    """

    explanation_density = f"""
        <p>The density plot is a curve representing the distribution of the dataset. It provides insights into the shape of the data and its spread.</p>
        <ul>
            <li>
                <strong>Mean:</strong> The mean is <strong>{mean:.2f}</strong>, represented by the red solid line in the plot. It is the average value and indicates the central tendency.
            </li>
            <li>
                <strong>Standard Deviation:</strong> 
                <ul>
                    <li>
                        <strong>+1 Std Dev:</strong> The dashed green line shows one standard deviation above the mean (<strong>{mean + std_dev:.2f}</strong>). This indicates where most of the higher values are concentrated.
                    </li>
                    <li>
                        <strong>-1 Std Dev:</strong> The dashed orange line shows one standard deviation below the mean (<strong>{mean - std_dev:.2f}</strong>). This indicates where most of the lower values are concentrated.
                    </li>
                </ul>
                Together, these lines show the typical spread of the dataset, with most data falling within one standard deviation of the mean (between the orange and green dotted lines).
            </li>
            <li>
                <strong>Density Peaks:</strong> Overall the peaks in the curve represent areas where the data points are concentrated. A higher peak means more frequent values in that range.
            </li>
        </ul>
    """
    explanation_spread = f"""
        <p>The spread metrics bar chart provides insights into the variability of the dataset. It highlights three key measures that describe how data points are distributed around the center:</p>
        <ul>
            <li>
                <strong>Variance:</strong> The variance is <strong>{variance:.2f}</strong>. 
                Variance measures the average squared deviation of each data point from the mean. 
                A higher variance indicates that data points are more spread out, while a lower variance suggests they are closer to the mean.
                <br>
                <strong>Example Interpretation:</strong> In this dataset, a variance of <strong>{variance:.2f}</strong> 
                suggests that the data points deviate moderately/significantly from the mean on average.
            </li>
            <li>
                <strong>Standard Deviation:</strong> The standard deviation is <strong>{std_dev:.2f}</strong>.
                It is the square root of the variance and is expressed in the same units as the data, making it more intuitive to interpret.
                 A smaller standard deviation means the data points are closer to the mean, while a larger one indicates greater variability.
                <br>
                <strong>Example Interpretation:</strong> A standard deviation of <strong>{std_dev:.2f}</strong> indicates that most data points are typically within <strong>{std_dev:.2f}</strong> units of the mean.
            </li>
            <li>
                <strong>Range:</strong> The range is <strong>{range_value:.2f}</strong>.
                It is the difference between the maximum and minimum values in the dataset, showing the total spread.
                 <strong>The range is sensitive to outliers and provides a quick sense of the overall variability.</strong>
                <br>
                <strong>Example Interpretation:</strong> A range of <strong>{range_value:.2f}</strong> means the data 
                points span this entire interval from the smallest to the largest value.
            </li>
        </ul>
    """

    combined_histo = f"""
            <div>
                <div>  
                    {html_histogram}
                </div>
                <div>
                <h4>Results Summary</h4>
                    {explanation_histo}
                </div>
            </div>
        """

    combined_density = f"""
            <div>
                <div> 
                    {html_density}
                </div>
                <div>
                <h4>Results Summary</h4>
                    {explanation_density}
                </div>
            </div>
        """


    combined_boxplot = f"""
            <div>
                <div> 
                    {html_boxplot}
                </div>
                <div>
                <h4>Results Summary</h4>
                    {explanation_boxplot}
                </div>
            </div>
        """

    combined_spread = f"""
                <div>
                    <div> 
                        {html_spread}
                    </div>
                    <div>
                    <h4>Results Summary</h4>
                        {explanation_spread}
                    </div>
                </div>
            """
    return {
        "histogram": combined_histo,
        "boxplot": combined_boxplot,
        "density": combined_density,
        "spread": combined_spread
    }

def premade(distr: str) -> list:
    """
       Generate premade datasets for demonstrating different statistical distributions.
       ----------
       Parameters:
       distr : str
           A string specifying the desired distribution type. Options are:
           - "normal": Generates a dataset with a normal distribution.
           - "skewed": Generates a dataset with a right-skewed distribution.
           - "outliers": Generates a dataset with a normal distribution and added outliers.
       Returns:
       list
           A list of integers representing the generated dataset.
       Raises:
           ValueError: If the specified distribution type is not recognized.
       """
    if distr == "normal":
        # List with normal distribution
        np.random.seed(2)
        list1 = list(np.round(np.random.normal(50, 10, 800)).astype(int))
        return list1
    elif distr == "skewed":
        # List with skewed distribution (right skew)
        np.random.seed(3)
        list2 = list(np.round(np.random.exponential(20, 800)).astype(int))
        return list2
    else:
        # Outliers
        np.random.seed(1)
        list3 = list(np.round(np.random.normal(50, 10, 795)).astype(int))
        list3 = list3 + [150, 160, 170, 180, 190]
        return list3