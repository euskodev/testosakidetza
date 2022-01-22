from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.contrib.auth.forms import User


class LoginForm(forms.Form):
    username = forms.CharField(
        label='',
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Usuario',
                'class': 'form-control form-control-lg'
            }
        )
    )
    password = forms.CharField(
        label='',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password',
                'class': 'form-control form-control-lg'
            }
        )
    )

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        if not authenticate(username=username, password=password):
            raise forms.ValidationError('Los datos de usuario no son correctos')
        
        return self.cleaned_data


class UserRegisterForm(forms.ModelForm):
    
    username = forms.CharField(
        label='',
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Usuariodsdf',
                'class': 'form-control form-control-lg'
            }
        )
    )

    password1 = forms.CharField(
        #label = 'Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder':'Contraseña',
                'class': 'form-control form-control-lg'
            }
        )
    )

    password2 = forms.CharField(
        #label = 'Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder':'Repetir contraseña',
                'class': 'form-control form-control-lg'
            }
        )
    )

    class Meta:
        
        model = User
        fields = (
            'username',


        )
    def clean_password2(self):
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            self.add_error('password2', 'Las contraseñas no coinciden')


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password1','password2']

        help_texts = {
        'username' : None,
        'first_name': None,
        'last_name': None,
        'email': None,
        'password1': None,
        'password2': None,
        }


    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['username'].label = "Nombre de usuario"
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].label = "Nombre"
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].label = "Apellido"
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].label = "Email"
        #self.fields['birth_date'].widget.attrs.update({'class': 'form-control'})
        #self.fields['birth_date'].label = "Fecha nacimiento"
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].label = "Password"
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].label = "Confirmar password"

    field_order = [
        'username',
        'first_name',
        'last_name',
        'email',
        'password1',
        'password2']

    
    

        

class ResetPasswordForm(UserCreationForm):
    email = forms.CharField(
        label='',
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Email',
                'class': 'form-control form-control-lg'
            }
        )
    )

    