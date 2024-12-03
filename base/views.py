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
from django.shortcuts import render, redirect
from .models import Article
from .forms import ContactForm
from django.core.paginator import Paginator


# Statistics folder
from my_statistics.p_value import visualize_flips, flips, probability, experiments, observed  # Import functions
from my_statistics.linear_reagression import interactive_plot, add_points, generate_plot, clear_points, data_points
from my_statistics.descriptive_statistics import numerical, calculate_descriptions, premade


# General View #####


def home(request):
    articles = Article.objects.all().order_by('-created_at')[:3]  # Order by newest first
    return render(request, 'Home.html', {'articles': articles})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # Save data to the database
            return redirect('contact_success')  # Redirect to success page
    else:
        form = ContactForm()

    return render(request, 'Contact.html', {'form': form})


def contact_success_view(request):
    articles = Article.objects.all().order_by('-created_at')[:4]  # Order by newest first
    return render(request, 'Contact_success.html', {'articles': articles})


    # html_directory = os.path.join('templates')  # Adjust the directory as needed
    # html_directory = '/home/CatalinaM/CatalinaManduta/templates'


def search_html_files(request):
    search_query = request.GET.get('q', '').lower()  # Get search query from the request
    results = []  # To store search results
    # html_directory = os.path.join('templates')  # Adjust the directory as needed
    html_directory = '/home/CatalinaM/CatalinaManduta/templates'

    # Loop through all HTML files in the directory
    for root, dirs, files in os.walk(html_directory):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()  # Read file content without converting to lowercase
                        if search_query in content.lower():  # Convert content to lowercase only for the search
                            # Debug: Verify if the search query is found
                            print(f"Search query '{search_query}' found in file: {file}")

                            # Extract title
                            title_start = content.find('<meta name="title" content="')
                            if title_start != -1:
                                title_start += len('<meta name="title" content="')
                                title_end = content.find('"', title_start)
                                if title_end != -1:
                                    title = content[title_start:title_end].strip()
                                else:
                                    title = "No title found"
                            else:
                                title = "No title found"
                            print(f"Extracted title: {title}")  # Debug

                            # Extract URL
                            url_start = content.find('<meta name="url" content="')
                            if url_start != -1:
                                url_start += len('<meta name="url" content="')
                                url_end = content.find('"', url_start)
                                if url_end != -1:
                                    url = content[url_start:url_end].strip()
                                else:
                                    url = "#"
                            else:
                                url = "#"
                            print(f"Extracted URL: {url}")  # Debug

                            # Add to results
                            if title != "No title found" and url != "#":  # Exclude results with no title or URL
                                results.append({'title': title, 'url': url})
                except Exception as e:
                    print(f"Error reading file {file_path}: {e}")
    print(f"Final results: {results}")
    return render(request, 'Search_results.html', {'results': results, 'query': search_query})


def get_excerpt(content, query, char_limit=100):
    """Helper function to get a snippet around the search query."""
    index = content.find(query)
    if index != -1:
        start = max(index - char_limit // 2, 0)
        end = min(index + char_limit // 2, len(content))
        return content[start:end]
    return None


def about(request):
    return render(request, "About me.html")


def work_in_progress(request):
    return render(request, "Work_in_progress.html")


def all_articles(request):
    return render(request, "All_articles.html")


# Statistics #####
def st(request):
    # Filter and order articles
    articles = Article.objects.filter(group='Statistics').order_by('order')

    # Paginate the articles (e.g., 5 articles per page)
    paginator = Paginator(articles, 4)
    page_number = request.GET.get('page')  # Get the current page number from the query parameters
    page_obj = paginator.get_page(page_number)  # Get the articles for the current page

    # Pass `page_obj` to the template
    return render(request, "Statistics/ST.html", {'page_obj': page_obj})


def st_introduction_st(request):
    article = get_object_or_404(Article, title="Introduction to Statistics")
    return render(request, "Statistics/ST_Introduction_ST.html", {'article': article})


def st_descriptive_st(request):
    """
    Handles requests for the 'Descriptive Statistics' page.
    ----------
    Parameters:
    request : HttpRequest
        The HTTP request object containing metadata about the request.

    Returns:
    HttpResponse
        Renders the 'Statistics/ST_Descriptive_ST.html' template with the following context:
        - plot_html: A dictionary containing HTML representations of generated plots (if any).
        - error_message: A string containing an error message, if applicable.
        - article: The fetched article object titled "Descriptive Statistics".

    Functionality:
    - Responds to GET and POST requests.
    - Displays an interactive page where users can:
        1. Provide custom numerical data for analysis.
        2. Use predefined datasets (normal, skewed, or outliers) for analysis.
    - Handles errors in data input and allows clearing of plots.
    """
    error_message = None
    plot_html = {}

    # Fetch the article object
    article = get_object_or_404(Article, title="Descriptive Statistics")

    if request.method == "POST":
        # Handle the "Clear Plot" button
        if 'clear_plot' in request.POST:
            plot_html = {}  # Clear the plot
            error_message = None
            return render(request, "Statistics/ST_Descriptive_ST.html", {
                'plot_html': plot_html,
                'error_message': error_message,
                'article': article,
            })

        # Determine which button was clicked
        submit_type = request.POST.get("submit_type")

        # Check if "data_type" is provided for custom data
        if request.POST.get("data_type") == "numerical":
            data_input = request.POST.get("data_input")
            try:
                num = numerical(data_input)
                plot_html = calculate_descriptions(num)
            except ValueError as e:
                error_message = str(e)

        elif submit_type == "normal":
            # Use predefined normal dataset
            predefined_data = premade("normal")
            plot_html = calculate_descriptions(predefined_data)

        elif submit_type == "skewed":
            # Use predefined skewed dataset
            predefined_data = premade("skewed")
            plot_html = calculate_descriptions(predefined_data)

        elif submit_type == "outliers":
            # Use predefined dataset with outliers
            predefined_data = premade("outliers")
            plot_html = calculate_descriptions(predefined_data)

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


def st_descriptive_st(request):
    error_message = None
    plot_html = {}
    # Fetch the article object
    article = get_object_or_404(Article, title="Descriptive Statistics")

    if request.method == "POST":
        # Handle the "Clear Plot" button
        if 'clear_plot' in request.POST:
            plot_html = {}  # Clear the plot
            error_message = None
            return render(request, "Statistics/ST_Descriptive_ST.html", {
                'plot_html': plot_html,
                'error_message': error_message,
                'article': article,
            })
        # Get the user input
        data_input = request.POST.get("data_input")  # Comma-separated values

        try:
            # Convert to integers for numerical data
            num = numerical(data_input)
            plot_html = calculate_descriptions(num)

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

def st_data_visualization(request):
    article = get_object_or_404(Article, title='Data Visualization')
    return render(request, "Statistics/ST_Data_visualization.html", {'article': article})


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







