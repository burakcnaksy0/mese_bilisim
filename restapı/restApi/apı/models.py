from django.db import models

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=50)
    page_number = models.IntegerField()
    published_date = models.DateField()
    stock_number = models.IntegerField()

