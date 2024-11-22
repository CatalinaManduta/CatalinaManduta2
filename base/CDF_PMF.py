import numpy as np
from scipy.stats import binom
import plotly.graph_objects as go
from plotly.io import to_html


def flips(flip: int) -> int:
    """
    Validate and return the number of flips to be run per experiment.

    Parameters:
    ----------
    flips : int
        The number of flips to run per each experiment. Must be a positive integer
        between 1 and 150 (inclusive).

    Returns:
    int: the validated number of flips.

    Raises:
    ValueError
        If `flip` is not an integer.
        If `flip` is less than 1 or greater than 150.
    """
    try:
        # Check if the input is an integer
        if not isinstance(flip, int):
            raise ValueError("Input must be an integer.")

        # Check if the input is greater than 0
        if flip <= 0:
            raise ValueError("The number of flips must be greater than 0.")

        # Check if the input is less than or equal to 150
        if flip > 150:
            raise ValueError("The number of flips must not exceed 150.")

        # If all conditions pass, return the value
        return flip

    except ValueError as e:
        # Re-raise the specific error
        raise e


def experiments(experiment: int) -> int:
    """
    Validate and return the number of experiments to be run.

    Parameters:
    ----------
    experiment : int
        The number of experiments to run. Must be a positive integer
        between 1 and 150 (inclusive).

    Returns:
    int
        the validated number of experiments.

    Raises:
    ValueError
        If `experiment` is not an integer.
        If `experiment` is less than 1 or greater than 150.
    """
    try:
        if not isinstance(experiment, int):
            raise ValueError("Input must be an integer.")
        if experiment <= 1:
            raise ValueError("The number of flips must be greater than 0.")
        if experiment > 150:
            raise ValueError("The number of flips must not exceed 150.")
        # If all conditions pass, return the value
        return experiment
    except ValueError as e:
        raise e


def probability(prob: float) -> float:
    """
    Validate and return a probability value.

    Parameters:
    ----------

    prob : float
        A number (int or float) representing the probability.
        Must be between 0 and 1 (inclusive).

    Returns:
    float
        The validated probability value as a float.

    Raises:
    ValueError
        If `prob` is not a number (int or float).
        If `prob` is not in the range [0, 1].
    """
    if not isinstance(prob, (int, float)):
        raise ValueError("Input must be a number.")
    if not 0 <= prob <= 1:
        raise ValueError("The number should be between 0 and 1.")
    return float(prob)


def sample(f: int, p: float, exp: int):
    """
        Generate a sample of outcomes based on a binomial distribution.

        Parameters:
        ----------
        f : int
            The number of trials (flips) in each experiment. Must be a positive integer.
        p : float
            The probability of success (e.g., probability of heads in a coin flip).
            Must be a number between 0 and 1 (inclusive).
        exp : int
            The number of experiments to simulate. Must be a positive integer.

        Returns:
        -------
        numpy.ndarray
            An array of integers, where each element represents the number of successes
            (e.g., heads) observed in each experiment.

        Raises:
        ------
        ValueError
            If `f` or `exp` are not positive integers.
            If `p` is not a float or not in the range [0, 1].

        Example:
        -------
         sample(f=10, p=0.5, exp=5)
        array([5, 6, 4, 7, 5])  # Number of successes in 5 experiments of 10 flips
        """
    samples = np.random.binomial(f, p, exp)
    return samples


def visualize_flips(f: int, p: float, exp: int) -> str:
    """
    Visualize the distribution of outcomes from a binomial distribution, highlight tail areas,
    and display the p-value based on observed data.

    Parameters:
    ----------
    f : int
        The number of trials (flips) in each experiment.
    p : float
        The probability of success (e.g., heads in a coin flip).
    exp : int
        The number of experiments to simulate.

    Returns:
    -------
    str
        The HTML representation of the plot to be rendered in the template.

    Raises:
    ------
    ValueError
        If input values do not meet validation criteria.
    """
    # Validate inputs
    f = flips(f)
    p = probability(p)
    exp = experiments(exp)

    # Generate sample data
    samples = sample(f, p, exp)

    # Determine k_observed (e.g., use the mean or a random sample as "observed" value)
    k_observed = int(np.mean(samples))  # Example: mean of samples

    # Count occurrences of each number of successes
    unique, counts = np.unique(samples, return_counts=True)

    # Calculate PMF and CDF
    pmf = binom.pmf(unique, f, p)
    cdf = binom.cdf(unique, f, p)

    # Calculate p-value for the observed number of successes (two-tailed test)
    left_tail = binom.cdf(k_observed, f, p)  # P(X <= k_observed)
    right_tail = 1 - binom.cdf(k_observed - 1, f, p)  # P(X >= k_observed)
    p_value = left_tail + right_tail

    # Highlight tail areas in the PMF
    tail_colors = ["red" if (x <= k_observed or x >= f - k_observed) else "blue" for x in unique]

    # Create the plot using Plotly
    fig = go.Figure()

    # Add PMF as a bar plot
    fig.add_trace(go.Bar(
        x=unique,
        y=pmf,
        name="PMF",
        marker=dict(color=tail_colors, opacity=0.7),
        hovertemplate="Successes: %{x}<br>PMF: %{y:.3f}<extra></extra>"
    ))

    # Add CDF as a step plot
    fig.add_trace(go.Scatter(
        x=unique,
        y=cdf,
        mode="lines+markers",
        name="CDF",
        line=dict(color="green"),
        hovertemplate="Successes: %{x}<br>CDF: %{y:.3f}<extra></extra>"
    ))

    # Add p-value annotation
    fig.add_annotation(
        x=k_observed,
        y=0,
        text=f"P-value: {p_value:.4f}",
        showarrow=True,
        arrowhead=2,
        ax=0,
        ay=-40,
        font=dict(color="red", size=12),
        align="center"
    )

    # Update layout details
    fig.update_layout(
        title=f"Binomial Distribution (flips={f}, p={p}, experiments={exp})",
        xaxis_title="Number of Successes (Heads)",
        yaxis_title="Probability",
        legend=dict(title="Legend"),
        template="plotly_white"
    )

    # Return the plot as an HTML div
    return to_html(fig, full_html=False)


