# 간단한 파이썬 데코레이터 예제


def my_decorator(func):
    """
    함수의 실행 시간을 측정하는 간단한 데코레이터
    """

    def wrapper(*args, **kwargs):
        import time

        # 함수 실행 전 시간 기록
        start_time = time.time()

        # 원래 함수 실행
        result = func(*args, **kwargs)

        # 함수 실행 후 시간 기록
        end_time = time.time()

        # 실행 시간 출력
        print(f"함수 {func.__name__}의 실행 시간: {end_time - start_time:.4f}초")

        return result

    return wrapper


# 데코레이터 사용 예시
@my_decorator
def calculate_sum(n):
    """1부터 n까지의 합을 계산하는 함수"""
    total = 0
    for i in range(1, n + 1):
        total += i
    return total


# 함수 호출
result = calculate_sum(1000000)
print(f"계산 결과: {result}")
