import numpy as np
import random

# Fungsi objektif yang akan diminimumkan
def objective_function(x):
    return 3 * x**3 + 2 * x**2 - 14

# Class Particle
class Particle:
    def __init__(self, position, velocity):
        self.position = position  # Posisi partikel saat ini
        self.velocity = velocity  # Kecepatan partikel saat ini
        self.pbest_position = position  # Posisi terbaik partikel
        self.pbest_value = float('inf')  # Nilai fungsi terbaik partikel

    def update_velocity(self, W, c1, c2, gbest_position):
        r1 = random.random()  # Nilai random untuk perhitungan kognitif
        r2 = random.random()  # Nilai random untuk perhitungan sosial
        
        # Perhitungan komponen kecepatan
        cognitive = c1 * r1 * (self.pbest_position - self.position)
        social = c2 * r2 * (gbest_position - self.position)
        self.velocity = W * self.velocity + cognitive + social

    def update_position(self, bounds):
        # Update posisi partikel
        self.position += self.velocity
        # Pastikan posisi berada dalam batas [0, 4]
        self.position = max(bounds[0], min(self.position, bounds[1]))

# Class Swarm
class Swarm:
    def __init__(self, num_particles, bounds, function, W=1, c1=0.5, c2=0.5):
        self.num_particles = num_particles  # Jumlah partikel
        self.bounds = bounds  # Batas posisi partikel
        self.function = function  # Fungsi objektif
        self.W = W  # Inertia weight
        self.c1 = c1  # Koefisien kognitif
        self.c2 = c2  # Koefisien sosial
        self.gbest_position = None  # Posisi global terbaik
        self.gbest_value = float('inf')  # Nilai fungsi global terbaik
        self.particles = []  # Daftar partikel

        # Inisialisasi partikel
        for _ in range(num_particles):
            position = random.uniform(bounds[0], bounds[1])
            velocity = random.uniform(-abs(bounds[1] - bounds[0]), abs(bounds[1] - bounds[0]))
            self.particles.append(Particle(position, velocity))

    def optimize(self, max_iterations):
        for iteration in range(max_iterations):
            for particle in self.particles:
                # Hitung nilai fungsi di posisi partikel saat ini
                fitness = self.function(particle.position)
                
                # Update posisi terbaik partikel (pbest)
                if fitness < particle.pbest_value:
                    particle.pbest_value = fitness
                    particle.pbest_position = particle.position
                
                # Update posisi global terbaik (gbest)
                if fitness < self.gbest_value:
                    self.gbest_value = fitness
                    self.gbest_position = particle.position

            # Update velocity dan position semua partikel
            for particle in self.particles:
                particle.update_velocity(self.W, self.c1, self.c2, self.gbest_position)
                particle.update_position(self.bounds)

            print(f"Iteration {iteration+1}: Best Position = {self.gbest_position}, Best Value = {self.gbest_value}")

# Parameter
num_particles = 10  # Jumlah partikel
bounds = [0, 4]  # Rentang posisi x
max_iterations = 3  # Jumlah iterasi

# Jalankan optimasi
swarm = Swarm(num_particles, bounds, objective_function)
swarm.optimize(max_iterations)

# Implementasi di luar class
print("\nFinal Result:")
print(f"Global Best Position: {swarm.gbest_position}")
print(f"Global Best Value: {swarm.gbest_value}")
