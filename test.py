import time
import random

# Create hashmaps of different sizes
small_dict = {i: i * 2 for i in range(1000)}
large_dict = {i: i * 2 for i in range(1000000)}

start = time.time()
for i in range(100000):
    small_index = random.randint(0, 999)
    value = small_dict[small_index] + 1
print("small: ", (time.time() - start))
    
start = time.time()
for i in range(100000):
    large_index = random.randint(0, 999999)
    value = large_dict[large_index] + 1
print("large: ", (time.time() - start))

