from PIL import Image, ImageDraw, ImageFont
import os

def generate_image(rank):
    base = Image.new("RGB", (600, 400), "#FFF7F1")
    draw = ImageDraw.Draw(base)

    font_path = "C:\\Windows\\Fonts\\malgun.ttf"  # 또는 서버 배포 시 폰트 포함 경로 지정
    font = ImageFont.truetype(font_path, 36)

    messages = {
        "1등": "🎉 행운의 뽑기 결과는 1등! 🎉",
        "2등": "🥈 2등! 좋은 일이 생길 거예요!",
        "3등": "🥉 3등도 나쁘지 않죠!",
        "4등": "👏 4등, 그래도 행운입니다!",
        "꽝": "😅 아쉽지만 도전은 행운이에요!"
    }

    text = messages.get(rank, f"{rank} 당첨!")
    draw.text((50, 150), text, fill="#FF69B4", font=font)

    folder = "static/result_images"
    os.makedirs(folder, exist_ok=True)
    filename = f"{folder}/{rank}.png"
    base.save(filename)
    return filename
