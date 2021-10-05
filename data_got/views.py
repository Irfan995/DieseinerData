from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'home.html'


class WhatWeDoView(TemplateView):
    template_name = 'what_we_do.html'


class PortfolioView(TemplateView):
    template_name = 'portfolio.html'


class ContactView(TemplateView):
    template_name = 'contact.html'


class ReviewsView(TemplateView):
    template_name = 'reviews.html'


class TeamsView(TemplateView):
    template_name = 'teams.html'


class ClientView(TemplateView):
    template_name = 'client.html'
