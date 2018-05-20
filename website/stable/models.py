from django.db import models

CAMINE = (
        ('C1', 'Cămin C1'),
        ('C2', 'Cămin C2'),
        ('C3', 'Cămin C3'),
        ('C4', 'Cămin C4'),
        ('C5', 'Cămin C5'),
        ('C6', 'Cămin C6'),
        ('C7', 'Cămin C7'),
        ('C8', 'Cămin C8'),
        ('C10', 'Cămin C10'),
        ('C11', 'Cămin C11'),
        ('C12', 'Cămin C12'),
        ('C13', 'Cămin C13'),
        ('Gaudeamus', 'Hotelul studenţesc Gaudeamus'),
        ('Akademos', 'Hotelul studenţesc Akademos'),
        ('Buna Vestire', 'Cămin „Buna Vestire"'),
    )

FACULTATI = (
        ('Biologie', 'Biologie'),
        ('Chimie', 'Chimie'),
        ('Drept', 'Drept'),
        ('Economie si Administrarea Afacerilor', 'Economie și Administrarea Afacerilor'),
        ('Educatie fizica si Sport', 'Educație fizică și Sport'),
        ('Filosofie si Stiinte Social-Politice', 'Filosofie și Științe Social-Politice'),
        ('Fizica', 'Fizică'),
        ('Geografie si Geologie', 'Geografie și Geologie'),
        ('Informatica', 'Informatică'),
        ('Istorie', 'Istorie'),
        ('Litere', 'Litere'),
        ('Matematica', 'Matematică'),
        ('Psihologie si Stiinte ale Educatiei', 'Psihologie și Științe ale Educației'),
        ('Teologie Ortodoxa', 'Teologie Ortodoxă'),
        ('Teologie Romano-Catolica', 'Teologie Romano-Catolică'),
    )


class Student(models.Model):
    nume = models.CharField(max_length=50)
    prenume = models.CharField(max_length=50)
    numar_matricol = models.CharField(max_length=30, primary_key=True)
    facultate = models.CharField(max_length=40, choices=FACULTATI)
    an = models.IntegerField()
    grupa = models.CharField(max_length=5)
    sex = models.CharField(max_length=5)
    poza_profil = models.FileField(default='1')
    email = models.CharField(max_length=50, default="")
    cod_reset_parola = models.CharField(max_length=8, default="", blank=True)

    def __str__(self):
        return self.numar_matricol + ' - ' + self.nume + ' ' + self.prenume


class Recenzie(models.Model):
    class Meta:
        unique_together = (('from_uid', 'to_uid'),)

    from_uid = models.CharField(max_length=30)
    to_uid = models.CharField(max_length=30)
    mesaj = models.CharField(max_length=600)
    calificativ = models.IntegerField(default=1)
    data = models.DateField(u"Conversation Date", auto_now_add=True, blank=True)

    def __str__(self):
        return self.from_uid + ' catre ' + self.to_uid


class Coleg(models.Model):
    # coleg1 si coleg2 au stat sau inca stau in aceeasi camera
    class Meta:
        unique_together = (('coleg1', 'coleg2'),)

    coleg1 = models.CharField(max_length=30)
    coleg2 = models.CharField(max_length=30)

    def __str__(self):
        return self.coleg1 + ' cu ' +self.coleg2


class Repartizare(models.Model):
    class Meta:
        unique_together = (('numar_matricol', 'camin'),)

    numar_matricol = models.CharField(max_length=30)
    camin = models.CharField(max_length=30, choices=CAMINE)
    repartizare_camera = models.BooleanField(default=False)

    def __str__(self):
        return self.numar_matricol + ' in ' + self.camin


class Preferinta(models.Model):
    class Meta:
        unique_together = (('numar_matricol', 'uid_preferinta'),)

    numar_matricol = models.CharField(max_length=30)
    uid_preferinta = models.CharField(max_length=30)
    importanta = models.IntegerField()

    def __str__(self):
        return self.numar_matricol + ' -> ' + self.uid_preferinta


class Camin(models.Model):
    class Meta:
        unique_together = (('nume_camin', 'numar_camera'),)

    nume_camin = models.CharField(max_length=30, choices=CAMINE)
    numar_camera = models.IntegerField()
    facultate = models.CharField(max_length=40, choices=FACULTATI, blank=True)
    locuri = models.IntegerField()

    def __str__(self):
        return self.facultate + ': ' + self.nume_camin + ' - ' + str(self.numar_camera)


class MultimeStabila(models.Model):
    camera = models.OneToOneField(Camin, primary_key=True)
    coleg1 = models.CharField(max_length=30)
    coleg2 = models.CharField(max_length=30, blank=True)
    coleg3 = models.CharField(max_length=30, blank=True)
    coleg4 = models.CharField(max_length=30, blank=True)
    coleg5 = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.camera.nume_camin + '/' + str(self.camera.numar_camera) + ': ' + self.coleg1 + ' - ' + self.coleg2 + ' - ' + self.coleg3 + ' - ' + self.coleg4 + ' - ' + self.coleg5