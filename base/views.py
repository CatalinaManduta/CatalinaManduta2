# Create your views here.
from django.shortcuts import render
from .interactive_plots import interactive_plot

def home(request):
    return render(request, "Home.html")


def contact(request):
    return render(request, "Contact.html")


def about(request):
    return render(request, "About me.html")


def work_in_progress(request):
    return render(request, "Work in progress.html")


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


def st_linear_regression(request):
    graph_html = interactive_plot(request)
    return render(request, "Statistics/ST_Linear_regression.html", {'graph_html': graph_html})