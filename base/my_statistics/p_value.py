import numpy as np
from scipy.stats import binom
import plotly.graph_objects as go
from plotly.io import to_html


def flips(flip: int) -> int:
    """
    Validate and return the number of flips to be run per experiment.
    ----------
    Parameters:
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
    ----------
    Parameters:
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


def observed(obs: int) -> int:
    """
    Validate and return the number of experiments to be run.
    ----------
    Parameters:
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
        if not isinstance(obs, int):
            raise ValueError("Input must be an integer.")
        if obs <= 1:
            raise ValueError("The number of flips must be greater than 0.")
        if obs > 150:
            raise ValueError("The number of flips must not exceed 150.")
        # If all conditions pass, return the value
        return obs
    except ValueError as e:
        raise e


def probability(prob: float) -> float:
    """
    Validate and return a probability value.
    ----------
    Parameters:
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
        ----------
        Parameters:
        f : int
            The number of trials (flips) in each experiment. Must be a positive integer.
        p : float
            The probability of success (e.g., probability of heads in a coin flip).
            Must be a number between 0 and 1 (inclusive).
        exp : int
            The number of experiments to simulate. Must be a positive integer.

        Returns:
        numpy.ndarray
            An array of integers, where each element represents the number of successes
            (e.g., heads) observed in each experiment.

        Raises:
        ValueError
            If `f` or `exp` are not positive integers.
            If `p` is not a float or not in the range [0, 1].

        Example:
         sample(f=10, p=0.5, exp=5)
        array([5, 6, 4, 7, 5])  # Number of successes in 5 experiments of 10 flips
        """
    samples = np.random.binomial(f, p, exp)
    return samples


def visualize_flips(f: int, p: float, exp: int, obs: int) -> str:
    """
    Visualize the distribution of outcomes from a binomial distribution and return the plot as an HTML div.
    ----------
    Parameters:
    f : int
        The number of trials (flips) in each experiment.
    p : float
        The probability of success (e.g., heads in a coin flip).
    exp : int
        The number of experiments to simulate.
    obs : int
        The observed number of successes to validate against the distribution.
    Returns:
    str
        The HTML representation of the plot with explanatory text.
    """
    # Validate inputs
    f = flips(f)
    p = probability(p)
    exp = experiments(exp)
    obs = observed(obs)

    # Generate sample data
    samples = sample(f, p, exp)

    # Count occurrences of each number of successes
    unique, counts = np.unique(samples, return_counts=True)
    pmf_values = counts / exp  # Normalize counts to represent probabilities

    # Calculate the PMF for the observed value
    pmf_obs = pmf_values[unique == obs][0] if obs in unique else 0

    # Generate textual explanation
    explanation = f"""
        <p>In {exp} experiments, each involving {f} flips with a probability of {p} for heads:</p>
        <ul>
            <li>The observed value of {obs} heads occurred with an approximate probability of {pmf_obs:.4f}.</li>
            <li>The distribution shows most outcomes are centered around {int(f * p)} successes, which is expected for a fair coin.</li>
            <li>{'This outcome is quite rare.' if pmf_obs < 0.05 else 'This outcome is common and aligns well with expectations.'}</li>
        </ul>
    """

    # Create the plot using Plotly
    fig = go.Figure()

    # Bar plot for PMF
    fig.add_trace(go.Bar(
        x=unique,
        y=pmf_values,
        name="PMF",
        marker=dict(color=['red' if u == obs else 'blue' for u in unique]),
        hovertemplate="Successes: %{x}<br>Probability: %{y:.4f}<extra></extra>"
    ))

    # Add layout details
    fig.update_layout(
        title=f"Binomial Distribution (flips={f}, p={p}, experiments={exp})",
        xaxis_title="Number of Successes (Heads)",
        yaxis_title="Probability",
        legend=dict(title="Legend"),
        template="plotly_white"
    )

    # Combine plot and explanation as HTML
    combined_html = f"""
        <div>
            <div>
                <h3>Results Summary</h3>
                {explanation}
            </div>
            <div>
                {to_html(fig, full_html=False)}
            </div>
        </div>
    """

    return combined_html




