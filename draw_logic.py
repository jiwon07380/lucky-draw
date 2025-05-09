import random
import json
import os
from datetime import datetime
from config import PRIZE_COUNTS

BOARD_FILE = "prizes.json"
RESULTS_FILE = "results.json"
LOG_FILE = "reset_log.txt"

def generate_board():
    try:
        items = []
        for k, v in PRIZE_COUNTS.items():
            items += [k] * v
        random.shuffle(items)
        with open(BOARD_FILE, "w", encoding="utf-8") as f:
            json.dump(items, f, ensure_ascii=False)
    except Exception as e:
        log_error("generate_board", e)

def reset_results():
    try:
        with open(RESULTS_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f, ensure_ascii=False)
    except Exception as e:
        log_error("reset_results", e)

def get_board():
    try:
        with open(BOARD_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        generate_board()
        return get_board()

def draw_prize(cell_id):
    try:
        board = get_board()

        if cell_id < 0 or cell_id >= len(board):
            return "INVALID"

        result = board[cell_id]
        if result == "USED":
            return "USED"

        results = get_results(raw=True)
        results[result] = results.get(result, 0) + 1

        with open(RESULTS_FILE, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False)

        board[cell_id] = "USED"
        with open(BOARD_FILE, "w", encoding="utf-8") as f:
            json.dump(board, f, ensure_ascii=False)

        return result
    except Exception as e:
        log_error("draw_prize", e)
        return "ERROR"

def get_results(raw=False):
    try:
        with open(RESULTS_FILE, "r", encoding="utf-8") as f:
            results = json.load(f)
    except:
        results = {}

    if raw:
        return results

    order = ["1등", "2등", "3등", "4등", "꽝"]
    return {rank: results.get(rank, 0) for rank in order}

def reset_board():
    generate_board()
    reset_results()
    log("✅ 자정 초기화 완료!")

def log(message):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{now}] {message}\n")

def log_error(context, error):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{now}] ❌ {context} 오류: {error}\n")
