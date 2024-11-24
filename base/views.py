# Create your views here.

import sys
import os

# Add project directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # This is needed so other packages are recognized
# __file__: This is a special variable in Python that holds the full path of the script being executed.
# Example: If you're running views.py from C:\Users\Catalina\Desktop\CatalinaManduta2\base\, then:
# __file__ = "C:\\Users\\Catalina\\Desktop\\CatalinaManduta2\\base\\views.py"

from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import Article

# Statistics folder
from my_statistics.p_value import visualize_flips, flips, probability, experiments, observed  # Import functions
from my_statistics.linear_reagression import interactive_plot, add_points, generate_plot, clear_points, data_points
from my_statistics.descriptive_statistics import numerical, categorical, calculate_descriptions, choice, mode_st



# General View #####


def home(request):
    articles = Article.objects.all().order_by('-created_at')[:3]  # Order by newest first
    return render(request, 'Home.html', {'articles': articles})


def contact(request):
    return render(request, "Contact.html")


def about(request):
    return render(request, "About me.html")


def work_in_progress(request):
    return render(request, "Work_in_progress.html")


def all_articles(request):
    return render(request, "All_articles.html")


# Statistics #####
def st(request):
    articles = Article.objects.filter(group='Statistics').order_by('order')  # Filter and order by the `order` field
    return render(request, "Statistics/ST.html", {'articles': articles})


def st_introduction_st(request):
    article = get_object_or_404(Article, title="Introduction to Statistics")
    return render(request, "Statistics/ST_Introduction_ST.html", {'article': article})


def st_descriptive_st(request):
    error_message = None
    plot_html = {}
    data_type = None  # To track the selected data type


    # Fetch the article object
    article = get_object_or_404(Article, title="Descriptive Statistics")

    if request.method == "POST":
        # Get the user input
        data_type = request.POST.get("data_type")  # Either "categorical" or "numerical"
        data_input = request.POST.get("data_input")  # Comma-separated values

        try:
            # Check the selected data type and validate
            if data_type == "numerical":
                # Convert to integers for numerical data
                num = choice("numerical", data_input)
                plot_html = calculate_descriptions(num)

            elif data_type == "categorical":
                choice("categorical", data_input)  # Validate categorical data
                plot_html = mode_st(data_input, plot=True)

            else:
                error_message = "Invalid data type selected. Please choose either categorical or numerical."

        except ValueError as e:
            error_message = str(e)

    # Render the page with the plot or an error message
    return render(
        request,
        "Statistics/ST_Descriptive_ST.html",
        {
            "article": article,
            "plot_html": plot_html,
            "error_message": error_message,
        }
    )


# Main view for linear regression, displaying both static and interactive plots
def st_linear_regression(request):
    error_message = None  # Initialize error message as None

    # Retrieve the "Linear Regression" article
    article = get_object_or_404(Article, title="Linear Regression")

    if request.method == 'POST':
        try:
            if 'add_points' in request.POST:
                # Get comma-separated input from the form
                x_values = request.POST.get('x')
                y_values = request.POST.get('y')

                # Convert the comma-separated values to lists of floats
                x_list = x_values.split(',')
                y_list = y_values.split(',')

                # Add multiple points
                add_points(x_list, y_list)

            elif 'clear_points' in request.POST:
                clear_points()
        except ValueError as e:
            error_message = str(e)  # Set error_message to the exception message

    # For normal GET requests or after handling POST
    graph_html = interactive_plot(request)  # Dataset-based plot
    plot_div = generate_plot(data_points)  # User-modifiable plot

    return render(request, "Statistics/ST_Linear_regression.html", {
        'graph_html': graph_html,
        'plot_div': plot_div,
        'error_message': error_message,  # Pass the error message to the template
        'article': article  # Pass the article data to the template

    })


def st_p_value(request):
    error_message = None  # Initialize error message
    plot_binominal = None  # Initialize plot as None

    # Retrieve the "P-Value" article
    article = get_object_or_404(Article, title="P-Value")

    if request.method == 'POST':
        # Handle the "Clear Plot" button
        if 'clear_plot' in request.POST:
            plot_binominal = None  # Clear the plot
            return render(request, "Statistics/ST_p_value.html", {
                'plot_binominal': plot_binominal,
                'error_message': error_message,
                'article': article,
            })

        try:
            # Retrieve and validate inputs
            exp = experiments(int(request.POST.get('experiments', 10)))  # Default to 10 if not provided
            f = flips(int(request.POST.get('flips', 10)))                # Default to 10 if not provided
            p = probability(float(request.POST.get('probability', 0.5)))  # Default to 0.5 if not provided
            obs = observed(int(request.POST.get('observed', 0)))         # Default to 0 if not provided


            # Generate plot
            plot_binominal = visualize_flips(f, p, exp, obs)

        except ValueError as e:
            error_message = str(e)  # Capture validation errors

    # Render template
    return render(request, "Statistics/ST_p_value.html", {
        'plot_binominal': plot_binominal,  # Pass the plot HTML to the template
        'error_message': error_message,  # Pass error messages to the template
        'article': article  # Pass the article to the template
    })



def st_cdf_pmf(request):
    error_message = None
    plot_binominal = None

    # Retrieve the "P-Value" article
    article = get_object_or_404(Article, title="P-Value")

    if request.method == 'POST':
        try:
            # Retrieve and validate inputs
            exp = experiments(int(request.POST.get('experiments', 10)))
            f = flips(int(request.POST.get('flips', 10)))
            p = probability(float(request.POST.get('probability', 0.5)))


            # Generate plot
            plot_binominal = visualize_flips(f, p, exp)
        except ValueError as e:
            error_message = str(e)

    return render(request, "Statistics/ST_p_value.html", {
        'plot_binominal': plot_binominal,
        'error_message': error_message,
        'article': article
    })


# Machine learning #####
def ml(request):
    articles = Article.objects.filter(group='Machine learning').order_by('-created_at')  # Filter and order by newest first
    return render(request, "Machine_learning/ML.html", {'articles': articles})


def ml_pattern_mining(request):
    article = get_object_or_404(Article, title="Frequent Pattern Mining")
    return render(request, "Machine_learning/ML_Pattern_mining.html", {'article': article})


def ml_clustering_basics(request):
    article = get_object_or_404(Article, title="Clustering - Basics")
    return render(request, "Machine_learning/ML_Clustering_basics.html", {'article': article})


#  Bioinformatics #####
def bi(request):
    articles = Article.objects.filter(group='Bioinformatics').order_by('-created_at')  # Filter and order by newest first
    return render(request, "Bioinformatics/BI.html", {'articles': articles})






def ig_classical_genetics(request):
    return render(request, "Genetics/IG_classical_genetics.html")


def ig(request):
    return render(request, "Genetics/IG.html")







