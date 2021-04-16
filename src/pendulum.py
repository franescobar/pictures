import numpy as np
import matplotlib.pyplot as plt

# Simulation parameters
l = 1
g = 9.81
m = 1

def xdot(t, x):
    ''' Model dynamics of a simple pendulum. '''

    # Unpack states
    theta1 = x[0]
    theta2 = x[1]
    ptheta1 = x[2]
    ptheta2 = x[3]

    # Compute derivatives
    theta1_dot = (6/(m*l**2))*(2*ptheta1 - 3*np.cos(theta1 - theta2)*ptheta2)\
                 /(16 - 9*np.cos(theta1 - theta2)**2)
    theta2_dot = (6/(m*l**2))*(8*ptheta2 - 3*np.cos(theta1 - theta2)*ptheta1)\
                 /(16 - 9*np.cos(theta1 - theta2)**2)
    ptheta1_dot = -0.5*m*l**2*(theta1_dot*theta2_dot*np.sin(theta1 - theta2)\
                               + (3*g/l)*np.sin(theta1))
    ptheta2_dot = -0.5*m*l**2*(-theta1_dot*theta2_dot*np.sin(theta1 - theta2)\
                               + (g/l)*np.sin(theta2))

    return np.array([theta1_dot, theta2_dot, ptheta1_dot, ptheta2_dot])

def RK4(fdot, f0, tf, t0=0, h=1e-2):
    ''' Implement a fourth-order Runge-Kutta method. '''

    t = np.arange(t0, tf, h)
    f = np.zeros([len(t), len(f0)])
    f[0] = f0

    for i in range(len(t) - 1):
        # Compute coefficients
        k1 = fdot(t[i], f[i])
        k2 = fdot(t[i] + h/2, f[i] + h*k1/2)
        k3 = fdot(t[i] + h/2, f[i] + h*k2/2)
        k4 = fdot(t[i] + h, f[i] + h*k3)
        # Compute and save next value
        f[i+1] = f[i] + (h/6)*(k1 + 2*k2 + 2*k3 + k4)

    return t, f

def write_data(t, x, filename, step='Unknown', header=''):
    ''' Write data to file so it can be parsed by LaTeX. '''

    with open(filename, 'w') as f:
        for (i, ti) in enumerate(t):
            # Write time
            line = '{' + str(ti) + '/'
            # Write states
            for xi in x[i, :]:
                line += str(xi) + '/'
            # Remove last comma and add linebreak
            line = line[:-1]
            if i == len(t) - 1:
                line += '}\n'
            else:
                line += '},\n'
            # Write line itself
            f.write(line)

# Initial conditions
theta1_0 = np.deg2rad(90)
theta2_0 = np.deg2rad(90)

x0 = [theta1_0, theta2_0, 0, 0]
tf = 15
t, x = RK4(xdot, x0, tf, h=0.02)
x[:, 0] = [np.rad2deg(theta) for theta in x[:, 0]]
x[:, 1] = [np.rad2deg(theta) for theta in x[:, 1]]
theta1 = x[:, 0]
theta2 = x[:, 1]
plt.plot(t, theta1)
plt.plot(t, theta2)
plt.show()
write_data(t, x, 'data.txt')
