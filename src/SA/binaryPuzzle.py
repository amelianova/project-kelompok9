import numpy as np
import random

# Parameter
n = 6  # Ukuran teka-teki
maxiter = 1000 # Jumlah iterasi maksimum
np.random.seed(0)
random.seed(0)

# Matriks teka-teki dengan posisi kosong diisi dengan None
problem = np.array([
    [1, None, None, 0, None, None],
    [None, None, 0, 0, None, 1],
    [None, 0, 0, None, None, 1],
    [None, None, None, None, None, None],
    [0, 0, None, 1, None, None],
    [None, 1, None, None, 0, 0]
], dtype=object)

# Fungsi mengisi tabel teka-teki dengan vektor jawaban
def fill_puzzle(puzzle, answer_vector):
    solution = np.copy(puzzle)
    index = 0
    for row in range(n):
        for col in range(n):
            if solution[row, col] is None:
                solution[row, col] = answer_vector[index]
                index += 1
    return solution

# Fungsi menghitung skor pelanggaran
def calculate_penalty(solution):
    penalty = 0

    # Skor pelanggaran untuk jumlah 0 dan 1 per kolom
    col_sums = np.sum(solution, axis=0)
    penalty += np.sum((col_sums - n // 2) ** 2)

    # Tiga simbol sama berurutan mendatar
    for row in range(n):
        for col in range(n - 2):
            if solution[row, col] == solution[row, col + 1] == solution[row, col + 2]:
                penalty += 30

    # Tiga simbol sama berurutan vertikal
    for col in range(n):
        for row in range(n - 2):
            if solution[row, col] == solution[row + 1, col] == solution[row + 2, col]:
                penalty += 30

    # Kolom yang sama persis
    for p in range(n - 1):
        for q in range(p + 1, n):
            if np.array_equal(solution[:, p], solution[:, q]):
                penalty += 30

    # Baris yang sama persis
    for p in range(n - 1):
        for q in range(p + 1, n):
            if np.array_equal(solution[p, :], solution[q, :]):
                penalty += 30

    return penalty

# Inisialisasi vektor jawaban
ones_needed = np.full(n, n // 2) - np.sum(problem == 1, axis=1)
zeros_needed = np.full(n, n // 2) - np.sum(problem == 0, axis=1)
answer_vector = np.concatenate([np.ones(int(ones_needed[i])) for i in range(n)] +
                               [np.zeros(int(zeros_needed[i])) for i in range(n)])
np.random.shuffle(answer_vector)

# Simulated Annealing
best_solution = fill_puzzle(problem, answer_vector)
best_penalty = calculate_penalty(best_solution)

for iteration in range(1, maxiter + 1):
    improved = False

    # Pertukaran dua elemen acak dalam answer_vector
    for i in range(len(answer_vector) - 1):
        for j in range(i + 1, len(answer_vector)):
            # Buat salinan baru dari answer_vector
            new_answer_vector = answer_vector.copy()
            new_answer_vector[i], new_answer_vector[j] = new_answer_vector[j], new_answer_vector[i]

            # Hitung solusi baru
            new_solution = fill_puzzle(problem, new_answer_vector)
            new_penalty = calculate_penalty(new_solution)

            # Print solusi pada iterasi ini
            print(f"Iterasi {iteration} - Penalti: {new_penalty}")

            # Simulated Annealing: Jika penalty baru lebih kecil atau berdasarkan probabilitas
            if new_penalty < best_penalty:
                answer_vector = new_answer_vector
                best_solution = new_solution
                best_penalty = new_penalty
                improved = True
                break
            else:
                # Probabilitas menerima solusi lebih buruk (simulated annealing)
                probability = best_penalty / (new_penalty * iteration)
                if random.random() < probability:
                    answer_vector = new_answer_vector
                    best_solution = new_solution
                    best_penalty = new_penalty
                    improved = True
                    break
        if improved:
            break

    # Jika menemukan solusi sempurna
    if best_penalty == 0:
        print(f"\nSolusi sempurna ditemukan pada iterasi {iteration}")
        print(best_solution.astype(int))
        break
else:
    print("\nTidak menemukan solusi sempurna, coba tambahkan iterasi")
    print(best_solution.astype(int))

    # Jika menemukan solusi sempurna
if best_penalty == 0:
        best_solution = best_solution.astype(int)  # Konversi elemen-elemen ke integer
        print(f"Solusi ditemukan pada iterasi {iteration}")
        print(best_solution)
else:
    best_solution = best_solution.astype(int)  # Konversi elemen-elemen ke integer
    print("Tidak menemukan solusi, coba tambahkan iterasi")
    print(best_solution)
