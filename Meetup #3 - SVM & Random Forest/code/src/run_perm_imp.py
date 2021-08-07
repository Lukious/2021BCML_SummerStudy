import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_absolute_error
from pandas.api.types import is_string_dtype, is_numeric_dtype, is_object_dtype, is_categorical_dtype
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.base import clone
import cProfile, pstats, io
from pstats import SortKey

from timeit import default_timer as timer

from rfpimp import *

df = pd.read_feather("/Users/parrt/github/mlbook-private/data/bulldozer-train-num.feather")

rf = RandomForestRegressor(n_estimators=50,
                           n_jobs=-1,
                           oob_score=True,
                           max_features=.4)
X_train, y_train = df.drop('SalePrice', axis=1), df['SalePrice']

print("Data loaded")

rf.fit(X_train, y_train)

print("Model fit")

start = timer() # ------------

#I = oob_importances(rf, X_train, y_train, n_samples=3000)
profiler = cProfile.Profile()
profiler.enable()
I = importances(rf, X_train, y_train, n_samples=3000)
profiler.disable()

end = timer() # ------------
print(f"{end - start:.2f}s")

s = io.StringIO()
sortby = SortKey.TIME
ps = pstats.Stats(profiler, stream=s).sort_stats(sortby)
ps.print_stats()
print(s.getvalue())

viz = plot_importances(I)
viz.view()
