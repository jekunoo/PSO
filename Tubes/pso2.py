import numpy as np
import random
import matplotlib.pyplot as plt

# Fungsi objektif yang akan diminimumkan (f(x, y))
def objective_function(position):
    x, y = position  # Pisahkan x dan y dari posisi
    return 10 + 2 * x**2 - 4 * np.cos(2 * np.pi * x) + y**2 - 4 * np.cos(2 * np.pi * y)

# Class Particle
class Particle:
    def __init__(self, position, velocity):
        self.position = position  # Posisi partikel saat ini [x, y]
        self.velocity = velocity  # Kecepatan partikel saat ini [vx, vy]
        self.pbest_position = position  # Posisi terbaik partikel
        self.pbest_value = float('inf')  # Nilai fungsi terbaik partikel

    def update_velocity(self, W, c1, c2, gbest_position):
        r1 = random.random()  # Nilai random untuk perhitungan kognitif
        r2 = random.random()  # Nilai random untuk perhitungan sosial

        # Perhitungan komponen kecepatan
        cognitive = c1 * r1 * (np.array(self.pbest_position) - np.array(self.position))
        social = c2 * r2 * (np.array(gbest_position) - np.array(self.position))
        self.velocity = W * np.array(self.velocity) + cognitive + social

    def update_position(self, bounds):
        # Update posisi partikel
        self.position = np.array(self.position) + self.velocity

        # Pastikan posisi berada dalam batas [-5, 5] untuk x dan y
        self.position = np.clip(self.position, bounds[0], bounds[1])

# Class Swarm
class Swarm:
    def __init__(self, num_particles, bounds, function, W=1, c1=0.5, c2=0.5):
        self.num_particles = num_particles  # Jumlah partikel
        self.bounds = bounds  # Batas posisi partikel [-5, 5] untuk x dan y
        self.function = function  # Fungsi objektif
        self.W = W  # Inertia weight
        self.c1 = c1  # Koefisien kognitif
        self.c2 = c2  # Koefisien sosial
        self.gbest_position = None  # Posisi global terbaik
        self.gbest_value = float('inf')  # Nilai fungsi global terbaik
        self.particles = []  # Daftar partikel
        self.history = []  # Untuk menyimpan posisi partikel tiap iterasi

        # Inisialisasi partikel
        for _ in range(num_particles):
            position = [random.uniform(bounds[0], bounds[1]), random.uniform(bounds[0], bounds[1])]
            velocity = [random.uniform(-abs(bounds[1] - bounds[0]), abs(bounds[1] - bounds[0])),
                        random.uniform(-abs(bounds[1] - bounds[0]), abs(bounds[1] - bounds[0]))]
            self.particles.append(Particle(position, velocity))

    def optimize(self, max_iterations):
        for iteration in range(max_iterations):
            print(f"\nIteration {iteration + 1}")
            print(f"{'Particle':<10} {'x':<10} {'y':<10} {'vx':<10} {'vy':<10} {'pBest_x':<10} {'pBest_y':<10} {'pBest_value':<15} {'gBest_value':<15}")
            print("=" * 100)

            iteration_positions = []  # Untuk menyimpan posisi partikel pada iterasi ini

            for idx, particle in enumerate(self.particles):
                # Hitung nilai fungsi di posisi partikel saat ini
                fitness = self.function(particle.position)

                # Update posisi terbaik partikel (pbest)
                if fitness < particle.pbest_value:
                    particle.pbest_value = fitness
                    particle.pbest_position = particle.position.copy()

                # Update posisi global terbaik (gbest)
                if fitness < self.gbest_value:
                    self.gbest_value = fitness
                    self.gbest_position = particle.position.copy()

                # Cetak data partikel dalam iterasi ini
                x, y = particle.position
                vx, vy = particle.velocity
                pBest_x, pBest_y = particle.pbest_position
                print(f"{idx + 1:<10} {x:<10.4f} {y:<10.4f} {vx:<10.4f} {vy:<10.4f} {pBest_x:<10.4f} {pBest_y:<10.4f} {particle.pbest_value:<15.4f} {self.gbest_value:<15.4f}")

                # Simpan posisi partikel
                iteration_positions.append(particle.position)

            # Simpan posisi partikel untuk visualisasi
            self.history.append(iteration_positions)

            # Visualisasi setiap kelipatan 10 iterasi
            if (iteration + 1) % 10 == 0:
                self.visualize_plot(iteration + 1)

            # Update velocity dan position semua partikel
            for particle in self.particles:
                particle.update_velocity(self.W, self.c1, self.c2, self.gbest_position)
                particle.update_position(self.bounds)

    def print_history(self):
        print(f"{'Iteration':<10} {'Particle':<10} {'Position':<10} {'Velocity':<10} {'pBest':<15} {'gBest':<15}")
        print("=" * 70)

        for data in self.history:
            iteration = data["iteration"]
            gBest = data["gBest"]

            for idx, p in enumerate(data["particles"]):
                print(f"{iteration:<10} {idx+1:<10} {p['position']:<10.4f} {p['velocity']:<10.4f} "
                      f"{p['pBest']:<15.4f} {gBest:<15.4f}")
            print("-" * 70)

    def visualize_plot(self, iteration):
        particle_positions_x = []
        particle_positions_y = []
        gbest_positions_x = []
        gbest_positions_y = []

        # Flatten history to collect all positions and highlight gbest per iteration
        for i, iteration_positions in enumerate(self.history):
            for position in iteration_positions:
                particle_positions_x.append(position[0])
                particle_positions_y.append(position[1])
            # Add the gbest position for each iteration
            gbest_positions_x.append(self.gbest_position[0])
            gbest_positions_y.append(self.gbest_position[1])

        # Plotting
        plt.figure(figsize=(8, 6))

        # Plot all particle positions
        plt.scatter(particle_positions_x, particle_positions_y, color='blue', label='Particle Positions')

        # Highlight the final global best position
        plt.scatter(self.gbest_position[0], self.gbest_position[1], color='red', s=100, label='Global Best')

        # Additional plot details
        plt.title(f"Particle Positions and Global Best at Iteration {iteration}")
        plt.xlabel("Position X")
        plt.ylabel("Position Y")
        plt.legend()
        plt.grid()
        plt.show()

# Parameter
num_particles = 10  # Jumlah partikel
bounds = [-5, 5]  # Rentang posisi x dan y [-5, 5]
max_iterations = 20  # Jumlah iterasi

# Jalankan optimasi
swarm = Swarm(num_particles, bounds, objective_function)
swarm.optimize(max_iterations)

# Implementasi di luar class
print("\nFinal Result:")
print(f"Global Best Position: {swarm.gbest_position}")
print(f"Global Best Value: {swarm.gbest_value}")
