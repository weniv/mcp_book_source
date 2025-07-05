import xlsxwriter

# 엑셀 파일 생성하기(test.xlsx로 생성)
workbook = xlsxwriter.Workbook("c:/test/test.xlsx")

# 파일 안에 워크 시트 생성하기(test이름으로 생성, 여러개의 워크시트 만들 수 있음)
worksheet = workbook.add_worksheet("test")

# 워크 시트 안에 문자열 값을 넣습니다.
worksheet.write("A1", "A")
worksheet.write("B1", "B")
worksheet.write("C1", "C")
worksheet.write("D1", "D")
worksheet.write("E1", "E")

# 워크 시트 안에 숫자 값을 넣습니다.
worksheet.write("A2", 1)
worksheet.write("B2", 2)
worksheet.write("C2", 3)
worksheet.write("D2", 4)
worksheet.write("E2", 5)

# 워크 시트 안에 숫자 값을 넣습니다.
worksheet.write(2, 0, 1)
worksheet.write(2, 1, 2)
worksheet.write(2, 2, 3)
worksheet.write(2, 3, 4)
worksheet.write(2, 4, 5)

workbook.close()
