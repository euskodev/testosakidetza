from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class Modality(models.Model):
    name=models.CharField('Modalidad',max_length=100, null=True,blank=True)

    class Meta:
        verbose_name = 'Modalidad'
        verbose_name_plural = 'Modalidades'
        ordering = ['name']
    
    def __str__(self):
        return self.name

class TestQuestion(models.Model):
    ANSWER=(('1','A'),('2','B'),('3','C'),('4','D'))
    number=models.IntegerField('Nº',null=True,blank=True)
    question=models.TextField('Pregunta',null=True,blank=True)
    a=models.TextField('A',null=True,blank=True)
    b=models.TextField('B',null=True,blank=True)
    c=models.TextField('C',null=True,blank=True)
    d=models.TextField('D',null=True,blank=True)
    answer=models.CharField('Respuesta',max_length=1,choices=ANSWER, null=True, blank=True)
    nameModality=models.ForeignKey(Modality,on_delete=models.CASCADE,null=True,blank=True)
    observations=models.TextField('Observaciones',null=True,blank=True)

    class Meta:
        verbose_name = 'Test'
        verbose_name_plural = 'Test'
        ordering = ['number']

    def __str__(self):
        return str(self.number)


class UserAnswers(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    modality = models.ForeignKey(Modality,on_delete=models.CASCADE,null=True,blank=True)
    numberQuestion = models.IntegerField('Número pregunta',null=True,blank=True)
    correctAnswerCounterSameQuestion=models.IntegerField('Veces que se ha respondido una pregunta correctamente',null=True,blank=True)
    wrongAnswerCounterSameQuestion=models.IntegerField('Veces que se ha respondido una pregunta incorrectamente',null=True,blank=True)

    class Meta:
        verbose_name = 'Respuesta de usuario'
        verbose_name_plural = 'Respuestas de usuarios'
        ordering = ['numberQuestion']

    def __str__(self):
        return str(self.numberQuestion)

    def get_absolute_url(self):
        return reverse('test_app:test-hacertest', args=[self.user])

class TestCounter(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    modality = models.ForeignKey(Modality,on_delete=models.CASCADE,null=True,blank=True)
    counter = models.IntegerField('Contador',null=True,blank=True)
    listQuestionsNumbers = models.TextField('Array números preguntas',null=True,blank=True)
    completed = models.BooleanField('Completado',null=True,blank=True, default=False)

    class Meta:
        verbose_name = 'Contador de preguntas'
        verbose_name_plural = 'Contadores de preguntas'
        ordering = ['user','modality']
    
    def __str__(self):
        return str(self.counter)





