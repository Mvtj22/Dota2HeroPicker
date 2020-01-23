# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 10:57:46 2020

@author: velaz
"""
import numpy as np
import pandas as pd

games=np.load('GameWinLose.npy')
games = games.tolist()
df = pd.DataFrame (games)

filepath = 'my_excel_file.xlsx'
df.to_excel(filepath,index=False)