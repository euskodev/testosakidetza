from django.shortcuts import render, redirect
from django.views.generic import (
    TemplateView,
    ListView,
    CreateView
)
from .models import TestQuestion
from .models import Modality
from .models import UserAnswers
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.db.models import Q
from .forms import UserAnswerForm
import datetime
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login



from django.db import connection


class TestPageView(TemplateView):
    template_name = "test/question.html"




def nextQuestion(request):
    return render(request,'test/question.html')

def saveUserAnswer(request):
    if request.method == "POST":
        answerCorrectPost = request.POST['answer']
        modalityPost = request.POST['modality']
        numberQuestion = int(request.POST['numberQuestion'])
        """userAnswerA = request.POST.getlist('nameCheckboxA')
        userAnswerB = request.POST.getlist('nameCheckboxB')
        userAnswerC = request.POST.getlist('nameCheckboxC')
        userAnswerD = request.POST.getlist('nameCheckboxD')"""
        selectedAnswer = request.POST['selectedAnswer']
        userAnswer= 1
        ansOK = 1
        ansWrong = 1
        print(answerCorrectPost)
        print(modalityPost)
        print(numberQuestion)
        """print(userAnswerA)
        print(userAnswerB)
        print(userAnswerC)
        print(userAnswerD)"""
        print("Respuesta del usuario: "+ selectedAnswer)

        ### LO SIGUIENTE ES LA INSERT SQL. Si dejamos solo user_id y modality_id hace bien la insert. En cambio con el resto no hace bien la insert.

        # Obtienes el objeto cursor:
        cursor = connection.cursor()
        # Preparas la consulta SQL para luego reemplazar los datos que desees insertar:
        query = '''INSERT INTO testapp_useranswers (user_id, modality_id, "numberQuestion", "correctAnswerCounterSameQuestion", "wrongAnswerCounterSameQuestion") VALUES (%s,%s,%s,%s,%s)'''
        # Ejecutas la query. Aquí reemplazamos la variable que necesitamos para nuestro INSERT en forma de lista
        cursor.execute(query, [userAnswer, modalityPost, numberQuestion, ansOK, ansWrong])
        print("Insert completo")



        #respuestas = UserAnswers.objects.all()
        #print(respuestas)

    else:

        print("No es post")
        
    return(redirect(reverse('test_app:test'),questionModality='celador'))





"""
    from django.db import connection,transaction
    cursor = connection.cursor()
    
    query = ''' INSERT INTO table_name 
            (var1,var2,var3) 
            VALUES (%s,%s,%s) '''
    
    query_list = build_query_list() 
    
    # here build_query_list() represents some function to populate
    # the list with multiple records
    # in the tuple format (value1, value2, value3).
    
    
    cursor.executemany(query, query_list)
    
    transaction.commit()
"""








"""def nextQuestion(request):
    data = {
        'title':'Preguntas',
        'categoría':'Historia'
    }
    return render(request,'prueba.html',{'datos' : data})"""


"""def testFilterByModalityAndByUser(request, questionModality):
    model = Test
    msg='Estás en la modalidad ' + questionModality
    test = Test.objects.all().filter(nameModality__name=questionModality).order_by('number')[:10]
    print(test[0].question)
    if request.user.is_authenticated:
        username = request.user.username
        print(username)
    msg='Estás en la modalidad ' + questionModality + ' usuario ' + username
    messages.success(request, msg, test)
    return redirect(reverse_lazy('test_app:test'),args=(test))"""

"""def test_list(request):
    data = {
        'title':'Los 50 mejores test',
        'categoria':'Auxiliar administrativo'
    }
    return render(request,'prueba.html',data)"""


"""class UserAnswersView(CreateView):
    #model = UserAnswers
    template_name = 'prueba.html'
    form_class = UserAnswerForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_initial(self, *args, **kwargs):
        initial = super(UserAnswersView, self).get_initial(**kwargs)
        initial['title'] = 'My Title'
        return initial

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(UserAnswersView, self).get_form_kwargs(*args, **kwargs)
        kwargs['user'] = self.request.user
        return kwargs"""


class testFilterByModalityAndByUserView(ListView):
    model = TestQuestion
    template_name = 'test/question.html'

    def get_queryset(self):
        questionMod = self.kwargs['questionModality']
        username = None
        """if request.user.is_authenticated():
            username = request.user.username
            print(username)"""
                
        print(questionMod)
        print(questionMod)
        print(questionMod)
        print(questionMod)

        #name = self.request.GET.get('kword', '')
        if questionMod:
            object_list = TestQuestion.objects.all().filter(nameModality__name=questionMod).order_by('number')[:1]
        else:
            object_list = TestQuestion.objects.all()
        return object_list
    login_url = reverse_lazy('test_app:test')


    #Aquí se tiene que retornar desde el formulario: Letra seleccionada, Modalidad de preguntas, Nºpregunta y Usuario.
    def post(self, request):
        if request.method == 'POST':
            
            """if request.user.is_authenticated:
                username = request.user.username
                print(username)"""
            # create a form instance and populate it with data from the request:
            #form = NameForm(request.POST)

            """user= request.POST.get('userId')
            testModality = request.POST.get('testModality')
            numberTest = request.POST.get('numberTest')
            answerLetter = request.POST.get('answerLetter')
            answerOk= request.POST.get('answerOk')"""
            
        
            # check whether it's valid:
            if form.is_valid():
                pass
                # process the data in form.cleaned_data as required
                # ...
                # redirect to a new URL:
                return HttpResponseRedirect('/thanks/')


"""def SeleccionarPregunta():
    user = #tomar el usuario por authenticated
    modalidad = #tomar la modalidad desde la url que está como argumento
    sql = #Consulta SQL de las 10 preguntas según usuario y modalidad (Esto lo implementa Iñaki)
    #Pasar los valores a object_list (o como se llame)
    #Ir a template llevando elo object list


def GuardarPreguntaPost():
    user = #tomar el usuario por authenticated
    modalidad = #tomar la modalidad desde la url que está como argumento
    sql = #Consulta SQL para guardar los datos que han venido por POST. (Esto lo implementa Iñaki)
    SeleccionarPregunta():"""


"""def testFilterByModalityAndByUser(request, questionModality):
    model = Test
    msg='Estás en la modalidad ' + questionModality

    test = Test.objects.all().filter(nameModality__name=questionModality)
    print(test)

    if request.user.is_authenticated:
        username = request.user.username
        print(username)
    
    messages.success(request, msg)
    return redirect(reverse_lazy('test_app:test'))"""



"""class InstallationGalleryListView(ListView):
    model = ImageInstallation
    template_name = 'installation/gallery_installation.html'
    def get_queryset(self):
        name = self.kwargs['pk']
        if name:
            object_list = self.model.objects.all().filter(installation__id = name)
        #else:
        #    object_list = self.model.objects.all().order_by('id')
        return object_list"""