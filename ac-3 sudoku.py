from collections import deque

# AC-3 알고리즘을 수행하는 함수
def ac3(csp):
    # 제약 조건을 큐에 추가(큐는 데이터 구조중 하나로 요소를 저장하고 관리 방식)
    queue = deque(csp['constraints'])
   
    # 큐가 빌 때까지 반복
    while queue:
        (xi, xj) = queue.popleft()  # 큐에서 제약 조건을 꺼냄
        if revise(csp, xi, xj):  # xi의 도메인을 수정(xi,xj는 변수)
            if not csp['domains'][xi]:  # 도메인이 비었다면
                return False  # 해결 불가능
            # xi의 이웃 변수에 대해 큐에 추가
            for xk in csp['neighbors'][xi]:
                if xk != xj:
                    queue.append((xk, xi))
    return True  # 성공적으로 AC-3 알고리즘을 수행함

# 도메인을 수정하는 함수
def revise(csp, xi, xj):
    revised = False
    # xi의 모든 값에 대해
    for x in list(csp['domains'][xi]):
        # xj의 도메인에서 xi와 충족되지 않는 값이 존재하는지 확인
        if not any(satisfies(x, y) for y in csp['domains'][xj]):
            csp['domains'][xi].remove(x)  # xi의 도메인에서 x 제거
            revised = True  # 수정됨
    return revised  # 수정 여부 반환

# 두 값이 충족되는지 확인하는 함수
def satisfies(x, y):
    return x != y  # 스도쿠에서는 같은 숫자가 아닌 경우 충족됨

# 스도쿠 퍼즐을 출력하는 함수
def print_sudoku(sudoku):
    for row in sudoku:
        print(" ".join(str(num) for num in row))  # 각 행을 출력

# 스도쿠를 해결하는 함수
def solve_sudoku(sudoku):
    csp = create_csp(sudoku)  # CSP 생성(csp는 제약만족문제 줄임말)
    if ac3(csp):  # AC-3 알고리즘 수행
        return backtrack(csp)  # 백트래킹으로 해결(백트래킹은 문제해결기법중 하나로 문제의 해를 찾기위해 모든경우 탐색하는 방법)
    return None  # 해결 불가능

# CSP를 생성하는 함수
def create_csp(sudoku):
    # 각 셀의 도메인을 1부터 9까지의 집합으로 초기화
    domains = {i: set(range(1, 10)) for i in range(81)}
    constraints = []  # 제약 조건 리스트
    neighbors = {i: set() for i in range(81)}  # 이웃 변수 저장

    # 스도쿠 퍼즐을 기반으로 CSP 구성
    for i in range(9):
        for j in range(9):
            idx = i * 9 + j  # 인덱스 계산
            if sudoku[i][j] != 0:
                domains[idx] = {sudoku[i][j]}  # 이미 채워진 셀의 도메인 설정
            else:
                # 행과 열의 이웃 변수 추가
                for k in range(9):
                    if k != j:
                        neighbors[idx].add(i * 9 + k)
                    if k != i:
                        neighbors[idx].add(k * 9 + j)
                # 3x3 박스의 이웃 변수 추가
                box_x, box_y = i // 3, j // 3
                for k in range(3):
                    for l in range(3):
                        if (box_x * 3 + k) * 9 + (box_y * 3 + l) != idx:
                            neighbors[idx].add((box_x * 3 + k) * 9 + (box_y * 3 + l))

    # 제약 조건 추가
    for i in range(81):
        for j in neighbors[i]:
            constraints.append((i, j))

    return {'domains': domains, 'constraints': constraints, 'neighbors': neighbors}  # CSP 반환

# 백트래킹으로 스도쿠를 해결하는 함수
def backtrack(csp):
    # 모든 도메인이 하나의 값만 남았는지 확인
    if all(len(domain) == 1 for domain in csp['domains'].values()):
        sudoku = [[0] * 9 for _ in range(9)]  # 스도쿠 결과 저장할 배열
        for idx, domain in csp['domains'].items():
            if domain:
                num = next(iter(domain))  # 도메인에서 값 가져오기
                sudoku[idx // 9][idx % 9] = num  # 스도쿠 배열에 값 설정
        return sudoku  # 해결된 스도쿠 반환

    # 할당되지 않은 변수 찾기
    unassigned = [i for i in range(81) if len(csp['domains'][i]) > 1]
    if not unassigned:  # 할당되지 않은 변수가 없으면
        return None  # 해결 불가능

    idx = unassigned[0]  # 첫 번째 할당되지 않은 변수 선택
    for value in list(csp['domains'][idx]):
        new_csp = {key: val.copy() for key, val in csp.items()}  # 새로운 CSP 생성
        new_csp['domains'][idx] = {value}  # 현재 변수의 도메인 설정
        if ac3(new_csp):  # AC-3 알고리즘 수행
            result = backtrack(new_csp)  # 재귀적으로 백트래킹
            if result:  # 해결된 경우
                return result
    return None  # 해결 불가능

# 예시 스도쿠 퍼즐 (0은 빈 칸)
sudoku = [
    [9, 6, 7, 0, 8, 4, 0, 5, 0],
    [3, 0, 0, 0, 5, 0, 0, 7, 8],
    [0, 8, 5, 6, 0, 7, 4, 0, 9],
    [0, 5, 9, 0, 1, 3, 0, 0, 2],
    [4, 0, 0, 0, 9, 0, 3, 8, 1],
    [0, 1, 3, 0, 4, 0, 9, 6, 0],
    [0, 9, 0, 0, 7, 1, 0, 2, 6],
    [0, 2, 0, 0, 6, 5, 1, 0, 4],
    [1, 0, 6, 0, 2, 0, 0, 0, 7],
]

#또 다른 예시 위쪽 숫자 지우고 붙여넣기

#    [5, 3, 0, 0, 7, 0, 0, 0, 0],
#    [6, 0, 0, 1, 9, 5, 0, 0, 0],
#    [0, 9, 8, 0, 0, 0, 0, 6, 0],
#    [8, 0, 0, 0, 6, 0, 0, 0, 3],
#    [4, 0, 0, 8, 0, 3, 0, 0, 1],
#    [7, 0, 0, 0, 2, 0, 0, 0, 6],
#    [0, 6, 0, 0, 0, 0, 2, 8, 0],
#    [0, 0, 0, 4, 1, 9, 0, 0, 5],
#    [0, 0, 0, 0, 8, 0, 0, 7, 9],

# 스도쿠 해결불가

#    [5, 3, 0, 0, 7, 0, 0, 0, 0],
#    [6, 0, 0, 1, 9, 5, 0, 5, 0],
#    [0, 9, 8, 0, 0, 0, 0, 6, 0],
#    [8, 0, 0, 0, 6, 0, 0, 0, 3],
#    [4, 0, 6, 8, 0, 3, 0, 0, 1],
#    [7, 0, 0, 0, 2, 0, 5, 0, 6],
#    [0, 6, 0, 0, 0, 0, 2, 8, 0],
#    [0, 0, 0, 4, 1, 4, 0, 0, 5],
#    [0, 0, 3, 0, 8, 0, 0, 7, 9],







solution = solve_sudoku(sudoku)  # 스도쿠 해결 시도
if solution:
    print_sudoku(solution)  # 해결된 스도쿠 출력
else:
    print("스도쿠 해결 불가함")  # 해결 불가능 메시지 출력

print("made by hubble")
