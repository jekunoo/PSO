import random

def func(x):
    return (3 * x**3) + (2 * x**2) - 14

# Inisialisasi nilai awal
particles = {f"x{i+1}": random.uniform(0, 4) for i in range(10)}
velocities = {f"v{i+1}": 0 for i in range(10)}
particles_prev = particles.copy()
c1, c2, w = 0.5, 1, 1
r1, r2 = random.random(), random.random()
Pbesti = []
Gbest = None

# Fungsi untuk menemukan nilai Gbest
def find_gbest(particles):
    return min(particles.values(), key=lambda x: func(x))

# Fungsi untuk memperbarui nilai Pbesti
def update_pbesti(particles, particles_prev):
    return [min(particles[f"x{i+1}"], particles_prev[f"x{i+1}"], key=func) for i in range(10)]

# Fungsi untuk menghitung nilai vi
def update_velocity(vi, xi, pbest, gbest):
    return w * vi + c1 * r1 * (pbest - xi) + c2 * r2 * (gbest - xi)

# Fungsi utama iterasi PSO
n = int(input("Masukkan Jumlah Iterasi: "))
for index in range(n):
    print(f"Iterasi ke-{index+1}")
    
    # Hitung nilai Gbest
    Gbest = find_gbest(particles)

    # Perbarui nilai Pbesti
    if index == 0:
        Pbesti = list(particles.values())
    else:
        Pbesti = update_pbesti(particles, particles_prev)

    print(f"Gbest: {Gbest}, Minimum f(x): {func(Gbest)}")

    # Perbarui kecepatan dan posisi
    for i in range(10):
        key_x = f"x{i+1}"
        key_v = f"v{i+1}"
        velocities[key_v] = update_velocity(velocities[key_v], particles[key_x], Pbesti[i], Gbest)
        particles_prev[key_x] = particles[key_x]
        particles[key_x] += velocities[key_v]
