from django.urls import path, include
from .import views
from django.urls import path
from . import views

urlpatterns = [
    path('create-shortlink/', views.CreateShortLinkView.as_view(), name='create-shortlink'),
    path('list-shortlinks/', views.ListShortLinksView.as_view(), name='list-shortlinks'),
    path('pageviews-count/', views.PageViewsCountView.as_view(), name='pageviews-count'),
    path('login/', views.CustomAuthToken.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path("", views.index, name="index"),
    path('<str:short_code>/', views.redirect_to_original, name='redirect'),
    
    ]