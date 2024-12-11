# Example how to compute the connectivity between elements in a mesh

import numpy as np
import h5py
import pyLOM

# Substitute with your own path to h5 clean file
filepath = '/home/data/NEW/clean.h5'

d = pyLOM.Dataset.load(filepath)
mesh = pyLOM.Mesh.load(filepath)

normals = d.fields['Normals']['value'].reshape((-1, 3))

print("Tamaño de la malla: ", mesh.ncells)

connecc = mesh.centers_connectivity(normals, radius_factor=10.)
print(connecc[:5])

# # Save the connectivity to a file
with h5py.File('connectivity.h5', 'w') as f: 
    f.create_dataset('connectivity', data=connecc)

# Check the connectivity of some random cells

test_idx = np.array([0, 170889, 89579, 159747, 703309, 1692167, 1676293, 838062, 423623, 202415])
test_cells_connectivity = connecc[test_idx]

# This hardcoded values are the true connectivities for the clean.h5 file mesh
true_connectivities = np.array(
    [[298, 302, -1],
     [170116, 171358, 171367],
     [88979, 89966, 89980],
     [159197, 159789, 160164],
     [702956, 703214, 703725],
     [1692059, 1692182, 1692246],
     [1676134, 1676262, 1676475],
     [835490, 835541, 841486],
     [423202, 423711, 423934],
     [201851, 202611, 202892]]
)

# Sort the connectivities in order to compare them
test_cells_connectivity = np.sort(test_cells_connectivity, axis=1)
true_connectivities = np.sort(true_connectivities, axis=1)

print("Connectivity is correct: ", np.all(test_cells_connectivity == true_connectivities))

pyLOM.cr_info()