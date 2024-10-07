import numpy as np
import pyLOM
from pathlib import Path
import torch

# u = torch.rand(100, 120)
# v = torch.rand(100, 120)
u = (torch.arange(0, 20).float()).repeat(10, 1)
v = (torch.arange(0, 20).float()).repeat(10, 1)
print(u.shape, v.shape)
print(u[0], v[0], u[:, 0])
mesh_shape = (2, 5)
dataset = pyLOM.NN.Dataset(variables_out=(u, v), mesh_shape=mesh_shape)
print(len(dataset))
x = dataset[:2]
print(x.shape)
x = dataset[:]
print(x.shape)
u1, v1 = dataset[3]
print(u1, v1)
# u1 = dataset[0]
# print(u1)

DATASET_DIR = Path("/home/david/Desktop/Datos_DLR_pylom")

input_scaler = pyLOM.NN.MinMaxScaler()
output_scaler = pyLOM.NN.MinMaxScaler()   

def load_dataset(path):
    original_dataset = pyLOM.Dataset.load(path)
    # x = original_dataset.xyz[:,0]
    # cp = original_dataset["CP"][:, 0]
    # plt.scatter(x, cp[:597], s=1, label='trainañdbsdgh')
    
    # print(original_dataset.fieldnames, original_dataset.varnames, len(original_dataset.get_variable('AoA')), len(original_dataset.get_variable('Mach')))
    # print(original_dataset["CP"].shape, original_dataset["CP"].max(), original_dataset.xyz.shape, original_dataset.xyz.min(), original_dataset.xyz.max())

    # print(len([*zip(original_dataset.get_variable('AoA'), original_dataset.get_variable('Mach'))]), torch.tensor([*zip(original_dataset.get_variable('AoA'), original_dataset.get_variable('Mach'))]).shape)
    # import sys; sys.exit() 
    # print([*zip(original_dataset.get_variable('AoA'), original_dataset.get_variable('Mach'))])
    dataset = pyLOM.NN.Dataset(
        variables_out=(original_dataset["CP"], original_dataset["CP"]), # CUIDADO CON ESTO. TIENE QUE VER EN COMO TORCH HACE EL RESHAPE, SE ITRERA PRIMERO FOR FILAS Y DE AHI YA SALE MAL
        variables_in=original_dataset.xyz,
        parameters=[[*zip(original_dataset.get_variable('AoA'), original_dataset.get_variable('Mach'))]], # , original_dataset.get_variable('Mach')
        # parameters=[original_dataset.get_variable('AoA'), original_dataset.get_variable("Mach")],
        inputs_scaler=input_scaler,
        outputs_scaler=output_scaler,
    )
    return dataset

dataset_train = load_dataset(DATASET_DIR / "TRAIN.h5")
x, y = dataset_train[:]
print(x.shape, y.shape)
print(y[:10])
import sys; sys.exit(0)

# x = x[:597, 0]
# cp = y[:597]
# plt.scatter(x, cp, s=1, label='train')
# plt.legend()
# plt.savefig('asd.png')
# import sys; sys.exit()
dataset_test = load_dataset(DATASET_DIR / "TEST.h5")
val_dataset = load_dataset(DATASET_DIR / "VAL.h5")
print(len(dataset_train), len(dataset_test), len(val_dataset))

x, y = dataset_train[:]
print(x.min(dim=0), x.max(dim=0), y.min(dim=0), y.max(dim=0), x.shape, y.shape)
x, y = dataset_test[:]
print(x.min(), x.max(), y.min(), y.max(), x.shape, y.shape)
x, y = val_dataset[:]
print(x.min(), x.max(), y.min(), y.max(), x.shape, y.shape)


optimizer = pyLOM.NN.OptunaOptimizer(
    optimization_params={
        "lr": 0.0005,  # fixed parameter
        "n_layers": (1, 4),  # optimizable parameter,
        "batch_size": (128, 512),
        "hidden_size": 256,
        "epochs": 30,
    },
    n_trials=10,
    direction="minimize",
    pruner=None,
    save_dir=None,
)

pipeline = pyLOM.NN.Pipeline(
    train_dataset=dataset_train,
    test_dataset=dataset_test,
    valid_dataset=val_dataset,
    optimizer=optimizer,
    model_class=pyLOM.NN.MLP,
)

pipeline.run()
# check saving and loading the model
pipeline.model.save("model.pth")
model = pyLOM.NN.MLP.load("model.pth")

preds = model.predict(dataset_test, batch_size=2048)
scaled_preds = output_scaler.inverse_transform([preds])[0]
scaled_y = output_scaler.inverse_transform([dataset_test[:][1]])[0]
# check that the scaling is correct
print(scaled_y.min(), scaled_y.max())

print(f"MAE: {np.abs(scaled_preds - np.array(scaled_y)).mean()}")
print(f"MRE: {np.abs(scaled_preds - np.array(scaled_y)).mean() / abs(np.array(scaled_y).mean() + 1e-6)}")