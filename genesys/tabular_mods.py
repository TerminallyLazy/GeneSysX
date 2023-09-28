import pandas as pd

#Listing out the column names

def list_column_names(df):
    column_names = str(df.columns)
    print(column_names)


# Creating Renaming tables


df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})

list_column_names(df)