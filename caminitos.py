import networkx as nx
import numpy as np

fileInput = "b.in"
fileOutput = "b2.out"

# INPUT
time = 0
Dijkstra = ""
libraries = []  # SOLO SE USA PARA CALCULAR EL DIKSTRA
book_value = []  # VECTOR DE LIBROS CON VALOR
book_library = []  # VECTOR DE LIBROS CON POSITION
reader_book = []
reader_library = []
person_book_value = []

# OUPUT
actions = []


def processInput():
    with open(fileInput) as fd:
        text = fd.readlines()

    global time
    global book_library
    global book_value
    global person_book_value
    time = int(text[0].split()[1])

    cont = 1
    while text[cont].split()[0] == 'L':
        t = list(map(int, text[cont].split()[2:]))
        libraries.append(t)
        cont += 1

    a = np.array(libraries)
    global Dijkstra
    Dijkstra = nx.from_numpy_matrix(a, create_using=nx.DiGraph)

    while text[cont].split()[0] == 'B':
        book_library.append(int(text[cont].split()[3]))
        book_value.append(int(text[cont].split()[2]))
        cont += 1

    cnt_person = 0
    while len(text) > cont and text[cont].split()[0] == 'R':
        reader_library.append(int(text[cont].split()[2]))
        book = text[cont].split()[3:]
        books = {}
        person_book_value.append({})
        c = 0
        while c < len(book):
            read_cost = int(book[c + 1]) + distance_p2p(int(book[c]), int(text[cont].split()[2]))
            if read_cost <= time:
                calc = book_value[int(book[c])] / read_cost
                person_book_value[cnt_person].setdefault(int(book[c]), calc)
                person_book_value[cnt_person] = {k: v for k, v in sorted(person_book_value[cnt_person].items(),
                                                                         key=lambda item: item[1])}
                books[int(book[c])] = int(book[c + 1])
            c += 2
        reader_book.append(books)
        cont += 1
        cnt_person += 1


def move(book, lib):
    origen = book_library[book]
    path = nx.dijkstra_path(Dijkstra, origen, lib)
    for x in range(len(path)-1):
        actions.append(str(book) + ' m ' + str(path[x + 1]))
    book_library[book] = lib


def read(book, person):
    actions.append(str(book) + ' r ' + str(person))


def distance(book_id, person_id):
    x = book_library[book_id]
    y = reader_library[person_id]
    return nx.single_source_dijkstra(Dijkstra, x, y)[0]


def distance_p2p(book_id, lib):
    x = book_library[book_id]
    return nx.single_source_dijkstra(Dijkstra, x, lib)[0]


def book_is_here(book_id, person_id):
    return book_library[book_id] == reader_library[person_id]


def calc_time_toRead(book_id, person_id):
    return int(dict(reader_book[person_id]).get(book_id) + distance(book_id, person_id))


def calc_book_value(book_id, person_id):
    val = calc_time_toRead(book_id, person_id)
    if val >= time:
        return -1
    return book_value[book_id] / (calc_time_toRead(book_id, person_id) + val)


def get_forat(time, person_id, size, offset, llibre_no_disp):  # TODO: Refactor This
    cont = 0
    if llibre_no_disp is not None:
        if offset + size >= len(time[person_id]):
            return -1
        for x in range(offset, len(time[person_id])):
            if time[person_id][x] < 3 and llibre_no_disp[0] >= x >= llibre_no_disp[1]:
                cont += 1
            else:
                cont = 0
            if cont == size:
                return (x + 1) - cont
    else:
        if offset + size >= len(time[person_id]):
            return -1
        for x in range(offset, len(time[person_id])):
            if time[person_id][x] < 3:
                cont += 1
            else:
                cont = 0
            if cont == size:
                return (x + 1) - cont
    return -1


def pintar(time, person_id, position, size):
    for x in range(size):
        time[person_id][position + x] += 1


def safe_list_get(l, idx):
    try:
        return l[idx]
    except:
        return None


def writeOutput():
    with open(fileOutput, "w") as fd:
        for x in actions:
            fd.write(x + '\n')


def selectNext():
    max = 0
    nextPerson = -1
    cont = 0
    for person in person_book_value:
        if len(person.values()) != 0:
            m = list(person.values())[len(person.values())-1]
            if m > max:
                max = m
                nextPerson = cont
        cont += 1
    return nextPerson



def get_person_time(person_id, book_id):
    return int(dict(reader_book[person_id]).get(book_id))


def schedule():
    global book_library
    global book_value
    global reader_library
    timeMat = np.zeros((len(reader_library), int(time)))
    llibre_no_disp = {}
    reader = selectNext()

    while reader != -1:
        person_book_value[reader] = {k: v for k, v in sorted(person_book_value[reader].items(), key=lambda item: item[1])}
        book = person_book_value[reader].popitem()
        book_id = book[0]
        if book[1] != -1:
            if book_is_here(book_id, reader):
                position = get_forat(timeMat, reader, get_person_time(reader, book_id), 0, safe_list_get(llibre_no_disp, book_id))
                if position != -1:
                    pintar(timeMat, reader, position, get_person_time(reader, book_id))
                    llibre_no_disp.setdefault(book_id, (position, position + get_person_time(reader, book_id)))
                    read(book_id, reader)
            else:
                position = get_forat(timeMat, reader, dict(reader_book[reader]).get(book_id),distance(book_id, reader), safe_list_get(llibre_no_disp, book_id))
                if position != -1:
                    move(book_id, reader_library[reader])
                    llibre_no_disp.setdefault(book_id, (position - distance(book_id, reader), position + get_person_time(reader, book_id)))
                    pintar(timeMat, reader, position, get_person_time(reader, book_id))
                    read(book_id, reader)
        reorder(book_id)
        reader = selectNext()

def reorder(x):
    global person_book_value
    cont = 0
    for person in person_book_value:
        if dict(person).__contains__(x):
            dict(person).setdefault(x, calc_book_value(x, cont))
        cont += 1

processInput()
schedule()
writeOutput()
