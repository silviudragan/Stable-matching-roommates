from django.db import models


class Student(models.Model):
    nume = models.CharField(max_length=50)
    prenume = models.CharField(max_length=50)
    numar_matricol = models.CharField(max_length=30)
    an = models.IntegerField()
    grupa = models.CharField(max_length=5)
    sex = models.CharField(max_length=5)
    poza_profil = models.FileField(default='1')
    email = models.CharField(max_length=50, default="")
    cod_reset_parola = models.CharField(max_length=8, default="")

    def __str__(self):
        return self.numar_matricol + ' - ' + self.nume + ' ' + self.prenume


class Recenzie(models.Model):
    from_uid = models.CharField(max_length=30)
    to_uid = models.CharField(max_length=30)
    mesaj = models.CharField(max_length=600)
    calificativ = models.IntegerField(default=1)
    data = models.DateField(u"Conversation Date", auto_now_add=True, blank=True)

    def __str__(self):
        return self.from_uid + ' to ' + self.to_uid


class Coleg(models.Model):
    # coleg1 si coleg2 au stat sau inca stau in aceeasi camera
    coleg1 = models.CharField(max_length=30)
    coleg2 = models.CharField(max_length=30)

    def __str__(self):
        return self.coleg1 + ' with ' +self.coleg2
