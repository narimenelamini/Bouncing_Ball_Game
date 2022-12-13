import matplotlib.pyplot as plt
import numpy as np

# Generate a grid of x and y values
x = np.linspace(-10, 10, 100)
y = np.linspace(-10, 10, 100)
xx, yy = np.meshgrid(x, y)

# Evaluate the function
z = xx**2 + yy**2

# Plot the results
plt.contour(x, y, z)
plt.show()
