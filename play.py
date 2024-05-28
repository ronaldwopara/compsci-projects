import numpy as np

# Convert a list to a NumPy array using np.asarray()
my_list = [1, 2, 3, 4, 5]
my_array = np.asarray(my_list)
print(my_array)

# Convert a tuple to a NumPy array
my_tuple = (6, 7, 8, 9, 10)
my_array_from_tuple = np.asarray(my_tuple)
print(my_array_from_tuple)

# Check if np.asarray() returns a view or a copy
my_array_view = np.asarray(my_array)
print(my_array is my_array_view)  # True (view of the same array)
