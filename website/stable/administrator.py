import copy
import operator
from math import floor, ceil
from pprint import pprint
from random import shuffle, random, randint
from time import sleep

from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
import MySQLdb

from . export import export_repartizare
from . models import Student, Recenzie, Coleg, Repartizare, Preferinta, Camin, MultimeStabila, Anunt

conn = MySQLdb.connect(host="localhost",
                       user="root",
                       passwd="Silviu01",
                       db="test")
students = []
copie_students = []
duplicat_students = []
camine = ['C1', 'C2', 'C13', 'C12']
          # 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C10', 'C11', 'C12', 'Gaudeamus', 'Akademos',
          # 'Buna Vestire']
FACULTATI = [
    'Biologie',
    'Chimie',
    'Drept',
    'Economie si Administrarea Afacerilor',
    'Educatie fizica si Sport',
    'Filosofie si Stiinte Social-Politice',
    'Fizica',
    'Geografie si Geologie',
    'Informatica',
    'Istorie',
    'Litere',
    'Matematica',
    'Psihologie si Stiinte ale Educatiei',
    'Teologie Ortodoxa',
    'Teologie Romano-Catolica', ]

LOCURI = {
    'C1': [2, 3],
    'C2': [2, 3, 4],
    'C3': [2, 3, 4],
    'C4': [5],
    'C5': [2, 3],
    'C6': [5],
    'C7': [5],
    'C8': [5],
    'C10': [5],
    'C11': [2, 3],
    'C12': [5],
    'C13': [5],
    'Gaudeamus': [2, 3],
    'Akademos': [2, 3],
    'Buna Vestire': [2]
}


def lista_studenti(camin, facultate, sex):
    c = conn.cursor()
    c.execute("SELECT * from stable_repartizare r "
              "join stable_student s on s.numar_matricol = r.numar_matricol "
              "where r.repartizare_camera= False and r.camin=%s and s.facultate=%s and s.sex=%s", [camin, facultate, sex])
    data = c.fetchall()
    toti_studentii = []
    for st in data:
        toti_studentii.append(st[1])
    return toti_studentii


def adaugare_coleg_fals(camin, facultate, sex):
    global students
    toti_studentii = lista_studenti(camin, facultate, sex)
    d = dict()
    d['name'] = "empty"
    d['propose'] = ""
    d['accept'] = ""
    shuffle(toti_studentii)
    studenti_preferati = []
    for i in toti_studentii:
        if i is not "empty":
            studenti_preferati.append(i)
    d['preferences'] = studenti_preferati
    students.append(d)


def incarcare_preferinte(camin, facultate, sex):
    del students[:]
    c = conn.cursor()
    toti_studentii = lista_studenti(camin, facultate, sex)
    empty = False
    if len(toti_studentii) % 2 == 1:
        toti_studentii.append("empty")
        empty = True
    c.execute("SELECT * from stable_repartizare r "
              "join stable_student s on s.numar_matricol = r.numar_matricol "
              "where r.camin=%s and s.facultate=%s and r.repartizare_camera=%s and s.sex=%s", [camin, facultate, False, sex])
    data = c.fetchall()

    studenti_eligibili = []
    for st in data:
        studenti_eligibili.append(st[1])
    if len(data) == 0:
        return -1
    for st in data:
        d = dict()
        numar_matricol = st[1]
        d['name'] = numar_matricol
        d['propose'] = ""
        d['accept'] = ""

        c.execute("SELECT * from stable_preferinta p "
                  "join stable_repartizare r on r.numar_matricol = p.numar_matricol "
                  "where r.repartizare_camera=False and p.numar_matricol=%s order by importanta", [numar_matricol])
        data_pref = c.fetchall()
        studenti_preferati = []
        for i in data_pref:
            if i[2] in studenti_eligibili:
                studenti_preferati.append(i[2])
        shuffle(toti_studentii)
        for st in toti_studentii:
            if st != numar_matricol and st not in studenti_preferati and st in studenti_eligibili:
                studenti_preferati.append(st)
        d['preferences'] = studenti_preferati
        students.append(d)

    if empty:
        adaugare_coleg_fals(camin, facultate, sex)
        '''
            adaugarea colegului fictiv unde este posibil
        '''
        c = conn.cursor()
        for student in students:
            c.execute("SELECT * from stable_preferinta p "
                      "join stable_repartizare r on r.numar_matricol = p.numar_matricol "
                      "where r.repartizare_camera=False and p.numar_matricol=%s order by importanta", [student['name']])
            data_pref = c.fetchall()
            studenti_preferati = []
            for i in data_pref:
                studenti_preferati.append(i[2])
            shuffle(toti_studentii)
            for st in toti_studentii:
                if st != student['name'] and st not in studenti_preferati:
                    studenti_preferati.append(st)
            student['preferences'] = studenti_preferati
    c.close()
    global copie_students
    copie_students = copy.deepcopy(students)
    global duplicat_students
    duplicat_students = copy.deepcopy(students)
    return 1


def free(multime, option):
    for st in multime:
        if option == st['name']:
            return st['accept']


def propose(multime, searcher, option):
    for st in multime:
        if option == st['name']:
            st['accept'] = searcher
    return multime


def who_is_beter(multime, searcher, option, current):
    for st in multime:
        if option == st['name']:
            for p in st['preferences']:
                if p == searcher:
                    return searcher
                if p == current:
                    return current


def abandon_current_accept(multime, option):
    for st in multime:
        if option == st['name']:
            current_accept = st['accept']
            try:
                st['preferences'].remove(current_accept)
                # print(st)
                # print(current_accept)
            except Exception as error:
                print("4", error)
            for st_rm in multime:
                if st_rm['name'] == current_accept:
                    st_rm['preferences'].remove(option)
                    st_rm['propose'] = ""
    return multime


def exista_in_cheie(punctaje_perechi, nume):
    for item in punctaje_perechi.keys():
        if nume in item:
            return True
    return False


def verificare_tag_empty():
    for st in students:
        if st['name'] == 'empty':
            return True
    return False


def preferintele_in_template(preferinte):
    # crearea listei cu dictionarele fiecarei perechi/single
    del students[:]

    for item in preferinte.keys():
        d = dict()
        d['name'] = item
        d['propose'] = ""
        d['accept'] = ""
        d['preferences'] = preferinte[item]
        students.append(d)


def preferinte_pentru_stable_3(camin, punctaje_perechi, facultate, sex):
    global copie_students
    global duplicat_students
    perechi = []
    single = []
    for item in punctaje_perechi.keys():
        if '+' in item:
            perechi.append(item)
        else:
            single.append(item)

    nr_studenti = len(lista_studenti(camin, facultate, sex))

    # trebuie sa pastram atatea perechi cate camere vor fi, iar pe celelalte le adaugam la single
    while len(perechi) > round(nr_studenti / 3):
        # int(math.ceil(nr_studenti/3.0))
        max = -1
        cheie = ""
        for item in punctaje_perechi.keys():
            if punctaje_perechi[item] > max and '+' in item:
                max = punctaje_perechi[item]
                cheie = item

        del punctaje_perechi[cheie]
        perechi.remove(cheie)
        for item in cheie.split('+'):
            single.append(item)
            punctaje_perechi[item] = 80

    if len(punctaje_perechi) % 2 == 1:
        if nr_studenti % 3 == 0:
            '''
                numar impar de elemente, iar numarul de studenti este multiplu de 3, deci avem empty in punctaje_perechi
                solutie: eliminam tag-ul empty pentru a avea un numar par de elemente
            '''
            single.remove('empty')
            del punctaje_perechi['empty']
            i = 0
            while i < len(copie_students):
                if copie_students[i]['name'] == 'empty':
                    copie_students.remove(copie_students[i])
                else:
                    i += 1
            for st in copie_students:
                if 'empty' in st['preferences']:
                    st['preferences'].remove('empty')
        else:
            '''
                numar impar de elemente, deci vom adauga un student fictiv pentru a avea numar par
            '''
            punctaje_perechi['empty'] = 100
            single.append('empty')
            toti_studentii = lista_studenti(camin, facultate, sex)
            d = dict()
            d['name'] = "empty"
            d['propose'] = ""
            d['accept'] = ""
            shuffle(toti_studentii)
            studenti_preferati = list(toti_studentii)
            toti_studentii.append('empty')
            d['preferences'] = studenti_preferati
            duplicat_students.append(d)

            # adaugam colegul fictiv in listele studentilor unde este posibil
            updatare_optiuni(toti_studentii)
            copie_students = copy.deepcopy(duplicat_students)

    preferinte = dict()
    for item in perechi:
        st1 = item.split('+')[0]
        st2 = item.split('+')[1]
        optiuni = []
        for student in copie_students:
            if student['name'] == st1:
                preferences_st1 = copy.copy(student['preferences'])
            elif student['name'] == st2:
                preferences_st2 = copy.copy(student['preferences'])
        i = 0
        j = 0
        while i < len(preferences_st1) and j < len(preferences_st2):
            if preferences_st1[i] in single and preferences_st1[i] not in optiuni:
                optiuni.append(preferences_st1[i])
            if preferences_st2[j] in single and preferences_st2[j] not in optiuni:
                optiuni.append(preferences_st2[j])
            i += 1
            j += 1
        preferinte[item] = optiuni

    c = conn.cursor()
    c.execute("SELECT * from stable_repartizare r "
              "join stable_student s on s.numar_matricol = r.numar_matricol "
              "where r.camin=%s and s.facultate=%s and r.repartizare_camera=%s and s.sex=%s", [camin, facultate, False, sex])
    data = c.fetchall()
    c.close()

    studenti_eligibili = []
    for st in data:
        studenti_eligibili.append(st[1])

    for item in single:
        preferences = []
        for student in copie_students:
            if student['name'] == item:
                for i in student['preferences']:
                    if i in studenti_eligibili:
                        preferences.append(i)

        optiuni = []
        i = 0
        while i < len(preferences):
            if preferences[i] not in single and preferences[i] != 'empty':
                opt = cauta_pereche(punctaje_perechi, preferences[i])
                # print("opt  ", opt)
                preferences.remove(opt.split('+')[0])
                preferences.remove(opt.split('+')[1])
                optiuni.append(opt)
            else:
                i += 1

        for s in single:
            if item != s:
                optiuni.append(s)

        preferinte[item] = optiuni
    return preferinte


def coleg_fictiv(punctaje_perechi, camin, facultate, sex):
    global copie_students
    punctaje_perechi['empty+empty'] = 100
    toti_studentii = lista_studenti(camin, facultate, sex)
    toti_studentii.append('empty+empty')
    for item in punctaje_perechi.keys():
        if 'empty' in item:
            toti_studentii.append('empty')
            break
    d = dict()
    d['name'] = "empty+empty"
    d['propose'] = ""
    d['accept'] = ""
    shuffle(toti_studentii)
    studenti_preferati = []
    for i in toti_studentii:
        if i != "empty+empty":
            studenti_preferati.append(i)
    d['preferences'] = studenti_preferati
    duplicat_students.append(d)

    # adaugam colegul fictiv in listele studentilor unde este posibil
    updatare_optiuni(toti_studentii)
    copie_students = copy.deepcopy(duplicat_students)


def preferinte_pentru_stable_4(camin, punctaje_perechi, facultate, sex):
    global copie_students
    if len(punctaje_perechi) % 2 == 1:
        '''
        trebuie adaugat un coleg fictiv
        '''
        coleg_fictiv(punctaje_perechi, camin, facultate, sex)

    perechi = []
    single = []
    for item in punctaje_perechi.keys():
        if '+' in item:
            perechi.append(item)
        else:
            single.append(item)

    if len(single) == 0 and len(perechi) % 2 == 0:
        preferinte = dict()
        # luam fiecare pereche si concatenam unic cele 2 liste cu preferintele fiecaruia
        for item in perechi:
            if item != "empty+empty":
                st1 = item.split('+')[0]
                st2 = item.split('+')[1]
            else:
                st1 = item
                st2 = item
            optiuni = []
            for student in copie_students:
                if student['name'] == st1:
                    preferences_st1 = copy.copy(student['preferences'])
                if student['name'] == st2:
                    preferences_st2 = copy.copy(student['preferences'])

            i = 0
            j = 0
            while i < len(preferences_st1) and j < len(preferences_st2):
                aux = cauta_pereche(punctaje_perechi, preferences_st1[i])
                if aux not in optiuni and aux != item:
                    opt = cauta_pereche(punctaje_perechi, preferences_st1[i])
                    optiuni.append(opt)
                    if opt.split('+')[0] in preferences_st1:
                        preferences_st1.remove(opt.split('+')[0])
                    if opt.split('+')[1] in preferences_st1:
                        preferences_st1.remove(opt.split('+')[1])
                else:
                    i += 1

                aux = cauta_pereche(punctaje_perechi, preferences_st2[j])
                if aux not in optiuni and aux != item:
                    opt = cauta_pereche(punctaje_perechi, preferences_st2[j])
                    optiuni.append(opt)
                    if opt.split('+')[0] in preferences_st2:
                        preferences_st2.remove(opt.split('+')[0])
                    if opt.split('+')[1] in preferences_st2:
                        preferences_st2.remove(opt.split('+')[1])
                else:
                    j += 1
            preferinte[item] = optiuni

    return preferinte


def scor_camera(student, camera):
    if student == "":
        return 1000
    scor = 0
    # punctajele celor din camera pentru "candidat"
    for item in camera:
        for st in copie_students:
            if st['name'] == item:
                scor += st['preferences'].index(student)

    # punctajele "candidatului" pentru cei din camera
    for st in copie_students:
        if st['name'] == student:
            for item in camera:
                scor += st['preferences'].index(item)
    return scor


def nume_camera(camera):
    nume = ""
    for item in camera:
        nume += item + "+"
    if nume == "":
        return nume
    return nume[:-1]


def preferinte_pentru_stable_5(multime, perechi_ramase):
    camera_5 = dict()
    for camera in multime:
        nume = nume_camera(camera)
        camera_5[nume] = ""

    nr_studenti_fara_camera = 0
    for item in perechi_ramase:
        if item.split('+')[0] != 'empty':
            nr_studenti_fara_camera += 1
        if item.split('+')[1] != 'empty':
            nr_studenti_fara_camera += 1

    not_single = set()
    i = 0
    while True:
        i += 1
        if i > 100:
            break
        for item in perechi_ramase:
            st1 = item.split('+')[0]
            st2 = item.split('+')[1]
            minim = 1000
            minim2 = 1000

            cheie = ""
            cheie2 = ""
            for camera in multime:
                if st1 != 'empty':
                    min_local = scor_camera(st1, camera)
                    # print(minim, min_local, scor_camera(camera_5[nume_camera(camera)], camera), st1, camera)
                    if minim > min_local < scor_camera(camera_5[nume_camera(camera)], camera):
                        minim = min_local
                        cheie = nume_camera(camera)
                if st2 != "empty":
                    min_local = scor_camera(st2, camera)
                    # print(minim2, min_local, scor_camera(camera_5[nume_camera(camera)], camera), st2, camera)
                    if minim2 > min_local < scor_camera(camera_5[nume_camera(camera)], camera):
                        minim2 = min_local
                        cheie2 = nume_camera(camera)

            if cheie == cheie2:
                if minim < minim2:
                    cheie2 = ""
                else:
                    cheie = ""

            if len(cheie) > 0 and st1 != 'empty' and st1 not in not_single:
                not_single.add(st1)
                if camera_5[cheie] != "":
                    not_single.remove(camera_5[cheie])
                camera_5[cheie] = st1

            if len(cheie2) > 0 and st2 != 'empty' and st2 not in not_single:
                not_single.add(st2)
                if camera_5[cheie2] != "":
                    not_single.remove(camera_5[cheie2])
                camera_5[cheie2] = st2

        if len(not_single) == nr_studenti_fara_camera:
            break
    return camera_5


def updatare_optiuni(toti_studentii):
    global duplicat_students
    c = conn.cursor()
    for student in duplicat_students:
        c.execute("SELECT * from stable_preferinta where numar_matricol=%s order by importanta", [student['name']])
        data_pref = c.fetchall()
        studenti_preferati = []
        for i in data_pref:
            studenti_preferati.append(i[2])
        shuffle(toti_studentii)
        for st in toti_studentii:
            if st != student['name'] and st not in studenti_preferati:
                studenti_preferati.append(st)
        student['preferences'] = studenti_preferati


def calcul_punctaj():
    global copie_students
    global students
    global duplicat_students
    # aflam punctajul pentru preferinta fiecarei persoane; indexul persoanei repartizate din preferences
    punctaje = dict()
    for student in students:
        if student['preferences'][0] == 'empty':
            punctaje[student['name']] = 100
        else:
            for st in copie_students:
                if st['name'] == student['name']:
                    punctaje[student['name']] = st['preferences'].index(student['preferences'][0])

    # calculam punctajul pentru fiecare pereche in parte
    punctaje_perechi = dict()
    for student in students:
        if not exista_in_cheie(punctaje_perechi, student['name']):
            # print(student)
            key = student['name'] + "+" + student['preferences'][0]
            punctaje_perechi[key] = punctaje[student['name']]
            for st in copie_students:
                if st['name'] == student['preferences'][0]:
                    punctaje_perechi[key] += punctaje[st['name']]

    return punctaje_perechi


def creare_perechi(camin, locuri, facultate, sex):
    punctaje_perechi = calcul_punctaj()
    # pprint(copie_students)
    if locuri == 3:
        preferinte = preferinte_pentru_stable_3(camin, punctaje_perechi, facultate, sex)
    elif locuri == 4:
        preferinte = preferinte_pentru_stable_4(camin, punctaje_perechi, facultate, sex)

    preferintele_in_template(preferinte)


def creare_perechi_de_4(camin, locuri, facultate, sex):
    punctaje_perechi = calcul_punctaj()
    '''
        sortam crescator perechile dupa punctajul lor pentru a le lua pe cele mai bune; atatea perechi cate camere vor
        fi asignate x2(e.g. 13 studenti -> 3 camere -> deci 6 perechi)
    '''
    tuplu_sortat = sorted(punctaje_perechi.items(), key=operator.itemgetter(1))
    punctaje_top = []
    nr_studenti = len(lista_studenti(camin, facultate, sex))
    single = []
    perechi_ramase = []
    for i in range(2 * int(ceil(nr_studenti / 5.0))):
        punctaje_top.append(tuplu_sortat[i][0])
        single.append(tuplu_sortat[i][0].split('+')[0])
        single.append(tuplu_sortat[i][0].split('+')[1])

    for i in range(2 * int(ceil(nr_studenti / 5.0)), len(tuplu_sortat)):
        perechi_ramase.append(tuplu_sortat[i][0])

    preferinte = dict()
    for item in punctaje_top:
        st1 = item.split('+')[0]
        st2 = item.split('+')[1]
        optiuni = []
        for student in copie_students:
            if student['name'] == st1:
                preferences_st1 = copy.copy(student['preferences'])
            elif student['name'] == st2:
                preferences_st2 = copy.copy(student['preferences'])

        i = 0
        j = 0
        while i < len(preferences_st1) and j < len(preferences_st2):
            opt_st1 = cauta_pereche(punctaje_perechi, preferences_st1[i])
            opt_st2 = cauta_pereche(punctaje_perechi, preferences_st2[j])

            if preferences_st1[i] in single and opt_st1 not in optiuni and opt_st1 != item:
                if opt_st1.split('+')[0] in preferences_st1:
                    preferences_st1.remove(opt_st1.split('+')[0])
                if opt_st1.split('+')[1] in preferences_st1:
                    preferences_st1.remove(opt_st1.split('+')[1])
                optiuni.append(opt_st1)
            else:
                i += 1

            if preferences_st2[j] in single and opt_st2 not in optiuni and opt_st2 != item:
                if opt_st2.split('+')[0] in preferences_st2:
                    preferences_st2.remove(opt_st2.split('+')[0])
                if opt_st2.split('+')[1] in preferences_st2:
                    preferences_st2.remove(opt_st2.split('+')[1])
                optiuni.append(opt_st2)
            else:
                j += 1
        preferinte[item] = optiuni
    # pprint(preferinte)
    studenti_2si2 = []
    for item in preferinte.keys():
        d = dict()
        d['name'] = item
        d['propose'] = ""
        d['accept'] = ""
        d['preferences'] = preferinte[item]
        studenti_2si2.append(d)
    return studenti_2si2, perechi_ramase


def cauta_pereche(punctaje_perechi, name):
    for item in punctaje_perechi.keys():
        if name in item:
            return item


def afisare_camere(multime):
    camere = []
    for student in multime:
        o_camera = []
        for item in student['name'].split('+'):
            o_camera.append(item)

        for item in student['preferences'][0].split('+'):
            o_camera.append(item)
        o_camera.sort()
        if o_camera not in camere:
            camere.append(o_camera)
    return camere


def afisare_camere_de_5(multime):
    camere = []
    for item in multime.keys():
        o_camera = []
        for st in item.split('+'):
            if st != 'empty':
                o_camera.append(st)
        if len(multime[item]) > 0:
            o_camera.append(multime[item])
        camere.append(o_camera)
    return camere


def stocare_colegi_camera():
    camere = MultimeStabila.objects.all()
    for camera in camere:
        colegi = []
        if len(camera.coleg1) > 0:
            colegi.append(camera.coleg1)
        if len(camera.coleg2) > 0:
            colegi.append(camera.coleg2)
        if len(camera.coleg3) > 0:
            colegi.append(camera.coleg3)
        if len(camera.coleg4) > 0:
            colegi.append(camera.coleg4)
        if len(camera.coleg5) > 0:
            colegi.append(camera.coleg5)

        if len(colegi) > 1:
            for i in range(len(colegi)-1):
                for j in range(i+1, len(colegi)):
                    try:
                        camin = Repartizare.objects.get(numar_matricol=colegi[i])
                        aux = Coleg(coleg1=colegi[i], coleg2=colegi[j], nume_camin=camin.camin)
                        aux.save()
                    except Exception:
                        pass
                        # este posibil ca cele 2 persoane sa mai fi stat in aceesi camera deci exista deja o intrare in baza de date


def stocare(camere, camin):
    hostel = Camin.objects.filter(nume_camin=camin)
    numar_camere = []
    for item in hostel:
        if len(MultimeStabila.objects.filter(camera=item)) == 0:
            numar_camere.append(item.numar_camera)
    numar_camere.sort()

    for i in range(len(camere)):
        hostel = Camin.objects.get(nume_camin=camin, numar_camera=numar_camere[i])
        # in cazul in care aceasta camera este deja inserata trebuie sa o stergem
        try:
            camera = MultimeStabila.objects.get(camera=hostel)
            camera.delete()
        except:
            pass

        try:
            MultimeStabila.objects.create(
                camera=hostel,
                coleg1=camere[i][0]
            )
        except Exception as error:
            print(error)

        c = conn.cursor()
        if len(camere[i]) == 5:
            c.execute("UPDATE stable_multimestabila set coleg2=%s, coleg3=%s, coleg4=%s, coleg5=%s where coleg1=%s",
                      [camere[i][1], camere[i][2], camere[i][3], camere[i][4], camere[i][0]])
        elif len(camere[i]) == 4:
            c.execute(
                "UPDATE stable_multimestabila set coleg2=%s, coleg3=%s, coleg4=%s where coleg1=%s",
                [camere[i][1], camere[i][2], camere[i][3], camere[i][0]])
        elif len(camere[i]) == 3:
            c.execute(
                "UPDATE stable_multimestabila set coleg2=%s, coleg3=%s where coleg1=%s",
                [camere[i][1], camere[i][2], camere[i][0]])
        elif len(camere[i]) == 2:
            c.execute(
                "UPDATE stable_multimestabila set coleg2=%s where coleg1=%s",
                [camere[i][1], camere[i][0]])
        conn.commit()
        c.close()

        for j in range(len(camere[i])):
            aux = Repartizare.objects.get(numar_matricol=camere[i][j])
            aux.repartizare_camera = True
            aux.save()


def punctaj_camere(camere):
    global copie_students
    punctaj = dict()
    # pentru fiecare camera
    for camera in camere:
        punctaj[nume_camera(camera)] = 0
        # pentru fiecare student
        for st in camera:
            # cautam studentul in dictionarul initial
            for student in copie_students:
                if student['name'] == st:
                    # dupa ce l-am gasit vedem indexul preferintelor
                    for coleg in camera:
                        if coleg != st:
                            punctaj[nume_camera(camera)] += student['preferences'].index(coleg)
    return punctaj


def stocare_2(camere, camin, locuri, facultate):
    punctaj = punctaj_camere(camere)
    punctaj = sorted(punctaj.items(), key=operator.itemgetter(1))
    hostel = Camin.objects.filter(nume_camin=camin, locuri=locuri, facultate=facultate)
    numar_camere = []
    for item in hostel:
        if len(MultimeStabila.objects.filter(camera=item)) == 0:
            numar_camere.append(item.numar_camera)
    numar_camere.sort()

    for i in range(len(numar_camere)):
        key = punctaj[i][0]
        for camera in camere:
            if key.split('+')[0] in camera:

                hostel = Camin.objects.get(nume_camin=camin, numar_camera=numar_camere[i])
                # in cazul in care aceasta camera este deja inserata trebuie sa o stergem
                try:
                    camera = MultimeStabila.objects.get(camera=hostel)
                    camera.delete()
                except:
                    pass

                try:
                    MultimeStabila.objects.create(
                        camera=hostel,
                        coleg1=camere[i][0]
                    )
                except:
                    pass

                '''
                    try - except pentru ca repartizarea poate fi facuta intr-o camera de 2/3/4 persoane, dar in camera sa
                    fie de fapt o singura persoana repartizata, deci va fi eroare index out of range
                '''
                try:
                    if locuri == 2:
                        aux = MultimeStabila.objects.get(camera=hostel)
                        aux.coleg2 = camere[i][1]
                        aux.save()
                except Exception as error:
                    pass

                try:
                    if locuri == 3:
                        aux = MultimeStabila.objects.get(camera=hostel)
                        aux.coleg2 = camere[i][1]
                        aux.save()
                        aux.coleg3 = camere[i][2]
                        aux.save()
                except Exception as error:
                    pass

                try:
                    if locuri == 4:
                        aux = MultimeStabila.objects.get(camera=hostel)
                        aux.coleg2 = camere[i][1]
                        aux.save()
                        aux.coleg3 = camere[i][2]
                        aux.save()
                        aux.coleg4 = camere[i][3]
                        aux.save()
                except Exception as error:
                    pass
                c = conn.cursor()
                for j in range(len(camere[i])):
                    c.execute("UPDATE stable_repartizare set repartizare_camera=True where numar_matricol=%s", [camere[i][j]])
                conn.commit()
                c.close()


def stable(multime):
    s = 0
    #pprint(multime)
    while True:
        for st in multime:
            s += 1
            if s > 1000:
                raise SystemExit
            if st['propose'] == "":
                for option in st['preferences']:
                    accept = free(multime, option)
                    if accept == "":
                        st['propose'] = option
                        multime = propose(multime, st['name'], option)
                        break
                    else:
                        better_choice = who_is_beter(multime, st['name'], option, accept)

                        if better_choice == st['name']:
                            multime = abandon_current_accept(multime, option)
                            st['propose'] = option

                        multime = propose(multime, better_choice, option)
                        # stim ca studentul curent a facut o alegere valida, deci nu mai este nevoie sa caute in continuare
                        if better_choice == st['name']:
                            break

        if len([st for st in multime if st['propose'] == ""]) == 0:
            break
    '''
        pasul 2
        eliminam toti potentialii parteneri cu o importanta mai mica decat optiunea curenta
    '''
    for st in multime:
        try:
            to_delete = st['preferences'][st['preferences'].index(st['accept']) + 1:]
        except Exception as error:
            pass
        for it in to_delete:
            for i in multime:
                if it == i['name']:
                    try:
                        i['preferences'].remove(st['name'])
                        st['preferences'].remove(it)
                    except Exception as error:
                        pass
                    break
    '''
        pasul 3
        scriem un student care are mai mult de o optiune
        scriem acea a doua optiune, apoi pentru ea scriem ultima
        repetam pana cand studentul initial apare din nou
    '''
    # pprint(multime)
    while True:
        first_line = []
        second_line = []
        for st in multime:
            if len(st['preferences']) > 1:
                first_line.append(st['name'])
                second_line.append(st['preferences'][1])
                # while first_line.count(first_line[0]) != 2:
                while len(first_line) == len(set(first_line)):
                    for i in multime:
                        if i['name'] == second_line[-1]:
                            try:
                                first_line.append(i['preferences'][-1])
                            except Exception as error:
                                pass
                            break
                    for i in multime:
                        if i['name'] == first_line[-1]:
                            second_line.append(i['preferences'][1])
                            break
                break

        '''
            eliminam simetric first_line[i] cu second_line[i-1], i = 1, x
        '''
        for i in range(1, len(first_line)):
            for st in multime:
                if st['name'] == first_line[i]:
                    st['preferences'].remove(second_line[i - 1])
                if st['name'] == second_line[i - 1]:
                    st['preferences'].remove(first_line[i])

        if len([st for st in multime if len(st['preferences']) > 1]) == 0:
            break
    return multime


class Administrator(View):
    template_name = 'stable/comenzi_admin/repartizare.html'

    def camere_2(self, camin, sex):
        global students
        """
            param 2: indexul -> 2 = trebuie incarcate preferintele
                                3 = trebuie create perechile
            param 3: numarul de locuri
        """
        for facultate in FACULTATI:
            if incarcare_preferinte(camin, facultate, sex) == 1:
                students = stable(students)
                camere = afisare_camere(students)

                for camera in camere:
                    if 'empty' in camera:
                        camera.remove('empty')
                print("Camere de 2 persoane " + sex, camere)
                stocare_2(camere, camin, 2, facultate)

    def camere_3(self, camin, sex):
        global students
        for facultate in FACULTATI:
            del students[:]
            if incarcare_preferinte(camin, facultate, sex) == 1:
                multime_de_2 = stable(students)

                creare_perechi(camin, 3, facultate, sex)
                students = stable(multime_de_2)
                camere = afisare_camere(students)

                for camera in camere:
                    if 'empty' in camera:
                        camera.remove('empty')
                print("Camere de 3 persoane " + sex, camere)
                stocare_2(camere, camin, 3, facultate)

    def camere_4(self, camin, sex):
        global students
        for facultate in FACULTATI:
            if incarcare_preferinte(camin, facultate, sex) == 1:
                multime_de_2 = stable(students)

                creare_perechi(camin, 4, facultate, sex)
                students = stable(multime_de_2)
                camere = afisare_camere(students)

                for camera in camere:
                    i = 0
                    while i < len(camera):
                        if camera[i] == 'empty':
                            camera.remove('empty')
                        else:
                            i += 1
                print("Camere de 4 persoane " + sex, camere)
                stocare_2(camere, camin, 4, facultate)

    def camere_5(self, camin, sex):
        for facultate in FACULTATI:
            if incarcare_preferinte(camin, facultate, sex) == 1:
                if len(students) > 6:
                    multime_de_2 = stable(students)
                    studenti_2si2, perechi_ramase = creare_perechi_de_4(camin, 4, facultate, sex)
                    multime_de_4 = stable(studenti_2si2)
                    multime_de_5 = preferinte_pentru_stable_5(afisare_camere(multime_de_4), perechi_ramase)

                    camere = afisare_camere_de_5(multime_de_5)
                else:
                    o_camera = []
                    camere = []
                    for item in students:
                        o_camera.append(item['name'])
                    camere.append(o_camera)
                print("Repartizare camere 5 persoane " + sex, camere)
                stocare(camere, camin)

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        mesaj_warning = ""
        semafor = True
        p = 0
        for camin in camine:
            print("\n")
            print("CAMIN")
            print(camin)
            print("\n\n")
            if 2 in LOCURI[camin]:
                while semafor and p < 50:
                    try:
                        self.camere_2(camin, "F")
                        semafor = False
                    except:
                        mesaj_warning = "Ups, se pare ca ceva nu a mers bine, te rugam sa incerci din nou!"
                        p += 1
                if semafor:
                    return render(request, self.template_name, {'mesaj_warning': mesaj_warning})

                semafor = True
                while semafor and p < 50:
                    try:
                        self.camere_2(camin, "M")
                        semafor = False
                    except:
                        mesaj_warning = "Ups, se pare ca ceva nu a mers bine, te rugam sa incerci din nou!"
                        p += 1
                if semafor:
                    return render(request, self.template_name, {'mesaj_warning': mesaj_warning})

            if 3 in LOCURI[camin]:
                p = 0
                semafor = True
                while semafor and p < 50:
                    try:
                        self.camere_3(camin, "F")
                        semafor = False
                    except:
                        mesaj_warning = "Ups, se pare ca ceva nu a mers bine, te rugam sa incerci din nou!"
                        p += 1
                if semafor:
                    return render(request, self.template_name, {'mesaj_warning': mesaj_warning})

                p = 0
                semafor = True
                while semafor and p < 50:
                    try:
                        self.camere_3(camin, "M")
                        semafor = False
                    except:
                        mesaj_warning = "Ups, se pare ca ceva nu a mers bine, te rugam sa incerci din nou!"
                        p += 1
                if semafor:
                    return render(request, self.template_name, {'mesaj_warning': mesaj_warning})

            if 4 in LOCURI[camin]:
                p = 0
                semafor = True
                while semafor and p < 50:
                    try:
                        self.camere_4(camin, "F")
                        semafor = False
                    except:
                        mesaj_warning = "Ups, se pare ca ceva nu a mers bine, te rugam sa incerci din nou!"
                        p += 1
                if semafor:
                    return render(request, self.template_name, {'mesaj_warning': mesaj_warning})

                p = 0
                semafor = True
                while semafor and p < 50:
                    try:
                        self.camere_4(camin, "M")
                        semafor = False
                    except:
                        mesaj_warning = "Ups, se pare ca ceva nu a mers bine, te rugam sa incerci din nou!"
                        p += 1
                if semafor:
                    return render(request, self.template_name, {'mesaj_warning': mesaj_warning})

            if 5 in LOCURI[camin]:
                p = 0
                semafor = True
                while semafor and p < 50:
                    try:
                        self.camere_5(camin, "F")
                        semafor = False
                    except:
                        mesaj_warning = "Ups, se pare ca ceva nu a mers bine, te rugam sa incerci din nou!"
                        p += 1

                p = 0
                semafor = True
                while semafor and p < 150:
                    try:
                        self.camere_5(camin, "M")
                        semafor = False
                    except:
                        mesaj_warning = "Ups, se pare ca ceva nu a mers bine, te rugam sa incerci din nou!"
                        p += 1

        mesaj_succes = "Repartizare realizată cu succes."
        stocare_colegi_camera()
        if not semafor:
            return render(request, self.template_name, {'mesaj_succes': mesaj_succes})
        else:
            return render(request, self.template_name, {'mesaj_warning': mesaj_warning})


class Resetare(View):
    template_name = 'stable/comenzi_admin/resetare.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        aux = Repartizare.objects.filter(repartizare_camera=True)
        for item in aux:
            item.repartizare_camera = False
            item.save()

        stable = MultimeStabila.objects.all()
        for item in stable:
            colegi = []
            if len(item.coleg1) > 0:
                colegi.append(item.coleg1)
            if len(item.coleg2) > 0:
                colegi.append(item.coleg2)
            if len(item.coleg3) > 0:
                colegi.append(item.coleg3)
            if len(item.coleg4) > 0:
                colegi.append(item.coleg4)
            if len(item.coleg5) > 0:
                colegi.append(item.coleg5)
            for i in range(len(colegi)-1):
                for j in range(i+1, len(colegi)):
                    Coleg.objects.filter(coleg1=colegi[i], coleg2=colegi[j]).delete()
                    Coleg.objects.filter(coleg1=colegi[j], coleg2=colegi[i]).delete()

        MultimeStabila.objects.all().delete()
        return render(request, self.template_name, {'mesaj_succes': "Datele au fost resetate"})


class Avansare(View):
    template_name = 'stable/comenzi_admin/avansareAn.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        studenti = Student.objects.all()
        for st in studenti:
            st.an += 1
            st.save()
        return render(request, self.template_name)


class GenerareExcel(View):
    template_name = 'stable/comenzi_admin/generareExcel.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        ok = True
        try:
            export_repartizare()
        except PermissionError:
            mesaj_warning = "Un fișier cu același nume este deschis"
            ok = False
        except Exception:
            mesaj_warning = "Eroare neașteptată, te rugăm să reîncerci"
            ok = False
        if ok:
            return render(request, self.template_name, {'mesaj_succes': "Fișierul a fost generat"})
        else:
            return render(request, self.template_name, {'mesaj_warning': mesaj_warning})


class StatisticaCamine(View):
    template_name = 'stable/comenzi_admin/camin.html'

    def get(self, request):
        camere_universitate = dict()
        for f in FACULTATI:
            camere_universitate[f] = []
            for item in camine:
                camere_fac = dict()
                aux = Camin.objects.filter(nume_camin=item, facultate=f)

                if len(aux) > 0:
                    camere_fac[item] = []

                    for i in aux:
                        camera = MultimeStabila.objects.filter(camera=i)
                        rez = []
                        camera_dict = dict()
                        if len(camera) > 0:
                            if len(camera[0].coleg1) > 0:
                                st = Student.objects.get(numar_matricol=camera[0].coleg1)
                                rez.append(st.nume)
                            if len(camera[0].coleg2) > 0:
                                st = Student.objects.get(numar_matricol=camera[0].coleg2)
                                rez.append(st.nume)
                            if len(camera[0].coleg3) > 0:
                                st = Student.objects.get(numar_matricol=camera[0].coleg3)
                                rez.append(st.nume)
                            if len(camera[0].coleg4) > 0:
                                st = Student.objects.get(numar_matricol=camera[0].coleg4)
                                rez.append(st.nume)
                            if len(camera[0].coleg5) > 0:
                                st = Student.objects.get(numar_matricol=camera[0].coleg5)
                                rez.append(st.nume)
                        while len(rez) < i.locuri:
                            rez.append("<loc liber>")
                        camera_dict[str(i.numar_camera)] = rez
                        camere_fac[item].append(camera_dict)

                if len(camere_fac) > 0:
                    camere_universitate[f].append(camere_fac)

        return render(request, self.template_name, {'repartizare': camere_universitate})

    def post(self, request):
        return render(request, self.template_name)


class CreareConturi(View):
    template_name = 'stable/comenzi_admin/cont.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        try:
            lista = request.FILES['fisier_studenti']
        except Exception as error:
            pass
        else:
            lungime = 1
            while lungime != 0:
                content = lista.readline().decode('utf-8')
                if len(content) > 0:
                    content = content.split(',')
                    query = Student(nume=content[1], numar_matricol=content[2], facultate=content[6][:-2], an=content[0],
                                    grupa=content[5], sex=content[4], email=content[3])
                    query.save()
                    password = ""
                    for i in range(5):
                        cifre = randint(0, 99)
                        password += str(cifre)
                    try:
                        user = User(username=content[2], password=password)
                        user.save()
                    except Exception:
                        pass
                        # are deja contul inregistrat

                lungime = len(content)
        return render(request, self.template_name, {'mesaj_succes': "Conturile au fost create"})


class Mesaj(View):
    template_name = 'stable/comenzi_admin/anunt.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        titlu = request.POST.get('titlu', '')
        mesaj = request.POST.get('message', '')
        data = request.POST.get('data', '')
        if len(data) > 0:
            query = Anunt(titlu=titlu, mesaj=mesaj, deadline=data)
        else:
            query = Anunt(titlu=titlu, mesaj=mesaj)
        query.save()
        return render(request, self.template_name, {'mesaj_succes': "Succes! Anunțul a fost postat."})


class Repartizare_camin(View):
    template_name = 'stable/comenzi_admin/dispozitie.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        try:
            lista = request.FILES['fisier_camin']
        except Exception as error:
            pass
        else:
            lungime = 1
            while lungime != 0:
                content = lista.readline().decode('utf-8')
                if len(content) > 0:
                    content = content.split(',')
                    try:
                        query = Repartizare(numar_matricol=content[0], camin=content[1][:-2])
                        query.save()
                    except Exception:
                        pass
                        # deja exista o intrare in baza de date, deci nu mai poate fi introdusa
                lungime = len(content)

        return render(request, self.template_name, {'mesaj_succes': "Repartizare realizată cu succes."})
