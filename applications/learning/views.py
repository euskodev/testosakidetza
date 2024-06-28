from django.shortcuts import render
from django.views.generic import TemplateView, ListView, FormView
from .models import Test, UserAnswer
from django.http import HttpResponse
from django.template import Template
# Create your views here.

class NextQuestionView(TemplateView):
    template_name = "home/preguntas.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user']=self.request.user
        context['categoria'] = self.kwargs['category']
        context['test'] = Test.objects.first()
        return context

    def post(self, request, *args, **kwargs):
        answer_dePosta = request.POST.get('answer','')  # Obtener el valor del campo 'opciones'
        # Aquí puedes procesar la opción seleccionada como lo necesites
        category_dePost = request.POST.get('category', '')
        number_dePost = request.POST.get('number', '')
        user=self.request.user
        print(answer_dePosta, category_dePost, number_dePost, user)

        form = UserAnswer()
        form.user=self.request.user
        form.test=1
        form.save()

        context2 = super().get_context_data(**kwargs)
        context2['categoria'] = self.kwargs['category']
        number = int(number_dePost) + 1
        context2['test'] = Test.objects.filter(number=number)
        print(context2['test'])
        print(context2)
        return render(request, 'home/preguntas.html', context2)



"""class NextQuestionView(FormView):
    template_name = 'pregunta.html'
    form_class = TestForm
    success_url = reverse_lazy('resultado_final')  # Redirige aquí después de responder todas las preguntas

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        pregunta_id = self.kwargs['pregunta_id']
        pregunta = get_object_or_404(Test, pk=pregunta_id)
        kwargs['instance'] = pregunta
        return kwargs

    def form_valid(self, form):
        # Procesa la respuesta del usuario
        respuesta_usuario = form.cleaned_data['respuesta_correcta']
        # Puedes realizar validaciones adicionales aquí si es necesario
        # Redirige a la siguiente pregunta si existe, o al resultado final si no hay más preguntas
        siguiente_pregunta_id = self.kwargs['pregunta_id'] + 1
        try:
            siguiente_pregunta = Test.objects.get(pk=siguiente_pregunta_id)
            return render(self.request, 'pregunta.html', {'form': self.form_class(instance=siguiente_pregunta)})
        except Test.DoesNotExist:
            return render(self.request, 'fin_test.html')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pregunta_id = self.kwargs['pregunta_id']
        pregunta = get_object_or_404(Test, pk=pregunta_id)
        context['pregunta'] = pregunta
        return context"""