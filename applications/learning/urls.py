from os import name
from django.urls import include, path
from . import views
from .views import NextQuestionView


app_name = 'learning_app'

urlpatterns = [
    path('nextQuestion/<str:category>/', views.NextQuestionView.as_view(), name='nextQuestion'),
]