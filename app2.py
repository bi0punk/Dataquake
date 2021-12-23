import pandas as pd






URL = 'https://api-sismologia-chile.herokuapp.com/'
df = pd.read_json(URL)
print(df)