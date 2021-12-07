from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/new_entry", views.new_entry, name="new_entry"),
    path("wiki/search", views.search, name="search"),
    path("wiki/random", views.random, name="random"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("wiki/<str:title>/edit", views.edit, name="edit")
]
