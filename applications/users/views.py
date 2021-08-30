from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import (
    FormView
)
from django.http import HttpResponseRedirect
from django.views.generic import (
    TemplateView,
    ListView,
    CreateView,
    View
)
from django.urls import reverse_lazy, reverse
from .forms import (
    LoginForm,
    UserRegisterForm,
    CustomUserCreationForm,
    ResetPasswordForm
)
from .models import User
from django.utils.crypto import get_random_string
import datetime
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from applications.users.models import TokenToUser
from applications.users.models import Profile
from django.contrib import messages
from django.utils.timezone import now


# Create your views here.
class HomePageView(TemplateView):
    template_name = "users/index.html"



class UserLoginView(FormView):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home_app:home')

    def form_valid(self, form):
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )
        login(self.request, user)
        return super(UserLoginView, self).form_valid(form)

class UserLogoutView(FormView):
    def get(self, request, *args, **kargs):
        logout(request)
        return HttpResponseRedirect(
            reverse(
                'home_app:home'
            )
        )

"""class UserRegistrationView(CreateView):
    template_name = 'users/user_registration.html'
    model = User
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('home_app:home')"""

class UserRegistrationView(CreateView):
    template_name = 'users/user_registration.html'
    model = User
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('home_app:home')

    def post(self, request):
        email = request.POST.get('email', None)
        user = User.objects.filter(email__exact=email).last()
        if True:
            #token = get_random_string(length=34)
            url_activation = 'http://127.0.0.1:8000{path}'.format(domain=settings.BASE_URL,path=reverse_lazy('users_app:user-login', kwargs={'email': email}))
            context = {'url_activation': url_activation, 'user': user.username, 'date': now().strftime('%Y-%m-%d %H:%M:%S')}
            html_message = render_to_string('users/email_confirm_new_user.html', context)
            plain_message = strip_tags(html_message)
            texto_email=send_mail(subject='Confirmación de registro de usuario', message=plain_message, from_email='info@prueba.com',
                          recipient_list=[email], html_message=html_message)
            if texto_email:
                #user_token = TokenToUser(user=user, token=token, date=now().strftime('%Y-%m-%d %H:%M:%S'))
                #user_token.save()
                messages.success(request, 'Ha sido enviado un email a su correo para resetear el password.')
            else:
                messages.error(request, '¡ups! Algo sucedió mal.')
        else:
            messages.error(request, 'El email introducido no existe. Pruebe de nuevo o regístrese como nuevo usuario.')
        return redirect(reverse_lazy('users_app:user-login'))



class UserResetView(View):
    template_name = "users/reset.html"
    form_class = ResetPasswordForm
    success_url = reverse_lazy('home_app:home')

    def get(self, request):
        return render(request, self.template_name, {})

    def post(self, request):
        email = request.POST.get('email', None)
        user = User.objects.filter(email__exact=email).last()
        if user:
            token = get_random_string(length=34)
            url_reset = 'http://127.0.0.1:8000{path}'.format(domain=settings.BASE_URL,path=reverse_lazy('users_app:user_newPassword', kwargs={'token': token}))
            #url_reset = '{domain}/{path}'.format(domain=settings.BASE_URL,path=reverse_lazy('users_app:user_newPassword', kwargs={'token': token}))
            #url_reset = '{domain}{path}'.format(domain=settings.BASE_URL,path='/'+token)
            context = {'url_reset': url_reset, 'user': user.username, 'date': now().strftime('%Y-%m-%d %H:%M:%S')}
            html_message = render_to_string('users/email_template.html', context)
            plain_message = strip_tags(html_message)
            texto_email=send_mail(subject='Reset de contraseña', message=plain_message, from_email='retegi84@gmail.com',
                          recipient_list=[email], html_message=html_message)
            if texto_email:
                user_token = TokenToUser(user=user, token=token, date=now().strftime('%Y-%m-%d %H:%M:%S'))
                user_token.save()
                messages.success(request, 'Ha sido enviado un email a su correo para resetear el password.')
            else:
                messages.error(request, '¡ups! Algo sucedió mal.')
        else:
            messages.error(request, 'El email introducido no existe. Pruebe de nuevo o regístrese como nuevo usuario.')
        return redirect(reverse_lazy('users_app:user-reset'))


class CreateNewPasswordView(View):
    template_name = "users/crear_password.html"
    template_name2 = "users/login.html"
    success_url = reverse_lazy('home_app:home')

    def get(self, request, token):
        return render(request, self.template_name, {})

    def post(self, request, token):
        if request.method == 'POST':
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            if password1 == password2:
                t = TokenToUser.objects.get(token=token)
                u = t.user
                u.set_password(password1)
                u.save()
                messages.success(request, 'La nueva contraseña ha sido creada con éxito. Ya puedes iniciar sesión con la nueva contraseña')
                
                return redirect(reverse_lazy('users_app:user-login'))
            else:
                messages.success(request, 'Las contraseñas deben coincidir. Prueba de nuevo.')
                return render(request, self.template_name, {})
        





        
        
        
