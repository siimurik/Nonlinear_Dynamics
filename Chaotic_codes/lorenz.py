import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D
from scipy.integrate import odeint

# Lorenz system parameters
sigma = 10.0
rho = 28.0
beta = 8.0 / 3.0

# Lorenz system equations
def lorenz_system(state, t):
    x, y, z = state
    dxdt = sigma * (y - x)
    dydt = x * (rho - z) - y
    dzdt = x * y - beta * z
    return [dxdt, dydt, dzdt]

# Initial conditions for multiple points
num_points = 10
initial_states = [np.random.rand(3) * 10 for _ in range(num_points)]

# Time points
t = np.linspace(0, 40, 4000)

# Solve the Lorenz system for each initial condition
solutions = [odeint(lorenz_system, initial_state, t) for initial_state in initial_states]

# Create the figure and 3D axis
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Initialize lines and points for each trajectory
lines = [ax.plot([], [], [], lw=0.5)[0] for _ in range(num_points)]
points = [ax.plot([], [], [], 'o')[0] for _ in range(num_points)]

# Setting the axes properties
ax.set_xlim((-25, 25))
ax.set_ylim((-35, 35))
ax.set_zlim((5, 55))
ax.set_xlabel("X Axis")
ax.set_ylabel("Y Axis")
ax.set_zlabel("Z Axis")
ax.set_title("Lorenz Attractor Animation")

# Initialization function: plot the background of each frame
def init():
    for line, point in zip(lines, points):
        line.set_data([], [])
        line.set_3d_properties([])
        point.set_data([], [])
        point.set_3d_properties([])
    return lines + points

# Animation function: this is called sequentially
def animate(i):
    for line, point, solution in zip(lines, points, solutions):
        x, y, z = solution[:i].T
        line.set_data(x, y)
        line.set_3d_properties(z)
        point.set_data(x[-1:], y[-1:])
        point.set_3d_properties(z[-1:])
    ax.view_init(30, 0.3 * i)
    fig.canvas.draw()
    return lines + points

# Create the animation
ani = animation.FuncAnimation(fig, animate, init_func=init, frames=400, interval=20, blit=False)

plt.show()

# To save the animation, uncomment the following lines:
# Writer = animation.writers['ffmpeg']
# writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)
# ani.save('lorenz_attractor.mp4', writer=writer)
