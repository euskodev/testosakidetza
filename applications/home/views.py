from django.shortcuts import render
from django.views.generic import (
    TemplateView,
    ListView
)
from .models import Home



class HomePageView(TemplateView):
    template_name = "home/index.html"

class AvisoLegalView(TemplateView):
    template_name = "home/aviso_legal.html"

class PoliticaDePrivacidadView(TemplateView):
    template_name = "home/politica_de_privacidad.html"

class PoliticaDeCookiesView(TemplateView):
    template_name = "home/politica_de_cookies.html"

class ContactView(TemplateView):
    template_name = "home/contact.html"


