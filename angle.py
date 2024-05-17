import matplotlib.pyplot as plt
import numpy as np
import math


def angle(P1, P2):
    P1_v = [P1[0], P1[1] + 1]
    ang1 = math.atan2(P1_v[1] - P1[1], P1_v[0] - P1[0])
    ang2 = math.atan2(P2[1] - P1[1], P2[0] - P1[0])
    return np.rad2deg((ang1 - ang2) % (2 * np.pi))


def plot_vectors_and_angles(P1, P2):
    fig, ax = plt.subplots()

    # Plot points
    ax.scatter(*P1, color='red', marker='o', label='P1')
    ax.scatter(*P2, color='green', marker='o', label='P2')

    # Plot horizontal vector from P1
    ax.arrow(*P1, 1, 0, color='blue', head_width=0.1, label='P1_v')

    # Plot vector from P1 to P2
    ax.arrow(*P1, P2[0] - P1[0], P2[1] - P1[1], color='orange', head_width=0.1, label='P1P2')

    # Calculate angle
    angle_deg = round(angle(P1, P2), 2)

    # Plot angle arc
    x_mid = (P1[0] + P2[0]) / 2
    y_mid = (P1[1] + P2[1]) / 2
    ax.annotate('', xy=P2, xytext=P1, xycoords='data',
                arrowprops=dict(arrowstyle="->,head_width=0.1", color='black', shrinkA=0, shrinkB=0))
    ax.text(x_mid, y_mid, f'{angle_deg}°', ha='center', va='center')

    # Set limits
    ax.set_xlim(min(P1[0], P2[0]) - 1, max(P1[0], P2[0]) + 1)
    ax.set_ylim(min(P1[1], P2[1]) - 1, max(P1[1], P2[1]) + 1)

    # Show grid and legend
    ax.grid(True)
    ax.legend()

    plt.show()


# Example points
P1 = (16, 0)
P2 = (28, 14)

plot_vectors_and_angles(P1, P2)
