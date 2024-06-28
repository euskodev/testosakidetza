from django.contrib import admin
from .models import Category, Test, UserAnswer

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id","name")
admin.site.register(Category,CategoryAdmin)


class TestAdmin(admin.ModelAdmin):
    list_display = ("id","category", "question", "aAnswer", "bAnswer", "cAnswer", "dAnswer", "correctAnswer")
admin.site.register(Test,TestAdmin)


class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ("id","user", "number", "category", "answerProgresionCorrect", "correctAnswerCounter", "incorrectAnswerCounter", "datetime")
admin.site.register(UserAnswer,UserAnswerAdmin)
