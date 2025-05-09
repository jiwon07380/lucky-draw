import os
import hashlib
from flask import Flask, render_template, jsonify, make_response, request
from datetime import datetime, timedelta
from draw_logic import draw_prize, get_results, get_board, reset_board  # ← reset_board 추가
from image_generator import generate_image

# Flask 앱을 templates 폴더와 연결
app = Flask(__name__, template_folder='templates')

# 홈 페이지 라우트
@app.route("/")
def index():
    board = get_board()
    results = get_results()
    return render_template("index.html", board=board, results=results)

# 클라이언트 IP 추출
def get_ip():
    return request.remote_addr

# 뽑기 실행 API
@app.route("/draw/<int:cell_id>")
def draw(cell_id):
    if request.cookies.get('has_drawn') == "true":
        return jsonify({'message': '오늘 이미 참여하셨습니다!'})

    user_ip = get_ip()
    ip_hash = hashlib.md5(user_ip.encode()).hexdigest()
    if ip_hash in request.cookies.get('ip_drawn', ''):
        return jsonify({'message': '오늘 이미 참여하셨습니다!'})

    result = draw_prize(cell_id)
    if result == "USED":
        return jsonify({'message': '이미 뽑은 칸입니다!'})

    image = generate_image(result)
    resp = make_response(jsonify({'rank': result, 'image': image}))

    expire = datetime.combine(datetime.now().date() + timedelta(days=1), datetime.min.time())
    resp.set_cookie("has_drawn", "true", expires=expire)

    ip_cookie = request.cookies.get('ip_drawn', '')
    new_ip_cookie = ip_cookie + ip_hash + ";"
    resp.set_cookie("ip_drawn", new_ip_cookie, expires=expire)

    return resp

# 보드 초기화 API
@app.route("/reset", methods=["POST"])
def reset():
    try:
        reset_board()
        return jsonify({"message": "Board reset successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 서버 실행
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
