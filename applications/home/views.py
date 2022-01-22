from testosakidetza.settings.base import EMAIL_HOST_USER
from django.http import request
from django.shortcuts import render
from django.views.generic import (
    TemplateView,
    ListView
)
from .models import Home

from django.template.loader import  get_template
from django.core.mail import EmailMultiAlternatives
from django.conf import settings



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


def send_email(contenido):
    context = contenido

    template = get_template('home/correo.html')
    content = template.render(context)

    email = EmailMultiAlternatives(
        context['name'],
        context['mail'],
        settings.EMAIL_HOST_USER,
        ['testosakidetza@gmail.com']
    )
    email.attach_alternative(content, 'text/html')
    email.send()
    print(email)

def index(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        mail = request.POST.get('mail')
        text = request.POST.get('text')
        contenido = {'name': name, 'mail': mail, 'text': text}
        send_email(contenido)
        print("Envio de correo" + mail)

    return render(request, 'home/index.html', {})