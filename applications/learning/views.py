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
from .models import Test
# Create your views here.


def getFirstQuestion(userId, categoryName):
    try:
        #firstTextQuery=UserAnswer.objects.filter(user=userId, category=categoryName, correctAnswerCounter__lt=4).order_by('number').first()
        firstTextQuery=UserAnswer.objects.filter(user=userId, category=categoryName, answerProgresionCorrect__lt=4).order_by('number').first()
        print("primeras preguntas: ", firstTextQuery)
        first4TextQuery=UserAnswer.objects.filter(user=userId, category=categoryName, answerProgresionCorrect__lt=4).order_by('number')[:4]
        print("primeras 4 preguntas", first4TextQuery[0].number, first4TextQuery[1].number, first4TextQuery[2].number, first4TextQuery[3].number)
        print("TryUNO", first4TextQuery[0].number,first4TextQuery[3].number)
             
    except:
        print("no es posible seleccionar 4 preguntas")
        try:
            print("3 preguntas seleccionadas")
            #firstTextQuery=UserAnswer.objects.filter(user=userId, category=categoryName, correctAnswerCounter__lt=4).order_by('number').first()
            firstTextQuery=UserAnswer.objects.filter(user=userId, category=categoryName, answerProgresionCorrect__lt=4).order_by('number').first()
            print("primera preguntas: ", firstTextQuery)
            first4TextQuery=UserAnswer.objects.filter(user=userId, category=categoryName, answerProgresionCorrect__lt=4).order_by('number')[:3]
            print("primeras 3 preguntas", first4TextQuery[0].number, first4TextQuery[1].number, first4TextQuery[2].number)
            totalLessThan4=UserAnswer.objects.filter(user=userId, category=categoryName, answerProgresionCorrect__lt=4).order_by('number').count()
            ultimoNumero = int(first4TextQuery[2].number)
            try:
                preguntaparacompletarla4 = Test.objects.filter(category__name=categoryName, number=ultimoNumero)
                print("Pregunta para completar la 4: ",preguntaparacompletarla4)
            except:
                print("No hay más preguntas disponibles en esta categoría[100]")
                    
        except:
            print("no es posible seleccionar 3 preguntas")
            try:
                print("2 preguntas seleccionadas")
                #firstTextQuery=UserAnswer.objects.filter(user=userId, category=categoryName, correctAnswerCounter__lt=4).order_by('number').first()
                firstTextQuery=UserAnswer.objects.filter(user=userId, category=categoryName, answerProgresionCorrect__lt=4).order_by('number').first()
                print("primeras preguntas: ", firstTextQuery)
                first4TextQuery=UserAnswer.objects.filter(user=userId, category=categoryName, answerProgresionCorrect__lt=4).order_by('number')[:2]
                print("primeras 2 preguntas", first4TextQuery[0].number, first4TextQuery[1].number)
                ultimoNumero = int(first4TextQuery[1].number)
                try:
                    preguntaparacompletarla3 = Test.objects.filter(category__name=categoryName, number=ultimoNumero+1)
                    preguntaparacompletarla4 = Test.objects.filter(category__name=categoryName, number=ultimoNumero+1)
                    print("Nuevas preguntas seleccionada da tabla TEST: ",preguntaparacompletarla3, preguntaparacompletarla4)
                except:
                    print("No hay más preguntas disponibles en esta categoría[101]")
            except:
                print("no es posible seleccionar 2 preguntas")
                try:
                    print("1 pregunta seleccionada")
                    #firstTextQuery=UserAnswer.objects.filter(user=userId, category=categoryName, correctAnswerCounter__lt=4).order_by('number').first()
                    firstTextQuery=UserAnswer.objects.filter(user=userId, category=categoryName, answerProgresionCorrect__lt=4).order_by('number').first()
                    print("primera pregunta: ", firstTextQuery)
                    first4TextQuery=UserAnswer.objects.filter(user=userId, category=categoryName, answerProgresionCorrect__lt=4).order_by('number')[:1]
                    print("primera pregunta", first4TextQuery[0].number)
                    ultimoNumero = int(first4TextQuery[0].number)
                    try:
                        preguntaparacompletarla2 = Test.objects.filter(category__name=categoryName, number=ultimoNumero+1)
                        preguntaparacompletarla3 = Test.objects.filter(category__name=categoryName, number=ultimoNumero+2)
                        preguntaparacompletarla4 = Test.objects.filter(category__name=categoryName, number=ultimoNumero+3)
                        #print("Nuevas preguntas seleccionada da tabla TEST: ",first4TextQuery[1].num,first4TextQuery[2].num, first4TextQuery[3].num)
                        print("Nuevas preguntas seleccionada da tabla TEST: ",preguntaparacompletarla2,preguntaparacompletarla3, preguntaparacompletarla4)
                    except:
                        print("No hay más preguntas disponibles en esta categoría[102]")
                except:
                    print("no es posible seleccionar NINGUNA pregunta")
    print("Resultado de la función pero dentro:",firstTextQuery)
    return firstTextQuery


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
        firstTextQuery = getFirstQuestion(userId, categoryName)
        #firstTextQuery = UserAnswer.objects.filter(user=userId, category=categoryName, correctAnswerCounter__lt=4).order_by('number').first()
        
        try:
            firstTextNumber = firstTextQuery.number
            print("La primera pregunta es la: ", firstTextNumber)
        except:
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
        categoryNamePost = request.POST.get('category', '')
        numberPost = request.POST.get('number', '')
        userAnswer_dePost = request.POST.get('answer','')
        correctAnswer_dePost = request.POST.get('correctAnswer','')
        userName=self.request.user
        userId = self.request.user.id

        #CHAT
        chatPhrase = request.POST.get('chatPhrase','')
        chat = TestChat()
        chat.text = chatPhrase
        if chat.text:
            chat.user = User.objects.get(id=userId)
            chat.datetime = datetime.now()
            chat.save()
        #FIN CHAT

        try:
            #UserAnswer.objects.get(user = userName, category=categoryNamePost, number=numberPost)
            form = UserAnswer.objects.get(user = userName, category=categoryNamePost, number=numberPost)
           
            #Contador               
            if userAnswer_dePost == correctAnswer_dePost:
                form.answerProgresionCorrect = form.answerProgresionCorrect + 1
                if form.answerProgresionCorrect > 4:
                    form.answerProgresionCorrect = 4
                form.correctAnswerCounter = form.correctAnswerCounter + 1
            else:
                form.incorrectAnswerCounter = form.incorrectAnswerCounter + 1
                form.answerProgresionCorrect = 0
            form.lastAnsweredQuestion = numberPost
            form.save()
            #FIN CONTADOR
        except:
            #AL NO EXISTIR SE CREA UNO NUEVO
            form = UserAnswer()
            form.user=self.request.user
            form.number=numberPost
            form.category=categoryNamePost
            form.incorrectAnswerCounter = 0
            if userAnswer_dePost == correctAnswer_dePost:
                form.correctAnswerCounter = 1
                form.answerProgresionCorrect = 1
                form.incorrectAnswerCounter = 0
                
            else:
                form.correctAnswerCounter = 0
                form.incorrectAnswerCounter = 1
                form.answerProgresionCorrect = 0
            form.lastAnsweredQuestion = numberPost    
            form.save()  
            #FIN CONTADOR

        context = super().get_context_data(**kwargs)
        context['categoria'] = self.kwargs['category']
        category = self.kwargs['category']
        context['categoria'] = category
        number = int(numberPost)
        totalTest=Test.objects.filter(category=category).count()
        print("Esta usuario en esta categoría tiene ", totalTest, " preguntas. ")
        if number == totalTest:
            number = 0
        categoryId = self.kwargs['category']
        categoryQuery = Category.objects.get(id=categoryId)
        categoryName = categoryQuery.name
        print("UserID: ",userId, " CategoryName: ", categoryName, " correctAnswerCounter: ")
        try:
            print("Try 0-3")
            #firstTextQuery = UserAnswer.objects.get(user=userId, category=categoryName, correctAnswerCounter__lt=4, number = number)
            #firstTextNumber = firstTextQuery.number
            questionNumberLast = UserAnswer.objects.filter(user=userId, category=categoryName, correctAnswerCounter__lt=4).order_by('number')[3]
            print(questionNumberLast.number)
            questionNumberCount = UserAnswer.objects.filter(user=userId, category=categoryName, correctAnswerCounter__lt=4).count()
            print("Numero preguntas: ", questionNumberCount)
            questionNumber0 = UserAnswer.objects.filter(user=userId, category=categoryName, correctAnswerCounter__lt=4).order_by('number')[0]
            print(questionNumber0.number)
        except:
            try:
                print("Try 0-2")
                questionNumberLast = UserAnswer.objects.filter(user=userId, category=categoryName, correctAnswerCounter__lt=4).order_by('number')[2]
                print(questionNumberLast.number)
                questionNumber0 = UserAnswer.objects.filter(user=userId, category=categoryName, correctAnswerCounter__lt=4).order_by('number')[0]
            except:
                try:
                    print("Try 0-1")
                    questionNumberLast = UserAnswer.objects.filter(user=userId, category=categoryName, correctAnswerCounter__lt=4).order_by('number')[1]
                    print(questionNumberLast.number)
                    questionNumber0 = UserAnswer.objects.filter(user=userId, category=categoryName, correctAnswerCounter__lt=4).order_by('number')[0]
                except:
                    try:
                        print("Try 0")
                        questionNumber0 = UserAnswer.objects.filter(user=userId, category=categoryName, correctAnswerCounter__lt=4).order_by('number')[0]
                        print(questionNumberLast.number)
                    except:
                        print("No hay más preguntas")
                        respuesta="No hay más resultados"

        number=questionNumber0.number    
        firstTextNext = number
        print("Siguiente pregunta", firstTextNext)
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
        context['questionList'] = UserAnswer.objects.filter(user=userName, category= categoryNamePost)
        context['chat'] = TestChat.objects.all()
        return render(request, 'home/preguntas.html', context)


    