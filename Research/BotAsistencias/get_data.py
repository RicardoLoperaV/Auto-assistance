"""
get_data.py

"""
import pandas as pd
l = [7,8,9]
df = pd.DataFrame({
    'Numero':l,
    'Tipo':[1 for i in range(len(l))]
})

print(df)
#df.to_csv('data.csv', index=False)
