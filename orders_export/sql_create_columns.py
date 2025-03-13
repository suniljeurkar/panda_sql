import mysql.connector
import pandas as pd

# Path to CSV file
filepath = "employees.csv"
# Define table name
table_name = "Employees"
# Read CSV into a DataFrame
df = pd.read_csv(filepath)

print("Column Names:", df.columns.tolist())

# Function to infer MySQL data types from pandas Series
def infer_mysql_data_types(series):
    """Infer MySQL data type from pandas Series."""
    if pd.api.types.is_integer_dtype(series):
        return "INT"
    elif pd.api.types.is_float_dtype(series):
        return "DECIMAL(10,2)"
    elif pd.api.types.is_datetime64_any_dtype(series):
        return "DATETIME"
    elif series.apply(lambda x: isinstance(x, str)).all():
        max_length = series.str.len().max() if not series.empty else 255
        return f"VARCHAR({max(255, max_length)})"  # Ensures VARCHAR has a reasonable length
    else:
        return "TEXT"

# Connect to MySQL
con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  # Change if you have a password
    database="northwind_mysql"
)
cursor = con.cursor()



# Infer column data types and format column definitions correctly
column_definitions = []
for col in df.columns:
    col_type = infer_mysql_data_types(df[col])
    column_definitions.append(f"`{col}` {col_type}")

# Create table query with correctly formatted column definitions
create_table_query = f"""CREATE TABLE IF NOT EXISTS `{table_name}` ({', '.join(column_definitions)});"""

# Execute table creation
cursor.execute(create_table_query)
con.commit()
print(f"Table `{table_name}` created successfully!")
