import matplotlib.pyplot as plt
import pandas as pd
from django.conf import settings


def plot_moisture(json_file, plot_img_name):
    df = pd.read_json(settings.PARCEL_FOLDER + json_file)
    df = df.transpose()

    # dataframe Naraja
    df_naranja = pd.json_normalize(df.naranja)
    number_naranja = df_naranja.loc[:, 'porcent']
    numbers_naranja = number_naranja.values

    df_amarillo = pd.json_normalize(df.amarillo)
    number_amarillo = df_amarillo.loc[:, 'porcent']
    numbers_amarillo = number_amarillo.values

    df_verdes = pd.json_normalize(df.verdes)
    number_verdes = df_verdes.loc[:, 'porcent']
    numbers_verdes = number_verdes.values

    df_azul_claro = pd.json_normalize(df.azul_claro)
    number_azul_claro = df_azul_claro.loc[:, 'porcent']
    numbers_azul_claro = number_azul_claro.values

    df_azul_medio = pd.json_normalize(df.azul_medio)
    number_azul_medio = df_azul_medio.loc[:, 'porcent']
    numbers_azul_medio = number_azul_medio.values

    df_azul_oscuro = pd.json_normalize(df.azul_oscuro)
    number_azul_oscuro = df_azul_oscuro.loc[:, 'porcent']
    numbers_azul_oscuro = number_azul_oscuro.values

    df_nubes = pd.json_normalize(df.nubes)
    number_nubes = df_nubes.loc[:, 'porcent']
    numbers_nubes = number_nubes.values

    df_naranja["nfecha"] = df["nombre"].astype(str) + ' - ' + df["fecha"]
    df_naranja['nombre'] = df[['nombre']]
    number_nombre = df_naranja.loc[:, 'nfecha']
    numbers_nombre = number_nombre.values

    dataframe = pd.DataFrame({'Naranja': numbers_naranja, 'Amarillo': numbers_amarillo, 'Verdes': numbers_verdes,
                              'Azul claro': numbers_azul_claro, 'Azul medio': numbers_azul_medio,
                              'Azul oscuro': numbers_azul_oscuro, 'Nubes': numbers_nubes}, index=numbers_nombre)
    axis = dataframe.plot(kind="barh",
                          color=['#ff8000', '#ffdf00', '#66ff98', '#02fefc', '#0087ff', '#2000ff', '#9901c4'])
    print(axis)
    plt.savefig(settings.PARCEL_FOLDER + plot_img_name, bbox_inches='tight')
    plt.close()


def plot_ndvi(json_file, plot_img_name):
    df = pd.read_json(settings.PARCEL_FOLDER + json_file)
    df = df.transpose()

    df_azules = pd.json_normalize(df.azules)
    number_azules_altos = df_azules.loc[:, 'altos.porcent']
    numbers_azules_altos = number_azules_altos.values

    number_azules_medios = df_azules.loc[:, 'medios.porcent']
    numbers_azules_medios = number_azules_medios.values

    number_azules_bajos = df_azules.loc[:, 'bajos.porcent']
    numbers_azules_bajos = number_azules_bajos.values

    df_amarillos = pd.json_normalize(df.amarillos)
    number_amarillos_altos = df_amarillos.loc[:, 'altos.porcent']
    numbers_amarillos_altos = number_amarillos_altos.values

    number_amarillos_medios = df_amarillos.loc[:, 'medios.porcent']
    numbers_amarillos_medios = number_amarillos_medios.values

    number_amarillos_bajos = df_amarillos.loc[:, 'bajos.porcent']
    numbers_amarillos_bajos = number_amarillos_bajos.values

    df_rojos = pd.json_normalize(df.rojos)
    number_rojos_altos = df_rojos.loc[:, 'altos.porcent']
    numbers_rojos_altos = number_rojos_altos.values

    number_rojos_medios = df_rojos.loc[:, 'medios.porcent']
    numbers_rojos_medios = number_rojos_medios.values

    number_rojos_bajos = df_rojos.loc[:, 'bajos.porcent']
    numbers_rojos_bajos = number_rojos_bajos.values

    df_verdes = pd.json_normalize(df.verdes)
    number_verdes_altos = df_verdes.loc[:, 'altos.porcent']
    numbers_verdes_altos = number_verdes_altos.values

    number_verdes_medios = df_verdes.loc[:, 'medios.porcent']
    numbers_verdes_medios = number_verdes_medios.values

    df_nubes = pd.json_normalize(df.nubes)
    number_nubes = df_nubes.loc[:, 'porcent']
    numbers_nubes = number_nubes.values

    df_azules["nfecha"] = df["nombre"].astype(str) + ' - ' + df["fecha"]
    df_azules['nombre'] = df[['nombre']]
    number_nombre = df_azules.loc[:, 'nfecha']
    numbers_nombre = number_nombre.values

    dataframe = pd.DataFrame({'Rojo alto': numbers_rojos_altos, 'Rojo medio': numbers_rojos_medios,
                              'Rojo bajo': numbers_rojos_bajos,

                              'Amarillo alto': numbers_amarillos_altos, 'Amarillo medio': numbers_amarillos_medios,
                              'Amarillo bajo': numbers_amarillos_bajos,

                              'Azul alto': numbers_azules_altos, 'Azul medio': numbers_azules_medios,
                              'Azul bajo': numbers_azules_bajos,

                              'Verde alto': numbers_verdes_altos, 'Verde medio': numbers_verdes_medios,
                              'Nubes': numbers_nubes
                              }, index=numbers_nombre)
    axis = dataframe.plot(kind="barh", color=['#fe0103', '#9b0004', '#680000',
                                              '#ffff33', '#cccc33', '#666600',
                                              '#33ffff', '#33cccc', '#006666',
                                              '#33ff33', '#33cc33', '#9901c4'])
    print(axis)
    plt.savefig(settings.PARCEL_FOLDER + plot_img_name, bbox_inches='tight')
    plt.close()


"""
df2 = pd.json_normalize(df.nubes)
df2['nombre'] = df[['nombre']]
print(df2)
print(len(df2))

number_column = df2.loc[:,'total']
numbers = number_column.values
print(numbers)

number_column_ = df2.loc[:,'nombre']
numbers_ = number_column_.values
print(numbers_)


dataframe = pd.DataFrame({'Nubes':numbers, 'Nubes2':numbers},
                          index =numbers_)
axis = dataframe.plot(kind="bar",color=['r', 'b'])
print(axis)
plt.show()
"""
