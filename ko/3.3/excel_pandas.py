import pandas as pd

# 간단한 데이터 생성
data = [
    {"name": "김철수", "age": 30, "department": "개발팀"},
    {"name": "이영희", "age": 35, "department": "마케팅팀"},
    {"name": "박지민", "age": 28, "department": "인사팀"},
]

# 데이터프레임 생성
df = pd.DataFrame(data)

# 엑셀 파일로 저장
df.to_excel("c:/test/employees.xlsx", index=False)

# 엑셀 파일 읽기
read_df = pd.read_excel("c:/test/employees.xlsx")
print(read_df)
