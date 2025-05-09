import random
import json
from config import PRIZE_COUNTS

BOARD_FILE = "prizes.json"
RESULTS_FILE = "results.json"

def generate_board():
    items = []
    for k, v in PRIZE_COUNTS.items():
        items += [k] * v
    random.shuffle(items)
    with open(BOARD_FILE, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False)

def reset_results():
    with open(RESULTS_FILE, "w", encoding="utf-8") as f:
        json.dump({}, f, ensure_ascii=False)

def get_board():
    try:
        with open(BOARD_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        generate_board()
        return get_board()

def draw_prize(cell_id):
    board = get_board()
    result = board[cell_id]

    # 실시간 통계는 USED가 아닌 경우에만 집계
    if result != "USED":
        results = get_results(raw=True)
        results[result] = results.get(result, 0) + 1
        with open(RESULTS_FILE, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False)

    board[cell_id] = "USED"
    with open(BOARD_FILE, "w", encoding="utf-8") as f:
        json.dump(board, f, ensure_ascii=False)

    return result

def get_results(raw=False):
    try:
        with open(RESULTS_FILE, "r", encoding="utf-8") as f:
            results = json.load(f)
    except:
        results = {}

    if raw:
        return results

    # 원하는 순서로 정렬된 딕셔너리 반환
    order = ["1등", "2등", "3등", "4등", "꽝"]
    sorted_results = {rank: results.get(rank, 0) for rank in order}
    return sorted_results

def reset_board():
    generate_board()      # 보드 초기화
    reset_results()       # 통계 초기화
    print("✅ 자정 초기화되었습니다^0^")
