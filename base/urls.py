from django.urls import path
from . import views


urlpatterns = [
    # General
    path("", views.home, name="home"),
    path("contact/", views.contact, name="contact"),
    path('contact/success/', views.contact_success_view, name='contact_success'),
    path("about/", views.about, name="about"),
    path("articles/", views.all_articles, name="articles"),
    path("work in progress/", views.work_in_progress, name="work in progress"),
    path('search/', views.search_html_files, name='search_html_files'), # Delete this if implementing Elasticseacrch
    # Machine learning
    path("machine learning/", views.ml, name="machine learning"),
    path("machine learning/pattern mining/", views.ml_pattern_mining, name="pattern mining"),
    path("machine learning/clustering basics/", views.ml_clustering_basics, name="clustering basics"),
    # Bioinformatics
    path("bioinformatics/", views.bi, name="bioinformatics"),
    # Statistics
    path("statistics/", views.st, name="statistics"),
    path("statistics/introduction to statistics/", views.st_introduction_st, name="introduction to statistics"),
    path("statistics/descriptive statistics/", views.st_descriptive_st, name="introduction to statistics"),
    path("statistics/linear regression/", views.st_linear_regression, name="linear regression"),
    path("statistics/p-value/", views.st_p_value, name="p-value"),
    # Genetics
    path("introduction genetics/", views.ig, name="introduction genetics"),
    path("introduction genetics/classical genetics/", views.ig_classical_genetics, name="classical genetics")
]
