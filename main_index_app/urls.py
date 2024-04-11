from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path("get_final_index", views.GetFinalIndex.as_view(), name="get_final_index"),
]
