import json

class Cell:
    def __init__(self, value=-1):
        self.domain = [1, 0] if value == -1 else [value]
        self.value = value
        self.satisfied = value != -1
        self.maclist = []

# Puzzle yang akan dipecahkan
mypuzzle = [
    ["1", "-", "-", "0", "-", "-"],
    ["-", "-", "0", "0", "-", "1"],
    ["-", "0", "0", "-", "-", "1"],
    ["-", "-", "-", "-", "-", "-"],
    ["0", "0", "-", "1", "-", "-"],
    ["-", "1", "-", "-", "0", "0"]
]

# Inisialisasi variabel
mygraph = dict()
unique_r = dict()
unique_c = dict()
steps = []
startPuzzle = []

n = 6  # Ukuran puzzle 6x6

# Inisialisasi mygraph dengan cell kosong atau nilai awal dari mypuzzle
for i in range(n):
    for j in range(n):
        if mypuzzle[i][j] == '-':
            mygraph[(i, j)] = Cell(-1)
        else:
            mygraph[(i, j)] = Cell(int(mypuzzle[i][j]))

for i in range(n):
    unique_r[i] = None
    unique_c[i] = None

def updatestr(graph, n, row=None, column=None):
    if row is None and column is None:
        for i in range(n):
            mystr = ''.join(str(graph[(i, j)].value) for j in range(n) if graph[(i, j)].value != -1)
            unique_r[i] = mystr if len(mystr) == n else None

        for j in range(n):
            mystr = ''.join(str(graph[(i, j)].value) for i in range(n) if graph[(i, j)].value != -1)
            unique_c[j] = mystr if len(mystr) == n else None
    else:
        row_str = ''.join(str(graph[(row, j)].value) for j in range(n) if graph[(row, j)].value != -1)
        unique_r[row] = row_str if len(row_str) == n else None

        col_str = ''.join(str(graph[(i, column)].value) for i in range(n) if graph[(i, column)].value != -1)
        unique_c[column] = col_str if len(col_str) == n else None

def check_constraints(graph, n, x, y):
    row = [graph[(x, j)].value for j in range(n)]
    col = [graph[(i, y)].value for i in range(n)]

    # Jumlah angka 1 dan 0 tidak boleh melebihi setengah ukuran n
    if row.count(1) > n // 2 or row.count(0) > n // 2:
        return False
    if col.count(1) > n // 2 or col.count(0) > n // 2:
        return False

    # Tidak boleh ada tiga angka berturut-turut yang sama di baris atau kolom
    for j in range(n - 2):
        if row[j] == row[j + 1] == row[j + 2] != -1:
            return False
    for i in range(n - 2):
        if col[i] == col[i + 1] == col[i + 2] != -1:
            return False

    # Baris dan kolom harus unik
    row_string = ''.join(str(val) for val in row if val != -1)
    col_string = ''.join(str(val) for val in col if val != -1)

    for i in range(n):
        if i != x and row_string == unique_r.get(i):
            return False
        if i != y and col_string == unique_c.get(i):
            return False

    return True

def MRV(graph, n):
    x, y = -1, -1
    min_len_domain = 3
    for i in range(n):
        for j in range(n):
            if graph[(i, j)].value == -1:
                if len(graph[(i, j)].domain) < min_len_domain:
                    min_len_domain = len(graph[(i, j)].domain)
                    x, y = i, j
    return x, y

def backtracking(graph, n):
    if is_complete(graph, n):
        return graph

    (x, y) = MRV(graph, n)
    for d in graph[(x, y)].domain:
        graph[(x, y)].value = d
        steps.append([x, y, d])
        updatestr(graph, n, x, y)

        if check_constraints(graph, n, x, y):
            done = backtracking(graph, n)
            if done:
                return graph

        graph[(x, y)].value = -1
        updatestr(graph, n, x, y)
        steps.append([x, y, -1])

    return None

def is_complete(graph, n):
    return all(graph[(i, j)].value != -1 for i in range(n) for j in range(n))

def init(graph, n):
    for i in range(n):
        for j in range(n):
            if graph[(i, j)].value != -1:
                startPuzzle.append([i, j, graph[(i, j)].value])
                if not check_constraints(graph, n, i, j):
                    return False
    return True

# Menjalankan fungsi utama untuk menyelesaikan puzzle dan mencetak hasilnya
def main():
    init(mygraph, n)
    g = backtracking(mygraph, n)
    has_answer = g is not None

    if has_answer:
        print("Solusi Binary Puzzle:")
        for i in range(n):
            print(' '.join(str(g[(i, j)].value) for j in range(n)))
    else:
        print("The puzzle doesn't have any solution!")

    return json.dumps({
        "steps": steps,
        "puzzle": startPuzzle,
        "len": n,
        "hasAnswer": has_answer
    })

# Run the main function
main()

