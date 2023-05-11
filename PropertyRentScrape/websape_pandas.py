import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import ast

file = open("result_22-06-28.txt", 'r+')
data = ast.literal_eval(file.readlines()[0])
rent_data = pd.DataFrame.from_dict(data)
rent_data = rent_data.transpose()
print (rent_data.head())
