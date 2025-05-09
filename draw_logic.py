import random
import json
import os
from datetime import datetime
from config import PRIZE_COUNTS

BOARD_FILE = "prizes.json"
RESULTS_FILE = "results.json"

# 새 보드 생성 (USED 없음)
def generate_board():
    items = []
    for k, v in PRIZE_COUNTS.items():
        items += [k] * v
    random.shuffle(items)
    with open(BOARD_FILE, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False)

# 결과 초기화
def reset_results():
    with open(RESULTS_FILE, "w", encoding="utf-8") as f:
        json.dump({}, f, ensure_ascii=False)

# 📌 새로고침할 때 보드는 다시 읽기만 한다 (없을 때만 생성)
def get_board():
    if not os.path.exists(BOARD_FILE):
        generate_board()
    with open(BOARD_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# 뽑기 실행
def draw_prize(cell_id):
    board = get_board()
    if board[cell_id] == "USED":
        return "USED"

    result = board[cell_id]

    results = get_results(raw=True)
    results[result] = results.get(result, 0) + 1
    with open(RESULTS_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False)

    board[cell_id] = "USED"
    with open(BOARD_FILE, "w", encoding="utf-8") as f:
        json.dump(board, f, ensure_ascii=False)

    return result

# 통계 반환
def get_results(raw=False):
    if not os.path.exists(RESULTS_FILE):
        reset_results()
    with open(RESULTS_FILE, "r", encoding="utf-8") as f:
        results = json.load(f)

    if raw:
        return results

    order = ["1등", "2등", "3등", "4등", "꽝"]
    return {rank: results.get(rank, 0) for rank in order}

# 전체 초기화 (자정 또는 배포 시에만 호출됨)
def reset_board():
    generate_board()
    reset_results()
    print("✅ 자정 또는 배포 시 전체 보드 초기화 완료")
