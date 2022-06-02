# %%
import pickle
import pandas as pd

with open ('../analysis/data/data.pickle', 'rb') as f:
    df = pickle.load(f)

# %%
# get rows with probability below 0.4
df[df['probability'] < 0.4]
# %%
# get rows with probabilty above 0.4
df[df['probability'] > 0.4]
# %%
# get all rows with probability between 0 and 0.05
df[(df['probability'] >= 0.8) & (df['probability'] < 0.825)]