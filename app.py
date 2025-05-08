from flask import Flask, render_template, jsonify, make_response, request
from datetime import datetime, timedelta
import os, json
from draw_logic import draw_prize, get_results, get_board
from image_generator import generate_image

app = Flask(__name__)

@app.route("/")
def index():
    board = get_board()
    results = get_results()
    return render_template("index.html", board=board, results=results)

@app.route("/draw/<int:cell_id>")
def draw(cell_id):
    if request.cookies.get('has_drawn') == "true":
        return jsonify({'message': '오늘 이미 참여하셨습니다!'})

    result = draw_prize(cell_id)
    if result == "USED":
        return jsonify({'message': '이미 뽑은 칸입니다!'})

    image = generate_image(result)
    resp = make_response(jsonify({'rank': result, 'image': image}))
    expire = datetime.combine(datetime.now().date() + timedelta(days=1), datetime.min.time())
    resp.set_cookie("has_drawn", "true", expires=expire)
    return resp
