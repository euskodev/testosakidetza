from django.db import models

# Create your models here


"""class Test(models.Model):
    number = models.OneToOneField(User, on_delete=models.CASCADE)
    category = models.TextField(blank=True, null=True)
    question = models.DateField(blank=True, null=True)
    aAnswer = models.CharField(max_length=30, blank=True, null=True)
    aAnswer = models.CharField(max_length=30, blank=True, null=True)
    aAnswer = models.CharField(max_length=30, blank=True, null=True)
    aAnswer = models.CharField(max_length=30, blank=True, null=True)
    correctAnswer = models.CharField(max_length=30, blank=True, null=True)
    
    def __str__(self):
        return self.user.username"""