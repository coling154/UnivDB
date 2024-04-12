from django.db import models

# Create your models here.
class Instructor(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32)
    dept_name = models.CharField(max_length=32)
    salary = models.DecimalField(max_digits=8, decimal_places=0)

    def __str__(self):
        return self.name