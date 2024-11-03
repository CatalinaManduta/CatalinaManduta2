from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("contact/", views.contact, name="contact"),
    path("about/", views.about, name="about"),
    path("articles/", views.all_articles, name="articles"),
    path("introduction genetics/", views.ig, name="introduction genetics"),
    path("machine learning/", views.ml, name="machine learning"),
    path("machine learning/pattern mining/", views.ml_pattern_mining, name="pattern mining"),
    path("introduction genetics/classical genetics/", views.ig_classical_genetics, name="classical genetics"),
    path("bioinformatics/", views.bi, name="bioinformatics"),
    path("work in progress/", views.work_in_progress, name="work in progress"),
    path("statistics/", views.st, name="statistics"),
    path("statistics/linear regression/", views.st_linear_regression, name="linear regression")
]
