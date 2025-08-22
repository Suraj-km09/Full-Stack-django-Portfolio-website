from django.urls import path
from . import views

urlpatterns = [
    path('', views.portfolio_home, name='portfolio_home'),
    path('cv/', views.generate_cv_pdf, name='generate_cv_pdf'),
]