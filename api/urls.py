from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.hello),
    path("users/", views.users_list),
    path("reports/", views.reports_list),
    path('stock/<str:ticker>/', views.StockReportView.as_view(), name='stock-report'),
]