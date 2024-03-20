from print_tricks import pt
pt.easy_imports()
pt.easy_testing(__name__)


# from ursina import *

# app = Ursina(size=(1920,1080), development_mode=True)

# e = Entity(name='e', model='cube', texture='white_cube')
# pt(e.name)

# EditorCamera()
# app.run()



''' testing python floats to ints conversion vs vectorized using numpy (or open3d tensor.to())

'''

import numpy as np
import time

# Create a list of 1 million floats
float_list = [float(i) for i in range(1_000_000)]

# Convert using a loop
start_time = time.time()
int_list = [int(f) for f in float_list]
end_time = time.time()
print(f"List conversion took {end_time - start_time} seconds.")

# Convert using NumPy (similar to what you'd do with Open3D tensors)
start_time2 = time.time()
float_array = np.array(float_list, dtype=np.float32)
int_array = float_array.astype(np.int32)
end_time2 = time.time()
print(f"NumPy conversion took {end_time2 - start_time2} seconds.")

print(f"The numpy version was {(end_time - start_time) / (end_time2 - start_time2)} times faster than the python loop")


import open3d as o3d
import open3d.core as o3c
g = o3c.Tensor([0, 1, 2])

# import open3d as o3c
# import numpy as np
# import time

# # Create a numpy array of 1 million floats
# float_list = np.array([float(i) for i in range(1_000_000)], dtype=np.float32)

# # Convert numpy array to Open3D tensor on CPU
# float_tensor = o3c.Tensor.from_numpy(float_list)

# # Convert using Open3D tensor (CPU)
# start_time = time.time()
# int_tensor = float_tensor.to(o3c.Dtype.Int32)
# end_time = time.time()
# print(f"Open3D CPU conversion took {end_time - start_time} seconds.")



# # Assuming Open3D with CUDA support and a compatible GPU is available
# # Convert numpy array to Open3D tensor on GPU
# float_tensor_gpu = o3c.Tensor.from_numpy(float_list, device=o3c.Device("CUDA:0"))

# # Convert using Open3D tensor (GPU)
# start_time = time.time()
# int_tensor_gpu = float_tensor_gpu.to(o3c.Dtype.Int32)
# end_time = time.time()
# print(f"Open3D GPU conversion took {end_time - start_time} seconds.")