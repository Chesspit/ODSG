import pandas as pd

# create a sample dataframe
df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie', 'David'],
    'age': [25, 30, 35, 40],
    'gender': ['F', 'M', 'M', 'M']
})

# filter the dataframe on two columns with different types
filtered_df = df.loc[(df['age'] > 30) & (df['gender'] == 'M')]

# print the filtered dataframe
print(filtered_df)