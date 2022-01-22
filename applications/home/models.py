from django.db import models

# Create your models here.
class Home(models.Model):
    title=models.CharField('Título',max_length=30,null=True,blank=True)

    class Meta:
        verbose_name = 'Home'
        verbose_name_plural = 'Home'
        ordering = ['title']
    
    def __str__(self):
        return self.title
