"""data_got URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from . views import HomeView, ReviewsView, TeamsView, WhatWeDoView, PortfolioView, ContactView, ClientView

urlpatterns = [
    path('', RedirectView.as_view(url='home/', permanent=False)),
    path('admin/', admin.site.urls),
    path('home/', HomeView.as_view(), name='home'),
    path('what-we-do/', WhatWeDoView.as_view(), name='what-we-do'),
    path('portfolio/', PortfolioView.as_view(), name='portfolio'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('reviews/', ReviewsView.as_view(), name='reviews'),
    path('teams/', TeamsView.as_view(), name='teams'),
    path('client/', ClientView.as_view(), name='client'),
    path('auth/', include('authentication.urls', namespace='auth')),
    path('visualisation/', include('visualisation.urls', namespace='visualisation'))
]
