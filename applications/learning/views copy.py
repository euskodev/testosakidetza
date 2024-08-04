from django.shortcuts import render
from django.views.generic import TemplateView, ListView, FormView
from applications.learning.models import Test, UserAnswer
from django.http import HttpResponse
from django.template import Template
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from applications.social.models import TestChat
from django.contrib.auth.models import User
from applications.learning.models import Category
from django.db.models import Q
# Create your views here.

class NextQuestionView(TemplateView):
    template_name = "home/preguntas.html"


    #Primera vez que se accede a las preguntas
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        userName = self.request.user
        context['user'] = userName
        categoryId = self.kwargs['category']
        categoryQuery = Category.objects.get(id=categoryId)
        categoryName = categoryQuery.name
        context['categoria'] = categoryName
        user = self.request.user
        userId = self.request.user.id
        firstTextQuery = UserAnswer.objects.filter(user=userId, category=categoryName, correctAnswerCounter__lt=4).order_by('number').first()
        #firstTextQuery = UserAnswer.objects.filter(user=userId, category=categoryName, correctAnswerCounter__lt=4).order_by('number').first()

        if firstTextQuery:
            firstTextNumber = firstTextQuery.number
        else:
            firstTextNumber = 1
        context['test'] = Test.objects.filter(category = categoryId, number = firstTextNumber).first()
        #context['test'] = Test.objects.first()
        totalQuestions = Test.objects.filter(category = categoryId).count()
        context['totalQuestions'] = totalQuestions
        testData = Test.objects.first()
        if testData.correctAnswer == 'A':
            answerTest = testData.aAnswer
        if testData.correctAnswer == 'B':
            answerTest = testData.bAnswer
        if testData.correctAnswer == 'C':
            answerTest = testData.cAnswer
        if testData.correctAnswer == 'D':
            answerTest = testData.dAnswer
        context['answerTest'] = answerTest
        user = self.request.user.id
        category = self.kwargs['category']
        #context['questionList'] = UserAnswer.objects.all()
        context['questionList'] = UserAnswer.objects.filter(user=user, category=categoryName)
        #context['chat'] = TestChat.objects.all()
        context['chat'] = TestChat.objects.all()
        return context
        
    #Tras la primera respuesta
    def post(self, request, *args, **kwargs):
        answer_dePosta = request.POST.get('answer','')  # Obtener el valor del campo 'opciones'
        # Aquí puedes procesar la opción seleccionada como lo necesites
        category_dePost = request.POST.get('category', '')
        number_dePost = request.POST.get('number', '')
        userAnswer_dePost = request.POST.get('answer','')
        correctAnswer_dePost = request.POST.get('correctAnswer','')
        user=self.request.user
        userId = self.request.user.id
        chatPhrase = request.POST.get('chatPhrase','')
        chat = TestChat()
        #chat.user = User.objects.get(id=userId)
        chat.text = chatPhrase
        if chat.text:
            chat.user = User.objects.get(id=userId)
            chat.datetime = datetime.now()
            chat.save()

        #Tomar la respuesta del usuario y guardar en la base de datos
        try:
            UserAnswer.objects.get(user = user, category=category_dePost, number=number_dePost)
            form = UserAnswer.objects.get(user = user, category=category_dePost, number=number_dePost)
            if userAnswer_dePost == correctAnswer_dePost:
                form.answerProgresionCorrect = form.answerProgresionCorrect + 1
                form.correctAnswerCounter = form.correctAnswerCounter + 1
            else:
                form.incorrectAnswerCounter = form.incorrectAnswerCounter + 1
                form.answerProgresionCorrect = 0
            form.save()
        except:
            form = UserAnswer()
            form.user=self.request.user
            form.number=number_dePost
            form.category=category_dePost
            form.incorrectAnswerCounter = 0
            if userAnswer_dePost == correctAnswer_dePost:
                form.correctAnswerCounter = 1
                form.answerProgresionCorrect = 1
                form.incorrectAnswerCounter = 0
                
            else:
                form.correctAnswerCounter = 0
                form.incorrectAnswerCounter = 1
                form.answerProgresionCorrect = 0      
            form.save()  
        context = super().get_context_data(**kwargs)
        context['categoria'] = self.kwargs['category']
        category = self.kwargs['category']
        context['categoria'] = category
        number = int(number_dePost)
        totalTest=Test.objects.filter(category=category).count()
        if number == totalTest:
            number = 0
        
        categoryId = self.kwargs['category']
        categoryQuery = Category.objects.get(id=categoryId)
        categoryName = categoryQuery.name
        
        while True:
            try:
                firstTextQuery = UserAnswer.objects.get(user=userId, category=categoryName, correctAnswerCounter__lt=4, number = number)
                firstTextNumber = firstTextQuery.number
                if firstTextNumber:
                    print("se cumple if: ", )
            except:
                print("Error al realizar el get")
                number = number + 1
                firstTextNumber = 0
                
            if firstTextNumber:
                print(firstTextNumber)
                break
            else:
                break

        firstTextNext = number
        context['test'] = Test.objects.filter(category=category).order_by('number')[firstTextNext-1]
        totalQuestions = Test.objects.filter(category=category).count()
        context['totalQuestions'] = totalQuestions

        testData = Test.objects.all().order_by('number')[number]
        if testData.correctAnswer == 'A':
            answerTest = testData.aAnswer
        if testData.correctAnswer == 'B':
            answerTest = testData.bAnswer
        if testData.correctAnswer == 'C':
            answerTest = testData.cAnswer
        if testData.correctAnswer == 'D':
            answerTest = testData.dAnswer
        context['answerTest'] = answerTest
        category = self.kwargs['category']
        context['questionList'] = UserAnswer.objects.filter(user=user, category= category_dePost)
        context['chat'] = TestChat.objects.all()
        return render(request, 'home/preguntas.html', context)


