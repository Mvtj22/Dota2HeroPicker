# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 09:35:23 2020

@author: velaz
"""

import numpy as np

games = np.zeros((129,129))
print(games)
np.save('GameWinLose', games)