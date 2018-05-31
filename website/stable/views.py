import operator
import random
import string

import MySQLdb
import datetime

from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator
from django.db.backends import mysql
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect

from .forms import UserForm, LoginForm
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from . models import Student, Recenzie, Coleg, Repartizare, Preferinta, Camin, MultimeStabila, Anunt

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
        succes_email = request.GET.get('p', None)
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form, 'succes_email': succes_email})

    def post(self, request):
        global username
        username = request.POST.get('nr_matricol', None)
        password = request.POST.get('parola', None)
        emailRecParola = request.POST.get('emailRecParola', None)
        if emailRecParola is None:
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                if username == "admin":
                    return redirect('administrator')
                return redirect('index')
            else:
                return render(request, 'stable/login.html')
        else:
            global email
            email = emailRecParola
            # if "@info.uaic.ro" not in email: ##################################################
            if "@yahoo.com" not in email and "gmail" not in email:
                mesaj = "Emailul introdus nu este falid sau nu apartine domeniului facultatii."
                return render(request, 'stable/login.html', {'mesaj_email': mesaj})
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

    def verificare_introducere_preferinte(self):
        data = Preferinta.objects.filter(numar_matricol=username)
        if len(data) == 0:
            return False
        else:
            return True

    template_name = 'stable/profil.html'

    def incarcare_preferinte(self):
        c = conn.cursor()
        c.execute("SELECT * from stable_repartizare where numar_matricol=%s", [username])
        data = c.fetchall()
        nume_camin = ""
        colegi_camin = []
        if len(data) == 0:
            warning = "Din nefericire nu aveti loc in camin"
        else:
            c.execute("SELECT s.nume, s.prenume from stable_student s "
                      "join stable_repartizare r on r.numar_matricol = s.numar_matricol "
                      "where r.camin=%s and s.numar_matricol!=%s", [data[0][2], username])
            nume_camin = data[0][2]
            data = c.fetchall()
            for it in data:
                colegi_camin.append(it[0] + ' ' + it[1])
        c.close()
        return colegi_camin, nume_camin

    def colegi_repartizati(self, nume_camin):
        camere_repartizate = Camin.objects.filter(nume_camin=nume_camin)
        numar_camere = []
        for item in camere_repartizate:
            numar_camere.append(item.numar_camera)

        uid_colegii_repartizati = []
        numar_camera = 0
        for nr in numar_camere:
            camera = MultimeStabila.objects.filter(camera=Camin.objects.get(numar_camera=nr))
            studenti_camera = []
            if len(camera) > 0:
                for item in camera:
                    studenti_camera.append(item.coleg1)
                    studenti_camera.append(item.coleg2)
                    studenti_camera.append(item.coleg3)
                    studenti_camera.append(item.coleg4)
                    studenti_camera.append(item.coleg5)
                if username in studenti_camera:
                    numar_camera = nr
                    for item in studenti_camera:
                        if len(item) > 0 and item != username:
                            uid_colegii_repartizati.append(item)

        colegii_repartizati = []
        an_studiu = []
        grupa = []
        for uid in uid_colegii_repartizati:
            student = Student.objects.get(numar_matricol=uid)
            colegii_repartizati.append(student.nume + ' ' + student.prenume)
        return colegii_repartizati, numar_camera

    def mesaje_admin(self):
        today = datetime.date.today()
        anunturi = Anunt.objects.all()
        anunturi_de_afisat = []
        for item in anunturi:
            if today <= item.deadline:
                anunturi_de_afisat.append((item.titlu, item.mesaj, item.deadline))
        anunturi_de_afisat.sort(key=operator.itemgetter(2), reverse=True)
        return anunturi_de_afisat

    def get(self, request):
        if len(username) == 0:
            return redirect('login')

        student = Student.objects.get(numar_matricol=username)
        colegi_camin, nume_camin = self.incarcare_preferinte()
        introdus_preferinte = False

        colegii_repartizati, numar_camera = self.colegi_repartizati(nume_camin)

        if self.verificare_introducere_preferinte():
            introdus_preferinte = True

        anunturi = self.mesaje_admin()
        print(anunturi)
        return render(request, self.template_name, {'student': student, 'colegi_camin': colegi_camin, 'nume_camin': nume_camin,
                                                    'introdus_preferinte': introdus_preferinte, 'colegii_repartizati': colegii_repartizati,
                                                    'numar_camera': numar_camera, 'anunturi': anunturi})

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
        colegi_camin, nume_camin = self.incarcare_preferinte()
        introdus_preferinte = False
        if self.verificare_introducere_preferinte():
            introdus_preferinte = True
        return render(request, self.template_name, {'student': student, 'colegi_camin': colegi_camin, 'nume_camin': nume_camin,
                                                    'introdus_preferinte': introdus_preferinte})


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


ITEMS_ON_PAGE = 3


class Recenzii(View):
    template_name = 'stable/recenzie.html'

    def get(self, request):
        page = request.GET.get('page', 1)
        if len(username) == 0:
            return redirect('login')

        student = Student.objects.get(numar_matricol=username)
        recenzii = obtine_recenzii()
        p = Paginator(recenzii, ITEMS_ON_PAGE)
        colegi = colegii_de_camera()
        return render(request, self.template_name, {'student': student, 'recenzii': p.page(page), 'colegi': colegi,
                                                    'nr_matricol': username})

    def post(self, request):
        page = request.GET.get('page', 1)
        nume_coleg = request.POST.get('numeColeg', '')
        calificativ = request.POST.get('notaColeg', '')
        mesaj = request.POST.get('mesajColeg', '')
        # revizuit split-ul pentru diferite forme de nume
        data = nume_coleg.split()

        if nume_coleg == '':
            student = Student.objects.get(numar_matricol=username)
            recenzii = obtine_recenzii()
            colegi = colegii_de_camera()
            p = Paginator(recenzii, ITEMS_ON_PAGE)
            warning = "Nu a fost selectat nici un nume pentru recenzie"
            return render(request, self.template_name, {'student': student, 'recenzii': p.page(page), 'colegi': colegi,
                                                        'warning': warning, "nr_matricol": username})
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
            p = Paginator(recenzii, ITEMS_ON_PAGE)
            return render(request, self.template_name, {'student': student, 'recenzii': p.page(page), 'colegi': colegi,
                                                        'warning': warning, "nr_matricol": username})

        c.execute("SELECT numar_matricol from stable_student where nume=%s and prenume=%s", [nume, prenume])
        nr_matricol = c.fetchone()
        c.execute("INSERT into stable_recenzie(from_uid, to_uid, mesaj, calificativ, data) "
                  "VALUES(%s, %s, %s, %s, %s)", [username, nr_matricol, mesaj, calificativ, datetime.date.today()])
        conn.commit()
        c.close()
        recenzii = obtine_recenzii()
        succes = "Recenzia pentru " + nume + " " + prenume + " a fost adaugata."
        p = Paginator(recenzii, ITEMS_ON_PAGE)
        return render(request, self.template_name, {'student': student, 'recenzii': p.page(page), 'colegi': colegi,
                                                    'succes': succes, "nr_matricol": username})


def aflare_nr_matricol(nume):
    data = nume.split()
    prenume = data[1:]
    nume = data[0]
    c = conn.cursor()
    c.execute("SELECT numar_matricol from stable_student where nume=%s and prenume=%s", [nume, prenume])
    data = c.fetchone()
    c.close()
    return data


###############################################################################################################
######################################## Functii pentru apelurile AJAX ########################################
###############################################################################################################


def display_info_coleg(request):
    coleg = request.GET.get('numeColeg', None)
    nume = coleg.split()
    c = conn.cursor()
    c.execute("SELECT * from stable_student where nume=%s and prenume=%s", [nume[0], nume[1]])
    rez = c.fetchone()
    nr_matricol = rez[2]
    c.close()
    print(rez)
    data = {
        'Nume:': rez[0],
        'Prenume:': rez[1],
        'An:': rez[3],
        'Grupa:': rez[4],
        'Poza:': rez[6],
    }
    if data['Poza:'] == "1":
        if rez[5] == "M":
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


def preferinte_student(request):
    nume_preferinte = request.GET.get('nume_preferinte', None)
    lista_preferinte = nume_preferinte.split('+')[:-1]
    c = conn.cursor()
    importanta = 1
    for item in lista_preferinte:
        nr_matricol = aflare_nr_matricol(item)
        c.execute('INSERT into stable_preferinta (numar_matricol, uid_preferinta, importanta) values (%s, %s, %s)',
                  [username, nr_matricol, importanta])
        importanta += 1
    conn.commit()
    c.close()
    return JsonResponse({})


###############################################################################################################
###############################################################################################################
###############################################################################################################


def trimite_email(destinatar, cod_verificare):
    # implementare care a functionat pentru o perioada de timp, iar dupa din motive necunoscute nu a mai functionat
    """
    import smtplib
    gmail_user = "stablematchingroommates@gmail.com"
    gmail_pwd = "StableRommates135680"
    SUBJECT = "Resetare parola"
    TEXT = "Foloseste codul urmator pentru resetarea parolei: " + cod_verificare + "."
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()

    server = smtplib.SMTP_SSL('smtp.googlemail.com', 465)

    server.login(gmail_user, gmail_pwd)
    BODY = '\r\n'.join(['To: %s' % destinatar,
                        'From: %s' % gmail_user,
                        'Subject: %s' % SUBJECT,
                        '', TEXT])

    server.sendmail(gmail_user, destinatar, BODY)
    """

    import smtplib
    fromaddr = 'stablematchingroommates@gmail.com'
    toaddrs = destinatar
    msg = "Foloseste codul urmator pentru resetarea parolei: " + cod_verificare + "."
    username = 'stablematchingroommates@gmail.com'
    password = 'StableRommates135680'
    SUBJECT = "Resetare parola"

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    BODY = '\r\n'.join(['To: %s' % destinatar,
                        'From: %s' % fromaddr,
                        'Subject: %s' % SUBJECT,
                        '', msg])
    server.starttls()
    server.login(username, password)
    server.sendmail(fromaddr, toaddrs, BODY)
    server.quit()
    print('email sent')


def id_generator(size=7, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class ResetPass(View):
    template_name = 'stable/resetPass.html'

    def get(self, request):
        cod_verificare = id_generator()
        c = conn.cursor()

        c.execute("UPDATE stable_student set cod_reset_parola=%s", [cod_verificare])
        conn.commit()
        c.close()

        trimite_email(email, cod_verificare)
        return render(request, self.template_name, {'email': email})

    def post(self, request):
        codVerificare = request.POST.get('codVerificare', '')
        password = request.POST.get('password', '')
        re_password = request.POST.get('re_password', '')

        c = conn.cursor()
        c.execute("SELECT cod_reset_parola, numar_matricol from stable_student where email=%s", [email])
        cod_valid, username = c.fetchone()

        if codVerificare == cod_valid:
            if password == re_password:
                user = User.objects.get(username=username)
                user.set_password(password)
                user.save()
                c.execute("UPDATE stable_student set cod_reset_parola=''")
                conn.commit()
                mesaj = "succes"
                return redirect('/login/?p=%s' % mesaj)
                # return redirect('login')
                # return render(request, 'stable/login.html', {'mesaj_reset': mesaj})

            mesaj = "Parolele nu se potrivesc"
            return render(request, 'stable/resetPass.html', {'mesaj_reset': mesaj})

        c.close()
        mesaj = "Codul de verificare nu este valid"
        return render(request, 'stable/resetPass.html', {'mesaj_reset': mesaj})
