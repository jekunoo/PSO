import random
import math

# Fungsi f(x, y)
def func(x, y):
    return 10 + (2 * x**2) - 4 * math.cos(2 * math.pi * x) + y**2 - 4 * math.cos(2 * math.pi * y)

# Inisialisasi variabel
n_particles = 10
xi = [random.uniform(-5, 5) for _ in range(n_particles)]
yi = [random.uniform(-5, 5) for _ in range(n_particles)]
xi_before = [0] * n_particles
yi_before = [0] * n_particles
vix = [0] * n_particles
viy = [0] * n_particles

# Parameter
c1, c2 = 1, 0.5
w = 1
r1, r2 = random.random(), random.random()
Pbestix, Pbestiy = xi[:], yi[:]
Gbestx, Gbesty = 0, 0

# Cari Gbest (partikel dengan nilai fungsi terkecil)
def find_gbest(xi, yi):
    global Gbestx, Gbesty
    f_values = [func(x, y) for x, y in zip(xi, yi)]
    min_index = f_values.index(min(f_values))
    Gbestx, Gbesty = xi[min_index], yi[min_index]

# Update Pbest
def update_pbest(xi, yi, xi_before, yi_before):
    global Pbestix, Pbestiy
    for i in range(n_particles):
        if func(xi[i], yi[i]) < func(xi_before[i], yi_before[i]):
            Pbestix[i], Pbestiy[i] = xi[i], yi[i]
        else:
            Pbestix[i], Pbestiy[i] = xi_before[i], yi_before[i]

# Update kecepatan dan posisi
def update_velocity_position(xi, yi, vix, viy):
    for i in range(n_particles):
        vix[i] = w * vix[i] + c1 * r1 * (Pbestix[i] - xi[i]) + c2 * r2 * (Gbestx - xi[i])
        viy[i] = w * viy[i] + c1 * r1 * (Pbestiy[i] - yi[i]) + c2 * r2 * (Gbesty - yi[i])
        xi[i] += vix[i]
        yi[i] += viy[i]

# Jumlah iterasi
n_iter = int(input("Masukkan jumlah iterasi: "))

# Loop iterasi
for iteration in range(n_iter):
    print(f"\nIterasi ke-{iteration + 1}")
    for i in range(n_particles):
        print(f"Partikel {i + 1}: x = {xi[i]:.4f}, y = {yi[i]:.4f}, f(x, y) = {func(xi[i], yi[i]):.4f}")

    # Cari Gbest
    find_gbest(xi, yi)

    # Update Pbest
    if iteration > 0:
        update_pbest(xi, yi, xi_before, yi_before)

    # Update kecepatan dan posisi
    update_velocity_position(xi, yi, vix, viy)

    # Simpan posisi saat ini sebagai xi_before dan yi_before
    xi_before, yi_before = xi[:], yi[:]

print(f"\nHasil akhir: \nGbestx = {Gbestx:.4f}\nGbesty = {Gbesty:.4f}\nf(Gbestx, Gbesty) = {func(Gbestx, Gbesty):.4f}")
