from django.db import models


class Student(models.Model):
    nume = models.CharField(max_length=50)
    prenume = models.CharField(max_length=50)
    numar_matricol = models.CharField(max_length=30)
    an = models.IntegerField()
    grupa = models.CharField(max_length=5)

    def __str__(self):
        return self.nume + ' ' + self.prenume + ' - ' + self.numar_matricol
