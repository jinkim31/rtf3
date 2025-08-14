import numpy as np
import matplotlib.pyplot as plt
from rtf3 import *

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

Rotation3().draw_pyplot(ax, size=3)
r = Rotation3.from_euler_zyx_deg(0, 0, 0)
r.draw_pyplot(ax, size=2)

# Set axes limits
ax.set_xlim([-5, 5])
ax.set_ylim([-5, 5])
ax.set_zlim([-5, 5])
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.show()