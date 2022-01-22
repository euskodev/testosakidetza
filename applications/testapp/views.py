from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.views.generic import (
    TemplateView,
    ListView,
    CreateView
)
from .models import TestQuestion
from .models import Modality
from .models import UserAnswers
from .models import TestCounter
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.db.models import Q
from .forms import UserAnswerForm
import datetime
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.db import connection


class testFilterByModalityAndByUserView(ListView):
    model = TestQuestion
    template_name = 'test/question.html'
    urlReturn = 'test_app:test'

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            urlReturn = 'test_app:test'

            questionMod = self.kwargs['questionModality']

            #Tomar userId 
            username=self.request.user.id
            

            #Si se pasa argumento por URL
            if questionMod:

                #Tomar ID de la modalidad o categoría de preguntas
                modID = Modality.objects.filter(name=questionMod)
                modalidadID = modID[0].id

                #Mirar si existe registro de conteo de preguntas de ese usuario/modalidad si no hay, se crea uno.
                exist10QuestionCounter = TestCounter.objects.filter(user=username,modality=modalidadID)

                if exist10QuestionCounter: #Existe de sistema de conteo de preguntas

                    #Leer sistema contador:
                    listQuestionFromTestCounter = TestCounter.objects.get(user=username, modality=modalidadID)
                    counter = listQuestionFromTestCounter.counter
                    
                    passedQuestionList=UserAnswers.objects.filter(modality__name=questionMod, user=username, correctAnswerCounterSameQuestion__gte=4).values('numberQuestion')
                    #Seleccionar acorde a las pregutas que quedan. Noramlmente 10, que si quedan menos se seleccionarán menos.
                    totalNewQuestionList = TestQuestion.objects.filter(nameModality__name=questionMod).order_by('number').exclude(number__in=passedQuestionList).count()
                    if totalNewQuestionList > 10:
                        selectQuantyNum = 10
                    else:
                        selectQuantyNum = totalNewQuestionList
                    newQuestionList = TestQuestion.objects.filter(nameModality__name=questionMod).order_by('number').exclude(number__in=passedQuestionList)[:selectQuantyNum]
                    
                    if counter < selectQuantyNum-1: 
                        #Sumar contador
                        counter = counter +1
                        #Guardar nuevo valor contador
                        saveCounter = TestCounter.objects.get(user=username, modality=modalidadID)
                        saveCounter.counter = counter
                        saveCounter.save()
                        #Seleccionar pregunta
                        listQuestionFromTestCounter = TestCounter.objects.get(user=username, modality=modalidadID)
                        number10QuestionList=listQuestionFromTestCounter.listQuestionsNumbers
                        array10Numbers = number10QuestionList.split(sep=',') #Pasar string a list
                        numberNextQuestion=array10Numbers[counter]
                        newQuestion = TestQuestion.objects.filter(nameModality__name=questionMod, number=numberNextQuestion)
                        object_list = newQuestion

                    else: #Si counter llega a 9... que hay que poner COUNTER a 0 y volver a hacer la select de 10 números (Si está finalizando las preguntas no serán 10, sino menos... ¡Por implementar!)
                        #Contador a 0
                        counter=0
                        #Guardar nuevo valor de contador
                        saveCounter = TestCounter.objects.get(user=username, modality=modalidadID)
                        saveCounter.counter = counter
                        saveCounter.save()
                        #Selección nuevo string con 10 numbers sin superar
                        passedQuestionList=UserAnswers.objects.filter(modality__name=questionMod, user=username, correctAnswerCounterSameQuestion__gte=4).values('numberQuestion')
                        #Seleccionar acorde a las pregutas que quedan. Noramlmente 10, que si quedan menos se seleccionarán menos.
                        totalNewQuestionList = TestQuestion.objects.filter(nameModality__name=questionMod).order_by('number').exclude(number__in=passedQuestionList).count()
                        print("Total de preguntas restantes SI LLEGA A 9: ", totalNewQuestionList)
                        if totalNewQuestionList > 10:
                            selectQuantyNum = 10
                        else:
                            selectQuantyNum = totalNewQuestionList
                        newQuestionList = TestQuestion.objects.filter(nameModality__name=questionMod).order_by('number').exclude(number__in=passedQuestionList)[:selectQuantyNum]
                        #Guardar nueva lista de 10 números:
                        stringNumbers=",".join(str(q.number) for q in newQuestionList) #Linea 104 que devuelve error (pasar array a string)
                        SaveList = TestCounter.objects.get(user=username, modality=modalidadID)
                        SaveList.listQuestionsNumbers = stringNumbers
                        SaveList.save()
                        #Seleccionar pregunta
                        
                        listQuestionFromTestCounter = TestCounter.objects.get(user=username, modality=modalidadID) #Queryset de Testcounter (Modality/User)
                        countListQuestionFromTestCounter = TestCounter.objects.get(user=username, modality=modalidadID)
                        number10QuestionList=listQuestionFromTestCounter.listQuestionsNumbers # Tomar string
                        lenNumber10QuestionList = len(number10QuestionList)
                        print("Largo de lenNumber10QuestioList: ",lenNumber10QuestionList)
                        array10Numbers = number10QuestionList.split(sep=',') #Pasar string a list
                        lenArray = len(array10Numbers)
                        if lenNumber10QuestionList > 0:
                            numberNextQuestion=int(array10Numbers[counter])
                        
                            newQuestion = TestQuestion.objects.filter(nameModality__name=questionMod, number=numberNextQuestion)
                            print(newQuestion)
                            object_list = newQuestion

                        else:
                            print("Redirigir a google...")
                            urlReturn = 'test_app:congratulations'

                else: #No existe un sistema de conteo de preguntas.   
                    modID = Modality.objects.filter(name=questionMod)
                    create10QuestionNumberList = TestCounter.objects.create(user_id=username,modality=modID[0],counter=0,listQuestionsNumbers='1,2,3,4,5,6,7,8,9,10')            

                    #Contador a 0
                    counter=0
                    #Guardar nuevo valor contador
                    saveCounter = TestCounter.objects.get(user=username, modality=modalidadID)
                    saveCounter.counter = counter
                    saveCounter.save()
                    #Selección nuevo string con 10 numbers sin superar
                    passedQuestionList=UserAnswers.objects.filter(modality__name=questionMod, user=username, correctAnswerCounterSameQuestion__gte=4).values('numberQuestion')
                    totalNewQuestionList = TestQuestion.objects.filter(nameModality__name=questionMod).order_by('number').exclude(number__in=passedQuestionList).count()
                    print("Total de preguntas restantes en NO EXISTE SISTEMA: ", totalNewQuestionList)
                    if totalNewQuestionList > 10:
                        selectQuantyNum = 10
                    else:
                        selectQuantyNum = totalNewQuestionList
                    newQuestionList = TestQuestion.objects.filter(nameModality__name=questionMod).order_by('number').exclude(number__in=passedQuestionList)[:selectQuantyNum]
                    #Guardar nuevo list de 10 numbers

                    #stringNumbers = newQuestionList[0],',',newQuestionList[1],',',newQuestionList[2],',',newQuestionList[3],',',newQuestionList[4],',',newQuestionList[5],',',newQuestionList[6],',',newQuestionList[7],',',newQuestionList[8],',',newQuestionList[9]
                    stringNumbers=",".join(str(q.number) for q in newQuestionList)
                    SaveList = TestCounter.objects.get(user=username, modality=modalidadID)
                    SaveList.listQuestionsNumbers = stringNumbers
                    SaveList.save()
                    #Seleccionar pregunta
                    listQuestionFromTestCounter = TestCounter.objects.get(user=username, modality=modalidadID) #Queryset de Testcounter (Modality/User)
                    number10QuestionList=listQuestionFromTestCounter.listQuestionsNumbers # Tomar string
                    array10Numbers = number10QuestionList.split(sep=',') #Pasar string a list

                    if int(array10Numbers[0]) > 0:
                        numberNextQuestion=int(array10Numbers[counter])
                    else:
                        print("No quedan más preguntas... ir al menu principal con un message...")
                        
                    newQuestion = TestQuestion.objects.filter(nameModality__name=questionMod, number=numberNextQuestion)
                    object_list = newQuestion  

            else: #No se ha pasado argumento por url
                
                print("No se ha pasado modalidad por argumento")
                object_list = TestQuestion.objects.all()
            if 'object_list' in locals(): #Para comprobar si la variable está declarada.
                context = super(testFilterByModalityAndByUserView, self).get_context_data(**kwargs) #Esto sobreescribe el mét
                context['answers'] = UserAnswers.objects.filter(user=username,modality=modalidadID)
                context['object_list'] = object_list
                questionCount = TestQuestion.objects.all().count()
                context['questionCount'] = questionCount
                return context         
            else:
                print("Ir a una página donde se felicite al usuario...")
        
            login_url = reverse_lazy('test_app:test')
        
           








class TestPageView(TemplateView):
    template_name = "test/question.html"

class IndexView(TemplateView):
    template_name = "test/index.html"

class CongratulationsView(TemplateView):
    template_name = "test/congratulations.html"

def nextQuestion(request):
    return render(request,'test/question.html')

def saveUserAnswer(request):
    if request.method == "POST":
        answerCorrectPost = request.POST['answer']
        modalityPost = request.POST['modalityId']
        modalityNamePost = request.POST['modalityName']
        numberQuestion = int(request.POST['numberQuestion'])
        selectedAnswer = request.POST['selectedAnswer']

        print("Respuesta correcta: ", answerCorrectPost)
        print("Respuesta seleccionada: ", selectedAnswer)
        #print("Modalidad: ", modalityPost)
        #print("Número pregunta: ", numberQuestion)
        #print("Nombre modalidad: ", modalityNamePost)

        if request.user.is_authenticated:
            userId=request.user.id
            
        #Mirar contando si existe una respuesta a la misma pregunta de una anterior vez:
        oldAnswer = UserAnswers.objects.filter(user=userId, modality=modalityPost, numberQuestion=numberQuestion).count()
        #print("Respondida antes cuantas veces: ", oldAnswer, " utilizando userId: ", userId, " modalidad: ", modalityPost, " número pregunta: ", numberQuestion)
        
        if oldAnswer > 0:
            #Tomar el valor de contador de correctas en la base de datos:
            correctCounterQuery = UserAnswers.objects.filter(user=userId, modality=modalityPost, numberQuestion=numberQuestion)[:1]
            correctCounterValue = correctCounterQuery[0].correctAnswerCounterSameQuestion
            #print("Contador correctas: ", correctCounterValue)
            
            #Tomar el valor de contador de incorrectas en la base de datos:
            wrongCounterQuery = UserAnswers.objects.filter(user=userId, modality=modalityPost, numberQuestion=numberQuestion)[:1]
            wrongCounterValue = wrongCounterQuery[0].wrongAnswerCounterSameQuestion
            #print("Contador incorrectas: ", wrongCounterValue)

            #Si la respuesta ha sido correcta CORRECT sumamos valor a la variable correctCounterValue y hacemos update
            if selectedAnswer == answerCorrectPost:
                #print("Respuesta correcta")
                correctCounterValue=correctCounterValue+1
                #print("Correctas sumadas: ", correctCounterValue)
                UserAnswers.objects.filter(user=userId, modality=modalityPost, numberQuestion=numberQuestion).update(correctAnswerCounterSameQuestion = correctCounterValue)

            #Si la respuesta ha sido incorrecta WRONG sumamos valor a la variable wrongCounterValue y hacemos update    
            elif selectedAnswer != answerCorrectPost:
                #print("Respuesta incorrecta")
                wrongCounterValue=wrongCounterValue+1
                correctCounterValue=0
                #print("Incorrectas sumadas: ", wrongCounterValue)
                UserAnswers.objects.filter(user=userId, modality=modalityPost, numberQuestion=numberQuestion).update(wrongAnswerCounterSameQuestion = wrongCounterValue,correctAnswerCounterSameQuestion = correctCounterValue)
                
                
                #Guardar respuesta de nueva pregunta:
        else:
            if selectedAnswer == answerCorrectPost:
                correctCounterNewInsert = 1
                wrongCounterNewInsert = 0
            if selectedAnswer != answerCorrectPost:
                correctCounterNewInsert = 0
                wrongCounterNewInsert = 1
            newAnswer = UserAnswers.objects.create(user_id=userId, modality_id=modalityPost, numberQuestion=numberQuestion, correctAnswerCounterSameQuestion=correctCounterNewInsert, wrongAnswerCounterSameQuestion=wrongCounterNewInsert)
            newAnswer.save()

    else:
        print("No es post")
    
    #modalityName = UserAnswers.object.get(modality=questionModality__)
        
    #return(redirect('testapp.views.testFilterByModalityAndByUserView',questionModality=1))
    #return(redirect('test_app:test',questionModality=modalityPost))
    return HttpResponseRedirect(reverse('test_app:test', kwargs={'questionModality': modalityNamePost}))
