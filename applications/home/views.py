from django.shortcuts import render
from django.views.generic import (
    TemplateView,
    ListView
)

class HomePageView(TemplateView):
    template_name = "home/index.html"

class AvisoLegalView(TemplateView):
    template_name = "home/aviso_legal.html"

class PoliticaDePrivacidadView(TemplateView):
    template_name = "home/politica_de_privacidad.html"

class PoliticaDeCookiesView(TemplateView):
    template_name = "home/politica_de_cookies.html"

class ContactView(TemplateView):
    template_name = "home/contactar.html"

class RegistrarseView(TemplateView):
    template_name = "home/registrarse.html"

class IniciarsesionView(TemplateView):
    template_name = "home/iniciar sesion.html"


class RecuperarcontrasenaView(TemplateView):
    template_name = "home/recuperar-contrasena.html"



