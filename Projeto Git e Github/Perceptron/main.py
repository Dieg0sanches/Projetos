import numpy as np
import pandas as pd
from data.generator import Gen_Data, Data_3D
from perceptron import Perceptron
from graphics import Gráfico_2D, Gráfico_3D

iterations = int(input("Quantas iterações sobre o dataset você deseja? "))
flag = input("2D ou 3D? ")

#separando as duas classes
if (flag == '2D'):
    Data = Gen_Data()
    theta = np.zeros(3)
    theta = Perceptron(iterations, theta, 1, Data, 60, 30)

    Gráfico_2D(Data, theta)
else:
    Data = Data_3D()
    theta = np.zeros(4)
    theta = Perceptron(iterations, theta, 1, Data, 100, 50)

    Gráfico_3D(Data, theta)

