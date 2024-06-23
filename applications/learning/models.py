from django.db import models

# Create your models here


class Category(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    def __str__(self):
        return self.name

class Test(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    number = models.IntegerField(blank=True, null=True)
    question = models.TextField(max_length=500, blank=True, null=True)
    aAnswer = models.CharField(max_length=350, blank=True, null=True)
    bAnswer = models.CharField(max_length=350, blank=True, null=True)
    cAnswer = models.CharField(max_length=350, blank=True, null=True)
    dAnswer = models.CharField(max_length=350, blank=True, null=True)
    correctAnswer = models.CharField(max_length=5, blank=True, null=True)
    
    def __str__(self):
        return self.question

