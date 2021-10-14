from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class id_Board(models.Model):
    author = models.CharField(max_length=10, null=False)
    keyword = models.CharField(max_length=100, null=False)
    count = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(300)])
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

