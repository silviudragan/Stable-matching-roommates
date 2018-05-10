import copy
import operator
from math import floor, ceil
from pprint import pprint
from random import shuffle

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
import MySQLdb

conn = MySQLdb.connect(host="localhost",
                       user="root",
                       passwd="Silviu01",
                       db="test")
students = []
copie_students = []
duplicat_students = []
camine = ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C10', 'C11', 'C12', 'C13', 'Gaudeamus', 'Akademos',
          'Buna Vestire']


def lista_studenti(camin):
    c = conn.cursor()

    c.execute("SELECT * from stable_repartizare where camin=%s", [camin])
    data = c.fetchall()
    toti_studentii = []
    for st in data:
        toti_studentii.append(st[1])
    return toti_studentii


def adaugare_coleg_fals(camin):
    toti_studentii = lista_studenti(camin)
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


def incarcare_preferinte(camin):
    del students[:]
    c = conn.cursor()

    toti_studentii = lista_studenti(camin)
    empty = False
    if len(toti_studentii) % 2 == 1:
        toti_studentii.append("empty")
        empty = True

    c.execute("SELECT * from stable_repartizare where camin=%s", [camin])
    data = c.fetchall()
    for st in data:
        d = dict()
        numar_matricol = st[1]
        d['name'] = numar_matricol
        d['propose'] = ""
        d['accept'] = ""

        c.execute("SELECT * from stable_preferinta where numar_matricol=%s order by importanta", [numar_matricol])
        data_pref = c.fetchall()
        studenti_preferati = []
        for i in data_pref:
            studenti_preferati.append(i[2])
        shuffle(toti_studentii)
        for st in toti_studentii:
            if st != numar_matricol and st not in studenti_preferati:
                studenti_preferati.append(st)
        d['preferences'] = studenti_preferati
        students.append(d)

    if empty:
        adaugare_coleg_fals(camin)

    c.close()
    # print('########################################')
    # pprint(students)
    # print('########################################')
    global copie_students
    copie_students = copy.deepcopy(students)
    global duplicat_students
    duplicat_students = copy.deepcopy(students)


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


def preferinte_pentru_stable_3(camin, punctaje_perechi):
    global copie_students
    global duplicat_students
    perechi = []
    single = []
    for item in punctaje_perechi.keys():
        if '+' in item:
            perechi.append(item)
        else:
            single.append(item)

    nr_studenti = len(lista_studenti(camin))

    # trebuie sa pastram atatea perechi cate camere vor fi - 1, iar pe celelalte le adaugam la single
    while len(perechi) > round(nr_studenti/3):
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
                numar impar de elemente, deci vom adauga un student fictiv pentru a avea numar impar
            '''
            punctaje_perechi['empty'] = 100
            single.append('empty')
            toti_studentii = lista_studenti(camin)
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

    # print("ppppp ", len(punctaje_perechi))
    # print("punctaje_perechi", punctaje_perechi)
    # print("single", single)
    # print("perechi", perechi)
    # pprint(copie_students)
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

    for item in single:
        for student in copie_students:
            if student['name'] == item:
                preferences = copy.copy(student['preferences'])

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
    # print("pref", preferinte)
    return preferinte


def coleg_fictiv(punctaje_perechi, camin):
    global copie_students
    punctaje_perechi['empty+empty'] = 100
    toti_studentii = lista_studenti(camin)
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


def preferinte_pentru_stable_4(camin, punctaje_perechi):
    # print("p", len(punctaje_perechi))
    global copie_students
    # print("++++++++++++++++++++")
    # pprint(lista_studenti(camin))
    # print("++++++++++++++++++++")
    if len(punctaje_perechi) % 2 == 1:
        '''
        trebuie adaugat un coleg fictiv
        '''
        coleg_fictiv(punctaje_perechi, camin)

    perechi = []
    single = []
    for item in punctaje_perechi.keys():
        if '+' in item:
            perechi.append(item)
        else:
            single.append(item)
    # print("pereeeechi", punctaje_perechi)
    # pprint(copie_students)
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
            # print("d")
            # pprint(copie_students)
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

    # print("pref ", preferinte)
    return preferinte


def scor_camera(student, camera):
    if student == "":
        return -1
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


def better_fit(student_actual, candidat, camera):
    return scor_camera(student_actual, camera) > scor_camera(candidat,camera)


def nume_camera(camera):
    nume = ""
    for item in camera:
        nume += item + "+"
    if nume == "":
        return nume
    return nume[:-1]


def verificare_cheie(camere, student):
    chei = []
    for item in camere.keys():
        if camere[item] == student:
            chei.append(item)
    return chei


def preferinte_pentru_stable_5(multime, perechi_ramase):
    print("**************************")
    print(multime)
    print("X")
    print(perechi_ramase)
    print("**************************")
    pprint(copie_students)

    print("0")
    camera_5 = dict()
    for camera in multime:
        nume = nume_camera(camera)
        camera_5[nume] = ""
    print("1")
    nr_studenti_fara_camera = 0
    for item in perechi_ramase:
        if item.split('+')[0] != 'empty':
            nr_studenti_fara_camera += 1
        if item.split('+')[1] != 'empty':
            nr_studenti_fara_camera += 1
    print("2")
    print(nr_studenti_fara_camera)
    not_single = set()
    while True:
        for item in perechi_ramase:
            st1 = item.split('+')[0]
            st2 = item.split('+')[1]
            minim = 1000
            for camera in multime:
                if st1 != 'empty':
                    min_local = scor_camera(st1, camera)
                    # print(min_local, st1, camera)
                    if minim > min_local > scor_camera(camera_5[nume_camera(camera)], camera):
                        minim = min_local
                        if camera_5[nume_camera(camera)] == "":
                            camera_5[nume_camera(camera)] = st1
                            print("1", minim, st1, nume_camera(camera))
                            not_single.add(st1)
                            chei = verificare_cheie(camera_5, st1)
                            for cheie in chei:
                                if cheie != nume_camera(camera):
                                    camera_5[cheie] = ""

                        elif better_fit(camera_5[nume_camera(camera)], st1, camera):
                            not_single.remove(camera_5[nume_camera(camera)])
                            camera_5[nume_camera(camera)] = st1
                            not_single.add(st1)
                            print("2", minim, st1, nume_camera(camera))

                if st2 != 'empty':
                    min_local = scor_camera(st2, camera)
                    if minim > min_local > scor_camera(camera_5[nume_camera(camera)], camera):
                        minim = min_local
                        if camera_5[nume_camera(camera)] == "":
                            camera_5[nume_camera(camera)] = st2
                            not_single.add(st2)
                            print("3", minim, st2, nume_camera(camera))
                        elif better_fit(camera_5[nume_camera(camera)], st2, camera):
                            not_single.remove(camera_5[nume_camera(camera)])
                            camera_5[nume_camera(camera)] = st2
                            not_single.add(st2)
                            print("4", minim, st2, nume_camera(camera))

        print(not_single)
        # break
        # print(camera_5)
        if len(not_single) == nr_studenti_fara_camera:
            break
    print(camera_5)
    return 1


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


def creare_perechi(camin, locuri):
    punctaje_perechi = calcul_punctaj()

    # pprint(copie_students)
    if locuri == 3:
        preferinte = preferinte_pentru_stable_3(camin, punctaje_perechi)
    elif locuri == 4:
        preferinte = preferinte_pentru_stable_4(camin, punctaje_perechi)

    preferintele_in_template(preferinte)


def creare_perechi_de_4(camin, locuri):
    punctaje_perechi = calcul_punctaj()
    '''
        sortam crescator perechile dupa punctajul lor pentru a le lua pe cele mai bune; atatea perechi cate camere vor
        fi asignate x2(e.g. 13 studenti -> 3 camere -> deci 6 perechi)
    '''
    tuplu_sortat = sorted(punctaje_perechi.items(), key=operator.itemgetter(1))
    punctaje_top = []
    nr_studenti = len(lista_studenti(camin))
    single = []
    perechi_ramase = []
    for i in range(2*int(ceil(nr_studenti/5.0))):
        punctaje_top.append(tuplu_sortat[i][0])
        single.append(tuplu_sortat[i][0].split('+')[0])
        single.append(tuplu_sortat[i][0].split('+')[1])

    for i in range(2*int(ceil(nr_studenti/5.0)), len(tuplu_sortat)):
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
    print("am ajuns aici")
    # pprint(multime)
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


def stable(multime):
    # pprint(multime)
    s = 0
    while True:
        for st in multime:
            # print("a1")
            s += 1
            if s > 1000:
                raise SystemExit
            if st['propose'] == "":
                for option in st['preferences']:
                    accept = free(multime, option)
                    if accept == "":
                        st['propose'] = option
                        multime = propose(multime, st['name'], option)
                        # print("a2")
                        break
                    else:
                        better_choice = who_is_beter(multime, st['name'], option, accept)

                        if better_choice == st['name']:
                            multime = abandon_current_accept(multime, option)
                            st['propose'] = option

                        multime = propose(multime, better_choice, option)
                        # print("a3")
                        # stim ca studentul curent a facut o alegere valida, deci nu mai este nevoie sa caute in continuare
                        if better_choice == st['name']:
                            # print("a4")
                            break

        if len([st for st in multime if st['propose'] == ""]) == 0:
            # print("a5")
            break
    '''
        pasul 2
        eliminam toti potentialii parteneri cu o importanta mai mica decat optiunea curenta
    '''
    for st in multime:
        try:
            to_delete = st['preferences'][st['preferences'].index(st['accept']) + 1:]
        except Exception as error:
            print("1", error)
        # print(to_delete)
        for it in to_delete:
            for i in multime:
                if it == i['name']:
                    try:
                        # print("2222222222")
                        # print(st)
                        # print("it  ", it)
                        # print("ii    ", i)
                        # print("2222222222")
                        i['preferences'].remove(st['name'])
                        st['preferences'].remove(it)
                    except Exception as error:
                        print("2", error)
                    break
    # print("b")
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
            # print("b1")
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
                                print("3", error)
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
        # print("b7")
        if len([st for st in multime if len(st['preferences']) > 1]) == 0:
            break
        # print("b6")
    # print("c")
    return multime


class Administrator(View):
    template_name = 'stable/admin.html'

    def camere_2(self, camin):
        global students
        """
            param 2: indexul -> 2 = trebuie incarcate preferintele
                                3 = trebuie create perechile
            param 3: numarul de locuri
        """
        incarcare_preferinte(camin)
        students = stable(students)
        print("Camere de 2 persoane", afisare_camere(students))

    def camere_3(self, camin):
        global students
        del students[:]
        incarcare_preferinte(camin)
        multime_de_2 = stable(students)

        creare_perechi(camin, 3)
        students = stable(multime_de_2)
        print("Camere de 3 persoane", afisare_camere(students))

    def camere_4(self, camin):
        global students
        incarcare_preferinte(camin)
        multime_de_2 = stable(students)
        # print("intermediar Camere de 4 persoane", afisare_camere(multime_de_2))

        creare_perechi(camin, 4)
        students = stable(multime_de_2)
        print("Camere de 4 persoane", afisare_camere(students))

    def camere_5(self, camin):
        incarcare_preferinte(camin)
        multime_de_2 = stable(students)
        # print("1111111111111111111111111111111")
        # pprint(multime_de_2)
        # print("1111111111111111111111111111111")
        # print("de 2", afisare_camere(students))

        studenti_2si2, perechi_ramase = creare_perechi_de_4(camin, 4)
        # print("camere_5")
        multime_de_4 = stable(studenti_2si2)

        multime_de_5 = preferinte_pentru_stable_5(afisare_camere(multime_de_4), perechi_ramase)
        print("Repartizare camere 4 persoane", afisare_camere(multime_de_4))
        # print("---------------------------------")
        # pprint(multime_de_4)
        # print("---------------------------------")

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        mesaj_warning = ""
        semafor = True
        s = 0
        p = 0
        while semafor and p < 500:
            try:
                self.camere_2('C12')
                semafor = False
            except:
                mesaj_warning = "Ups, se pare ca ceva nu a mers bine, te rugam sa incerci din nou!" + str(p)
                p += 1
                s += 1

        p = 0
        semafor = True
        while semafor and p < 500:
            try:
                self.camere_3('C12')
                semafor = False
            except:
                mesaj_warning = "Ups, se pare ca ceva nu a mers bine, te rugam sa incerci din nou!" + str(p)
                p += 1
                s += 1

        p = 0
        semafor = True
        while semafor and p < 500:
            try:
                self.camere_4('C12')
                semafor = False
            except:
                mesaj_warning = "Ups, se pare ca ceva nu a mers bine, te rugam sa incerci din nou!" + str(p)
                p += 1

        p = 0
        semafor = True
        while semafor and p < 500:
            try:
                self.camere_5('C12')
                semafor = False
            except:
                mesaj_warning = "Ups, se pare ca ceva nu a mers bine, te rugam sa incerci din nou!" + str(p)
                p += 1
                s += 1

        # pprint(students)
        mesaj_succes = "Repartizarea a fost facuta cu succes." + str(p) + " -> " + str(s)
        if not semafor:
            return render(request, self.template_name, {'mesaj_succes': mesaj_succes})
        else:
            return render(request, self.template_name, {'mesaj_warning': mesaj_warning})


def avansare_an_studiu(request):
    print("avansare an studiu")
    return JsonResponse({})
