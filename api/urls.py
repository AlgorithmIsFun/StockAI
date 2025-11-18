from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.hello),
    path("users/", views.users_list),
    path("reports/", views.reports_list),
]