# Create your views here.
from django.shortcuts import render
from .interactive_plots import interactive_plot, add_points, generate_plot, clear_points, data_points
import numpy as np
import plotly.graph_objs as go  # Import for go.Scatter
from sklearn.linear_model import LinearRegression


def home(request):
    return render(request, "Home.html")


def contact(request):
    return render(request, "Contact.html")


def about(request):
    return render(request, "About me.html")


def work_in_progress(request):
    return render(request, "Work_in_progress.html")


def all_articles(request):
    return render(request, "All_articles.html")


def ig(request):
    return render(request, "Genetics/IG.html")


def bi(request):
    return render(request, "Bioinformatics/BI.html")


def ig_classical_genetics(request):
    return render(request, "Genetics/IG_classical_genetics.html")


def ml(request):
    return render(request, "Machine_learning/ML.html")


def ml_pattern_mining(request):
    return render(request, "Machine_learning/ML_Pattern_mining.html")


def st(request):
    return render(request, "Statistics/ST.html")





# Main view for linear regression, displaying both static and interactive plots
def st_linear_regression(request):
    if request.method == 'POST':
        if 'add_points' in request.POST:
            # Get comma-separated input from the form
            x_values = request.POST.get('x')
            y_values = request.POST.get('y')

            # Convert the comma-separated values to lists of floats
            x_list = [float(i) for i in x_values.split(',')]
            y_list = [float(i) for i in y_values.split(',')]

            # Add multiple points
            add_points(x_list, y_list)

        elif 'clear_points' in request.POST:
            clear_points()



    # For normal GET requests
    graph_html = interactive_plot(request)  # Dataset-based plot
    plot_div = generate_plot(data_points)  # User-modifiable plot

    return render(request, "Statistics/ST_Linear_regression.html", {
        'graph_html': graph_html,
        'plot_div': plot_div
    })


