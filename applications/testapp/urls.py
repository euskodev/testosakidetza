from django.urls import include, path
from . import views
from .views import testFilterByModalityAndByUserView
from .views import CongratulationsView

app_name = 'test_app'

urlpatterns = [
    path('test/',
        views.TestPageView.as_view(),
        name='test',
    ),
    path('test/<str:questionModality>/',
        views.testFilterByModalityAndByUserView.as_view(),
        name='test',
    ),
    path('nextQuestion/',
        views.nextQuestion,
        name='nextQuestion',
    ),
    path('saveUserAnswer',
        views.saveUserAnswer,
        name='saveUserAnswer',
    ),
    path('congratulations/',
        views.CongratulationsView.as_view(),
        name='congratulations',
    )
]