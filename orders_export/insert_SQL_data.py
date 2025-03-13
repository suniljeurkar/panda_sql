import mysql.connector
import pandas as pd

# File path to the uploaded CSV
file_path = "employees.csv"
# Define table name
table_name = "Employees"

# Read the CSV file into a DataFrame
df = pd.read_csv(file_path)

# Replace NaN values with None (MySQL NULL)
df = df.where(pd.notna(df), None)

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  # Change if needed
    database="northwind_mysql"
)
cursor = conn.cursor()



# Prepare the INSERT query dynamically
columns = df.columns.tolist()
placeholders = ", ".join(["%s"] * len(columns))  # Generates "%s, %s, %s, ..." based on column count
insert_query = f"INSERT INTO `{table_name}` ({', '.join(columns)}) VALUES ({placeholders})"

# Insert data row by row, handling NaN values
for row in df.itertuples(index=False, name=None):
    cursor.execute(insert_query, tuple(None if pd.isna(x) else x for x in row))  # Convert NaN to None

# Commit and close connection
conn.commit()
conn.close()
print("CSV Data Inserted Successfully!")
