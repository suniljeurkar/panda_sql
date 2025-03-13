import pandas as pd


filepath = "customers.csv"

df = pd.read_csv(filepath)

print("Column Names:", df.columns.tolist())
df.head()

def infer_mysql_data_types(series):
    #infer from panda series
    if pd.api.types.is_integer_dtype(series):
        return "INT"
    elif pd.api.types.is_float_dtype(series):
        return "DECIMAL(10,2)"
    elif pd.api.types.is_datetime64_any_dtype(series):
        return "DATETIME"
    elif series.apply(lambda  x : isinstance(x,str)).all():
        max_length = series.str.len().max()
        return f"VARCHAR({max(255,max_length)})"
    else:
        return "TEXT"