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
    with open(BOARD_FILE, "w") as f:
        json.dump(items, f)
    with open(RESULTS_FILE, "w") as f:
        json.dump({}, f)

def get_board():
    try:
        with open(BOARD_FILE, "r") as f:
            return json.load(f)
    except:
        generate_board()
        return get_board()

def draw_prize(cell_id):
    board = get_board()
    result = board[cell_id]
    board[cell_id] = "USED"
    with open(BOARD_FILE, "w") as f:
        json.dump(board, f)

    # 실시간 통계 업데이트
    results = get_results()
    results[result] = results.get(result, 0) + 1
    with open(RESULTS_FILE, "w") as f:
        json.dump(results, f)

    return result

def get_results():
    try:
        with open("results.json", "r") as f:
            return json.load(f)
    except:
        return {}

def reset_board():
    # 기존 보드를 초기화
    generate_board()  # 새 보드 생성
    print("초기화되었습니다^0^")
