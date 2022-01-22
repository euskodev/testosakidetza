from django import forms
from .models import UserAnswers

class UserAnswerForm(forms.ModelForm):
    class Meta:
        model = UserAnswers
        fields = ('__all__')
    def __init__(self, *args, **kwargs):
        super(UserAnswerForm, self).__init__(*args, **kwargs)
        self.fields['user'].widget.attrs.update({'class': 'form-control'})
        self.fields['user'].label = "Area de la instalación"
        self.fields['modality'].widget.attrs.update({'class': 'form-control'})
        self.fields['modality'].label = "Tipo de instalación"
        self.fields['numberQuestion'].widget.attrs.update({'class': 'form-control'})
        self.fields['numberQuestion'].label = "Subtipo de instalación"
        #self.fields['datetimeAnswer'].widget.attrs.update({'class': 'form-control'})
        #self.fields['datetimeAnswer'].label = "Area de la instalación"
        self.fields['correctAnswerCounterSameQuestion'].widget.attrs.update({'class': 'form-control'})
        self.fields['correctAnswerCounterSameQuestion'].label = "Contador correctas"
        self.fields['wrongAnswerCounterSameQuestion'].widget.attrs.update({'class': 'form-control'})
        self.fields['wrongAnswerCounterSameQuestion'].label = "Contador incorrectas"

    field_order = [
        'user',
        'modality',
        'numberQuestion',
        #'datetime',
        'correctAnswerCounterSameQuestion',
        'wrongAnswerCounterSameQuestion']