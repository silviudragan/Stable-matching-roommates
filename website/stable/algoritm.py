from pprint import pprint

students = []
with open('input.txt') as f:
    line = f.readline()
    while line:
        d = dict()
        d['name'] = line.split(':')[0]
        d['preferences'] = line.split(':')[1].split()
        d['propose'] = ""
        d['accept'] = ""
        students.append(d)
        line = f.readline()


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
            except:
                pass
            for st_rm in students:
                if st_rm['name'] == current_accept:
                    st_rm['preferences'].remove(option)
                    st_rm['propose'] = ""


def stable():
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
        except:
            pass
        print(to_delete)
        for it in to_delete:
            for i in students:
                if it == i['name']:
                    try:
                        i['preferences'].remove(st['name'])
                        st['preferences'].remove(it)
                    except:
                        pass
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
                            except:
                                pass
                            break
                    for i in students:
                        if i['name'] == first_line[-1]:
                            second_line.append(i['preferences'][1])
                            break
                break
        print(first_line)
        print(second_line)
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


stable()
pprint(students)
