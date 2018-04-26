import copy
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
camine = ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C10', 'C11', 'C12', 'C13', 'Gaudeamus', 'Akademos',
          'Buna Vestire']


def incarcare_preferinte(camin):
    del students[:]
    c = conn.cursor()

    c.execute("SELECT * from stable_repartizare where camin=%s", [camin])
    data = c.fetchall()
    toti_studentii = []
    for st in data:
        toti_studentii.append(st[1])
    empty = False
    if len(toti_studentii) % 2 == 1:
        toti_studentii.append("empty")
        empty = True

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
        d = dict()
        d['name'] = "empty"
        d['propose'] = ""
        d['accept'] = ""
        shuffle(toti_studentii)
        print("2 ", toti_studentii)
        studenti_preferati = []
        for i in toti_studentii:
            if i is not "empty":
                studenti_preferati.append(i)
        d['preferences'] = studenti_preferati
        students.append(d)
    c.close()
    print('########################################')
    pprint(students)
    print('########################################')
    global copie_students
    copie_students = copy.deepcopy(students)


def free(option):
    for st in students:
        if option == st['name']:
            return st['accept']


def propose(searcher, option):
    for st in students:
        if option == st['name']:
            st['accept'] = searcher


def who_is_beter(searcher, option, current):
    for st in students:
        if option == st['name']:
            for p in st['preferences']:
                if p == searcher:
                    return searcher
                if p == current:
                    return current


def abandon_current_accept(option):
    for st in students:
        if option == st['name']:
            current_accept = st['accept']
            try:
                st['preferences'].remove(current_accept)
            except Exception as error:
                print(error)
            for st_rm in students:
                if st_rm['name'] == current_accept:
                    st_rm['preferences'].remove(option)
                    st_rm['propose'] = ""


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


def creare_perechi():
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
    if len(students) % 3 == 1 and verificare_tag_empty():
        '''
        trebuie doar eliminat empty din perechea corespunzatoare
        '''
        # print(punctaje_perechi)
        for item in punctaje_perechi.keys():
            if 'empty' in item:
                new_key = item.replace('empty', '')
                new_key = new_key.replace('+', '')
                punctaje_perechi[new_key] = punctaje_perechi.pop(item)
        # print(punctaje_perechi)
    else:
        '''
        trebuie adaugate empty multiplu de 3
        '''
    # print(punctaje_perechi)
    preferinte_pentru_stable_3(punctaje_perechi)


def preferinte_pentru_stable_3(punctaje_perechi):
    perechi = []
    single = []
    for item in punctaje_perechi.keys():
        if '+' in item:
            perechi.append(item)
        else:
            single.append(item)

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
        for p in perechi:
            st1 = p.split('+')[0]
            st2 = p.split('+')[1]

            if preferences.index(st1) < preferences.index(st2):
                optiuni.append(st1)
            else:
                optiuni.append(st2)
        preferinte[item] = optiuni
    print(preferinte)


def stable(camin):
    incarcare_preferinte(camin)
    while True:
        for st in students:
            if st['propose'] == "":
                for option in st['preferences']:
                    accept = free(option)
                    if accept == "":
                        st['propose'] = option
                        propose(st['name'], option)
                        break
                    else:
                        better_choice = who_is_beter(st['name'], option, accept)

                        if better_choice == st['name']:
                            abandon_current_accept(option)
                            st['propose'] = option

                        propose(better_choice, option)

                        # stim ca studentul curent a facut o alegere valida, deci nu mai este nevoie sa caute in continuare
                        if better_choice == st['name']:
                            break
        if len([st for st in students if st['propose'] == ""]) == 0:
            break
    '''
        pasul 2
        eliminam toti potentialii parteneri cu o importanta mai mica decat optiunea curenta
    '''
    for st in students:
        try:
            to_delete = st['preferences'][st['preferences'].index(st['accept'])+1:]
        except Exception as error:
            print(error)
        # print(to_delete)
        for it in to_delete:
            for i in students:
                if it == i['name']:
                    try:
                        i['preferences'].remove(st['name'])
                        st['preferences'].remove(it)
                    except Exception as error:
                        print(error)
                    break
    '''
        pasul 3
        scriem un student care are mai mult de o optiune
        scriem acea a doua optiune, apoi pentru ea scriem ultima
        repetam pana cand studentul initial apare din nou
    '''
    while True:
        first_line = []
        second_line = []
        for st in students:
            if len(st['preferences']) > 1:
                first_line.append(st['name'])
                second_line.append(st['preferences'][1])
                while first_line.count(first_line[0]) != 2:
                    for i in students:
                        if i['name'] == second_line[-1]:
                            try:
                                first_line.append(i['preferences'][-1])
                            except Exception as error:
                                print(error)
                            break
                    for i in students:
                        if i['name'] == first_line[-1]:
                            second_line.append(i['preferences'][1])
                            break
                break

        '''
            eliminam simetric first_line[i] cu second_line[i-1], i = 1, x
        '''
        for i in range(1, len(first_line)):
            for st in students:
                if st['name'] == first_line[i]:
                    st['preferences'].remove(second_line[i-1])
                if st['name'] == second_line[i-1]:
                    st['preferences'].remove(first_line[i])

        if len([st for st in students if len(st['preferences']) > 1]) == 0:
            break


class Administrator(View):
    template_name = 'stable/admin.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        try:
            stable('C12')
        except:
            mesaj = "Ups, se pare ca ceva nu a mers bine, te rugam sa incerci din nou!"
            return render(request, self.template_name, {'mesaj_warning': mesaj})
        # pprint(students)
        for student in students:
            print(student['name'] + " -> " + student['preferences'][0] + " " + str(len(student['preferences'])))
        creare_perechi()
        mesaj = "Repartizarea a fost facuta cu succes."
        return render(request, self.template_name, {'mesaj_succes': mesaj})


def avansare_an_studiu(request):
    print("avansare an studiu")
    return JsonResponse({})
