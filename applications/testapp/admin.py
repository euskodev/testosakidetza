from django.contrib import admin
from .models import Modality
from .models import TestQuestion
from .models import UserAnswers
from .models import TestCounter

# Register your models here.

class ModalityAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )
admin.site.register(Modality,ModalityAdmin)

class TestQuestionAdmin(admin.ModelAdmin):
    list_display = (
        'number',
        'question',
        'a',
        'b',
        'c',
        'd',
        'answer',
        'nameModality'
    )
admin.site.register(TestQuestion,TestQuestionAdmin)


class UserAnswersAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'modality',
        'numberQuestion',
        'correctAnswerCounterSameQuestion',
        'wrongAnswerCounterSameQuestion'
    )
admin.site.register(UserAnswers,UserAnswersAdmin)


class TestCounterAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'modality',
        'counter',
        'listQuestionsNumbers'
    )
admin.site.register(TestCounter,TestCounterAdmin)