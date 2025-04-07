import pandas as pd

# Create simple data
data = [
    {"name": "Kim Chulsoo", "age": 30, "department": "Development Team"},
    {"name": "Lee Younghee", "age": 35, "department": "Marketing Team"},
    {"name": "Park Jimin", "age": 28, "department": "HR Team"},
]

# Create DataFrame
df = pd.DataFrame(data)

# Save as Excel file
df.to_excel("c:/test/employees.xlsx", index=False)

# Read Excel file
read_df = pd.read_excel("c:/test/employees.xlsx")
print(read_df)
