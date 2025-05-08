import os
from flask import Flask, render_template, jsonify, make_response, request
from datetime import datetime, timedelta
import hashlib
from draw_logic import draw_prize, get_results, get_board
from image_generator import generate_image

app = Flask(__name__)

def get_ip():
    return request.remote_addr  # 클라이언트 IP 주소를 받아옵니다.

@app.route("/draw/<int:cell_id>")
def draw(cell_id):
    # 쿠키로 중복 방지
    if request.cookies.get('has_drawn') == "true":
        return jsonify({'message': '오늘 이미 참여하셨습니다!'})

    # IP로 중복 방지
    user_ip = get_ip()
    ip_hash = hashlib.md5(user_ip.encode()).hexdigest()  # IP를 해시값으로 변환
    if ip_hash in request.cookies.get('ip_drawn', ''):
        return jsonify({'message': '오늘 이미 참여하셨습니다!'})

    result = draw_prize(cell_id)
    if result == "USED":
        return jsonify({'message': '이미 뽑은 칸입니다!'})

    image = generate_image(result)
    resp = make_response(jsonify({'rank': result, 'image': image}))

    # 쿠키 설정
    expire = datetime.combine(datetime.now().date() + timedelta(days=1), datetime.min.time())
    resp.set_cookie("has_drawn", "true", expires=expire)
    
    # IP 기록
    ip_cookie = request.cookies.get('ip_drawn', '')
    new_ip_cookie = ip_cookie + ip_hash + ";"
    resp.set_cookie("ip_drawn", new_ip_cookie, expires=expire)

    return resp


# Flask가 Render의 자동 포트를 사용하도록 설정
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render에서 포트를 환경 변수로 받아옴
    app.run(host='0.0.0.0', port=port)  # 포트 설정
