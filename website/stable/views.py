import MySQLdb
import datetime
from django.core.files.storage import FileSystemStorage
from django.db.backends import mysql
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import UserForm, LoginForm
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from .models import Student, Recenzie

username = ""
email = ""
conn = MySQLdb.connect(host="localhost",
                       user="root",
                       passwd="Silviu01",
                       db="test")


def index(request):
    return render(request, 'stable/index.html')


class Login(View):
    form_class = LoginForm
    template_name = 'stable/login.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        global username
        username = request.POST.get('nr_matricol', None)
        password = request.POST.get('parola', None)
        emailRecParola = request.POST.get('emailRecParola', None)
        if emailRecParola is None:
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                return render(request, 'stable/login.html')
        else:
            global email
            email = emailRecParola
            return redirect('resetPass')


class UserFormView(View):
    form_class = UserForm
    template_name = 'stable/register.html'
    global conn

    def get(self, request):
        form = self.form_class(None)
        studenti = ""
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserForm(request.POST)
        re_password = request.POST.get('re_password', '')
        if form.is_valid():
            global username
            user = form.save(commit=False)

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            if password != re_password:
                return render(request, self.template_name, {'form': form})

            c = conn.cursor()
            c.execute("SELECT * FROM stable_student")
            studenti = c.fetchall()
            # verificam daca numarul matricol este valid
            id_valid = False
            for student in studenti:
                if username in student:
                    id_valid = True

            if not id_valid:
                return render(request, self.template_name, {'form': form, 'mesaj': "Numarul matricol nu este valid."})

            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('index')
        return render(request, self.template_name, {'form': form})


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('login')


class Profil(View):
    template_name = 'stable/profil.html'

    def get(self, request):

        try:
            student = Student.objects.get(numar_matricol=username)
        except Exception:
            return render(request, self.template_name)
        return render(request, self.template_name, {'student': student})

    def post(self, request):
        c = conn.cursor()
        try:
            poza_profil = request.FILES['poza_profil']
            fs = FileSystemStorage()
            fs.save(poza_profil.name, poza_profil)
            c.execute("UPDATE stable_student set poza_profil=%s where numar_matricol=%s", [poza_profil, username])
            conn.commit()
        except Exception:
            pass  # nu a fost incarcat nimic
        student = Student.objects.get(numar_matricol=username)
        return render(request, self.template_name, {'student': student})


# o lista cu colegii de camera cu care a stat sau inca sta studentul cu respectivul numar matricol
def colegii_de_camera():
    c = conn.cursor()
    c.execute("SELECT * from stable_coleg where coleg1=%s or coleg2=%s", [username, username])
    data = c.fetchall()
    nr_matricol_colegi = []
    for coleg in data:
        if coleg[1] == username:
            nr_matricol_colegi.append(coleg[2])
        else:
            nr_matricol_colegi.append(coleg[1])
    colegi = []
    for coleg in nr_matricol_colegi:
        c.execute("SELECT nume, prenume FROM stable_student where numar_matricol=%s", [coleg])
        data = c.fetchone()
        nume = data[0] + ' ' + data[1]
        colegi.append(nume)
    c.close()
    return colegi


def obtine_recenzii():
    recenzii = []
    c = conn.cursor()
    c.execute("SELECT * FROM stable_recenzie order by data desc")
    for recenzie in c.fetchall():
        recenzii.append(list(recenzie))
    for i in range(0, len(recenzii)):
        # aflam numele expeditorului
        c.execute("SELECT prenume, nume FROM stable_student where numar_matricol=%s", [recenzii[i][1]])
        nume = c.fetchone()
        recenzii[i][1] = nume[0] + ' ' + nume[1]

        # aflam numele destinatarului
        c.execute("SELECT prenume, nume FROM stable_student where numar_matricol=%s", [recenzii[i][2]])
        nume = c.fetchone()
        recenzii[i][2] = nume[0] + ' ' + nume[1]
    c.close()
    return recenzii


class Recenzii(View):
    template_name = 'stable/recenzie.html'

    def get(self, request):
        student = Student.objects.get(numar_matricol=username)
        recenzii = obtine_recenzii()
        colegi = colegii_de_camera()
        return render(request, self.template_name, {'student': student, 'recenzii': recenzii, 'colegi': colegi,
                                                    'nr_matricol': username})

    def post(self, request):
        nume_coleg = request.POST.get('numeColeg', '')
        calificativ = request.POST.get('notaColeg', '')
        mesaj = request.POST.get('mesajColeg', '')
        # revizuit split-ul pentru diferite forme de nume
        data = nume_coleg.split()
        nume = data[0]
        prenume = data[1]
        c = conn.cursor()

        c.execute("SELECT numar_matricol from stable_student where nume=%s and prenume=%s", [nume, prenume])
        nr_matricol = c.fetchone()

        colegi = colegii_de_camera()
        student = Student.objects.get(numar_matricol=username)
        c.execute("SELECT * from stable_recenzie where from_uid=%s and to_uid=%s", [username, nr_matricol])
        data = c.fetchone()

        if data:
            recenzii = obtine_recenzii()
            warning = "Exista deja o recenzie facuta pentru " + nume + " " + prenume
            return render(request, self.template_name, {'student': student, 'recenzii': recenzii, 'colegi': colegi,
                                                        'warning': warning, "nr_matricol": username})

        c.execute("SELECT numar_matricol from stable_student where nume=%s and prenume=%s", [nume, prenume])
        nr_matricol = c.fetchone()
        c.execute("INSERT into stable_recenzie(from_uid, to_uid, mesaj, calificativ, data) "
                  "VALUES(%s, %s, %s, %s, %s)", [username, nr_matricol, mesaj, calificativ, datetime.date.today()])
        conn.commit()
        c.close()
        recenzii = obtine_recenzii()
        succes = "Recenzia pentru " + nume + " " + prenume + " a fost adaugata."
        return render(request, self.template_name, {'student': student, 'recenzii': recenzii, 'colegi': colegi,
                                                    'succes': succes, "nr_matricol": username})


###############################################################################################################
######################################## Functii pentru apelurile AJAX ########################################
###############################################################################################################

def display_info_coleg(request):
    coleg = request.GET.get('numeColeg', None)
    nume = coleg.split()
    c = conn.cursor()
    c.execute("SELECT * from stable_student where nume=%s and prenume=%s", [nume[0], nume[1]])
    rez = c.fetchone()
    nr_matricol = rez[3]
    c.close()
    data = {
        'Nume:': rez[1],
        'Prenume:': rez[2],
        'An:': rez[4],
        'Grupa:': rez[5],
        'Poza:': rez[7],
    }
    if data['Poza:'] == "1":
        if rez[6] == "M":
            data['Poza:'] = "3.png"
        else:
            data['Poza:'] = "4.jpg"
    return JsonResponse(data)


def recenzii_facute(request):
    nr_matricol = request.GET.get('nr_matricol', None)

    recenzii = []
    c = conn.cursor()

    c.execute("SELECT * FROM stable_recenzie where from_uid=%s order by data desc", [nr_matricol])
    for recenzie in c.fetchall():
        recenzii.append(list(recenzie))
    for i in range(0, len(recenzii)):
        # aflam numele expeditorului
        c.execute("SELECT prenume, nume FROM stable_student where numar_matricol=%s", [recenzii[i][1]])
        nume = c.fetchone()
        recenzii[i][1] = nume[0] + ' ' + nume[1]

        # aflam numele destinatarului
        c.execute("SELECT prenume, nume FROM stable_student where numar_matricol=%s", [recenzii[i][2]])
        nume = c.fetchone()
        recenzii[i][2] = nume[0] + ' ' + nume[1]
    c.close()

    data = {}
    it = 0
    for rec in recenzii:
        for i in rec:
            eticheta = 'info' + str(it)
            it += 1
            data[eticheta] = i
    return JsonResponse(data)


def recenzii_primite(request):
    nr_matricol = request.GET.get('nr_matricol', None)

    recenzii = []
    c = conn.cursor()

    c.execute("SELECT * FROM stable_recenzie where to_uid=%s order by data desc", [nr_matricol])
    for recenzie in c.fetchall():
        recenzii.append(list(recenzie))
    for i in range(0, len(recenzii)):
        # aflam numele expeditorului
        c.execute("SELECT prenume, nume FROM stable_student where numar_matricol=%s", [recenzii[i][1]])
        nume = c.fetchone()
        recenzii[i][1] = nume[0] + ' ' + nume[1]

        # aflam numele destinatarului
        c.execute("SELECT prenume, nume FROM stable_student where numar_matricol=%s", [recenzii[i][2]])
        nume = c.fetchone()
        recenzii[i][2] = nume[0] + ' ' + nume[1]
    c.close()

    data = {}
    it = 0
    for rec in recenzii:
        for i in rec:
            eticheta = 'info' + str(it)
            it += 1
            data[eticheta] = i
    return JsonResponse(data)


def toate_recenziile(request):
    recenzii = []
    c = conn.cursor()

    c.execute("SELECT * FROM stable_recenzie order by data desc")
    for recenzie in c.fetchall():
        recenzii.append(list(recenzie))
    for i in range(0, len(recenzii)):
        # aflam numele expeditorului
        c.execute("SELECT prenume, nume FROM stable_student where numar_matricol=%s", [recenzii[i][1]])
        nume = c.fetchone()
        recenzii[i][1] = nume[0] + ' ' + nume[1]

        # aflam numele destinatarului
        c.execute("SELECT prenume, nume FROM stable_student where numar_matricol=%s", [recenzii[i][2]])
        nume = c.fetchone()
        recenzii[i][2] = nume[0] + ' ' + nume[1]
    c.close()

    data = {}
    it = 0
    for rec in recenzii:
        for i in rec:
            eticheta = 'info' + str(it)
            it += 1
            data[eticheta] = i
    return JsonResponse(data)


class ResetPass(View):
    template_name = 'stable/resetPass.html'

    def get(self, request):
        return render(request, self.template_name, {'email': email})

    def post(self, request):
        pass
