import xlsxwriter

# Create Excel file
workbook = xlsxwriter.Workbook("c:/test/employee_details.xlsx")

# Add worksheets
worksheet = workbook.add_worksheet("Employee Info")
summary_sheet = workbook.add_worksheet("Summary")

# Define cell formats
header_format = workbook.add_format(
    {
        "bold": True,
        "font_color": "white",
        "bg_color": "#4472C4",
        "align": "center",
        "valign": "vcenter",
        "border": 1,
    }
)

date_format = workbook.add_format({"num_format": "yyyy-mm-dd"})
money_format = workbook.add_format({"num_format": "#,##0"})
percent_format = workbook.add_format({"num_format": "0.0%"})
border_format = workbook.add_format({"border": 1})

# Set column widths
worksheet.set_column("A:A", 15)
worksheet.set_column("B:B", 10)
worksheet.set_column("C:C", 15)
worksheet.set_column("D:D", 15)
worksheet.set_column("E:E", 15)

# Add headers
headers = ["Name", "Age", "Department", "Hire Date", "Salary"]
for col, header in enumerate(headers):
    worksheet.write(0, col, header, header_format)

# Add data
employee_data = [
    ["Kim Chulsoo", 30, "Development Team", "2021-01-15", 45000000],
    ["Lee Younghee", 35, "Marketing Team", "2019-05-20", 55000000],
    ["Park Jimin", 28, "HR Team", "2022-03-10", 42000000],
    ["Choi Yujin", 32, "Sales Team", "2020-11-05", 60000000],
    ["Jung Minsoo", 27, "Development Team", "2022-08-22", 43000000],
]

# Fill data rows
for row_num, employee in enumerate(employee_data):
    worksheet.write(row_num + 1, 0, employee[0], border_format)  # Name
    worksheet.write(row_num + 1, 1, employee[1], border_format)  # Age
    worksheet.write(row_num + 1, 2, employee[2], border_format)  # Department
    worksheet.write(row_num + 1, 3, employee[3], date_format)  # Hire Date
    worksheet.write(row_num + 1, 4, employee[4], money_format)  # Salary

# Add conditional formatting (change background color if salary is 50M or higher)
worksheet.conditional_format(
    "E2:E6",
    {
        "type": "cell",
        "criteria": ">=",
        "value": 50000000,
        "format": workbook.add_format({"bg_color": "#C6EFCE"}),
    },
)

# Calculate totals
total_row = len(employee_data) + 1
worksheet.write(total_row, 0, "Total", workbook.add_format({"bold": True}))
worksheet.write_formula(total_row, 4, f"=SUM(E2:E{total_row})", money_format)

# Add data to summary sheet
summary_sheet.write(
    0,
    0,
    "Employees and Average Salary by Department",
    workbook.add_format({"bold": True, "font_size": 14}),
)
summary_sheet.write(2, 0, "Department", header_format)
summary_sheet.write(2, 1, "Number of Employees", header_format)
summary_sheet.write(2, 2, "Average Salary", header_format)

# Department list (remove duplicates)
departments = list(set([emp[2] for emp in employee_data]))

# Calculate and record department statistics
for i, dept in enumerate(departments):
    row = i + 3
    dept_employees = [emp for emp in employee_data if emp[2] == dept]
    count = len(dept_employees)
    avg_salary = sum([emp[4] for emp in dept_employees]) / count

    summary_sheet.write(row, 0, dept, border_format)
    summary_sheet.write(row, 1, count, border_format)
    summary_sheet.write(row, 2, avg_salary, money_format)

# Add chart
chart = workbook.add_chart({"type": "column"})
chart.add_series(
    {
        "name": "Average Salary",
        "categories": ["Summary", 3, 0, 3 + len(departments) - 1, 0],
        "values": ["Summary", 3, 2, 3 + len(departments) - 1, 2],
        "data_labels": {"value": True, "num_format": "#,##0"},
    }
)
chart.set_title({"name": "Average Salary by Department"})
chart.set_x_axis({"name": "Department"})
chart.set_y_axis({"name": "Salary (KRW)"})
summary_sheet.insert_chart("E3", chart, {"x_scale": 1.5, "y_scale": 1.5})

# Save Excel file
workbook.close()

print("employee_details.xlsx file has been created in the c:/test folder.")
