from django.urls import path, include
from .import views



urlpatterns = [
    path("", views.index, name="index"),
    path('<str:short_code>/', views.redirect_to_original, name='redirect'),
    
    ]